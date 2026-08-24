import hashlib
import json
import logging
import secrets
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import jwt
from jwt import PyJWKClient
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidAudienceError,
    InvalidIssuerError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
    PyJWKClientError,
)

from backend.app.config.config import (
    ALLOWED_OAUTH_REDIRECT_PATHS,
    GOOGLE_CALLBACK_URL,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    OAUTH_EXCHANGE_CODE_TTL_SECONDS,
    OAUTH_STATE_TTL_SECONDS
)
from backend.app.repositories.conversation_repository import (
    attach_anonymous_conversations
)
from backend.app.repositories.oauth_state_repository import (
    consume_exchange_code,
    consume_oauth_state,
    create_exchange_code,
    create_oauth_state
)
from backend.app.services.user_service import (
    get_or_create_google_user,
    get_user_by_id
)


GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
GOOGLE_ISSUERS = {
    "accounts.google.com",
    "https://accounts.google.com"
}


class GoogleOAuthError(Exception):
    def __init__(self, message, status_code=400, code="google_oauth_error"):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code


def _hash_secret(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _validate_config():
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise GoogleOAuthError(
            "Google OAuth n'est pas configuré",
            500,
            "google_oauth_not_configured"
        )


def _validate_redirect_path(redirect_path):
    if redirect_path in ALLOWED_OAUTH_REDIRECT_PATHS:
        return redirect_path

    return "/user/chat"


def start_google_oauth(session_id, redirect_path="/user/chat"):
    _validate_config()

    if not session_id:
        raise GoogleOAuthError(
            "session_id requis",
            400,
            "missing_session_id"
        )

    safe_redirect_path = _validate_redirect_path(redirect_path)
    state = secrets.token_urlsafe(32)
    state_hash = _hash_secret(state)

    create_oauth_state(
        state_hash=state_hash,
        session_id=session_id,
        redirect_path=safe_redirect_path,
        ttl_seconds=OAUTH_STATE_TTL_SECONDS
    )

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_CALLBACK_URL,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "online",
        "prompt": "select_account"
    }

    return {
        "auth_url": f"{GOOGLE_AUTH_URL}?{urlencode(params)}",
        "state": state
    }


def complete_google_callback(code, state, cookie_state):
    _validate_config()

    if not code or not state:
        raise GoogleOAuthError(
            "Paramètres OAuth manquants",
            400,
            "missing_oauth_parameters"
        )

    if not cookie_state or not secrets.compare_digest(state, cookie_state):
        raise GoogleOAuthError(
            "State OAuth invalide",
            400,
            "invalid_oauth_state"
        )

    state_row = consume_oauth_state(_hash_secret(state))

    if not state_row:
        raise GoogleOAuthError(
            "State OAuth expiré ou déjà utilisé",
            400,
            "invalid_oauth_state"
        )

    token_payload = _exchange_authorization_code(code)
    claims = _validate_id_token(token_payload.get("id_token"))

    if not claims.get("email_verified"):
        raise GoogleOAuthError(
            "L'email Google n'est pas vérifié",
            403,
            "google_email_not_verified"
        )

    user, error = get_or_create_google_user(
        email=claims["email"].lower(),
        nom=claims.get("name") or claims["email"],
        provider_subject=claims["sub"],
        email_verified=True
    )

    if error or not user:
        raise GoogleOAuthError(
            error or "Impossible de créer l'utilisateur Google",
            400,
            "google_user_error"
        )

    attached = attach_anonymous_conversations(
        session_id=state_row["session_id"],
        user_id=user["id"]
    )

    exchange_code = secrets.token_urlsafe(32)

    create_exchange_code(
        code_hash=_hash_secret(exchange_code),
        user_id=user["id"],
        attached_conversations=attached,
        ttl_seconds=OAUTH_EXCHANGE_CODE_TTL_SECONDS
    )

    return {
        "exchange_code": exchange_code,
        "redirect_path": state_row["redirect_path"],
        "attached_conversations": attached
    }


def exchange_login_code(exchange_code):
    if not exchange_code:
        raise GoogleOAuthError(
            "Code d'échange requis",
            400,
            "missing_exchange_code"
        )

    row = consume_exchange_code(_hash_secret(exchange_code))

    if not row:
        raise GoogleOAuthError(
            "Code d'échange invalide ou expiré",
            400,
            "invalid_exchange_code"
        )

    user = get_user_by_id(row["user_id"])

    if not user:
        raise GoogleOAuthError(
            "Utilisateur introuvable",
            404,
            "user_not_found"
        )

    return {
        "user": user,
        "attached_conversations": row["attached_conversations"]
    }


def _exchange_authorization_code(code):
    body = urlencode({
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_CALLBACK_URL,
        "grant_type": "authorization_code"
    }).encode("utf-8")

    request = Request(
        GOOGLE_TOKEN_URL,
        data=body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method="POST"
    )

    try:
        with urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        logging.error(f"Erreur échange code Google : {e}")
        raise GoogleOAuthError(
            "Échec de l'échange OAuth Google",
            502,
            "google_token_exchange_failed"
        )


def _validate_id_token(id_token):
    if not id_token:
        raise GoogleOAuthError(
            "id_token Google manquant",
            400,
            "missing_google_id_token"
        )

    try:
        jwk_client = PyJWKClient(GOOGLE_JWKS_URL, cache_jwk_set=False)
        signing_key = jwk_client.get_signing_key_from_jwt(id_token)
        claims = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=GOOGLE_CLIENT_ID,
            options={
                "require": [
                    "exp",
                    "iat",
                    "iss",
                    "aud",
                    "sub",
                    "email"
                ]
            }
        )
    except PyJWKClientError as e:
        logging.error("JWKS Google introuvable pour id_token : %s: %s", type(e).__name__, e)
        raise GoogleOAuthError(
            "Cle de signature Google introuvable",
            401,
            "invalid_google_signature"
        )
    except InvalidAudienceError as e:
        logging.error("Audience id_token Google incorrecte (attendu=%s) : %s", GOOGLE_CLIENT_ID, e)
        raise GoogleOAuthError(
            "Audience token Google invalide",
            401,
            "invalid_google_audience"
        )
    except ExpiredSignatureError as e:
        logging.error("id_token Google expire : %s", e)
        raise GoogleOAuthError(
            "Token Google expire",
            401,
            "expired_google_token"
        )
    except InvalidIssuerError as e:
        logging.error("Issuer id_token Google invalide : %s", e)
        raise GoogleOAuthError(
            "Issuer token Google invalide",
            401,
            "invalid_google_issuer"
        )
    except InvalidSignatureError as e:
        logging.error("Signature id_token Google invalide : %s", e)
        raise GoogleOAuthError(
            "Signature token Google invalide",
            401,
            "invalid_google_signature"
        )
    except MissingRequiredClaimError as e:
        logging.error("Claim obligatoire manquant dans id_token Google : %s", e)
        raise GoogleOAuthError(
            "Claim Google manquant",
            401,
            "invalid_google_token"
        )
    except (DecodeError, InvalidTokenError) as e:
        logging.error("id_token Google illisible : %s", e)
        raise GoogleOAuthError(
            "Token Google illisible",
            401,
            "invalid_google_token"
        )
    except Exception as e:
        logging.error("Erreur inattendue validation id_token Google : %s: %s", type(e).__name__, e)
        raise GoogleOAuthError(
            "Token Google invalide",
            401,
            "invalid_google_token"
        )

    if claims.get("iss") not in GOOGLE_ISSUERS:
        raise GoogleOAuthError(
            "Issuer Google invalide",
            401,
            "invalid_google_issuer"
        )

    if not claims.get("sub"):
        raise GoogleOAuthError(
            "Identifiant Google manquant",
            401,
            "missing_google_subject"
        )

    return claims
