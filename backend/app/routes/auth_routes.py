from flask import (
    Blueprint,
    request,
    jsonify,
    redirect,
    make_response
)

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from backend.app.services.user_service import (
    create_user,
    authenticate_user,
    get_user_by_id
)
from backend.app.config.config import (
    FRONTEND_URL,
    OAUTH_COOKIE_SECURE,
    OAUTH_STATE_COOKIE_NAME,
    OAUTH_STATE_TTL_SECONDS
)
from backend.app.services.google_oauth_service import (
    GoogleOAuthError,
    complete_google_callback,
    exchange_login_code,
    start_google_oauth
)

auth_bp = Blueprint(
    "auth",
    __name__
)


# =========================================
# REGISTER
# =========================================

@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    data = request.get_json() or {}

    nom = data.get(
        "nom",
        ""
    ).strip()

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    user_id, error = create_user(
        email=email,
        password=password,
        nom=nom
    )

    if error:

        return jsonify({
            "status": "error",
            "message": error
        }), 400

    return jsonify({
        "status": "success",
        "message": "Utilisateur créé avec succès",
        "user_id": user_id
    }), 201


# =========================================
# LOGIN
# =========================================

@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json() or {}

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    user = authenticate_user(
        email=email,
        password=password
    )

    if not user:

        return jsonify({
            "status": "error",
            "message": "Email ou mot de passe incorrect"
        }), 401

    token = create_access_token(
        identity=str(user["id"]),
        additional_claims={
            "role": user["role"]
        }
    )

    return jsonify({
        "status": "success",
        "message": "Connexion réussie",
        "token": token,
        "user": {
            "id": user["id"],
            "nom": user["nom"],
            "email": user["email"],
            "role": user["role"]
        }
    }), 200


# =========================================
# CURRENT USER
# =========================================

@auth_bp.route(
    "/me",
    methods=["GET"]
)
@jwt_required()
def me():

    user_id = get_jwt_identity()

    user = get_user_by_id(
        int(user_id)
    )

    if not user:

        return jsonify({
            "status": "error",
            "message": "Utilisateur introuvable"
        }), 404

    return jsonify({
        "status": "success",
        "user": user
    }), 200


# =========================================
# HEALTH CHECK AUTH
# =========================================

@auth_bp.route(
    "/verify",
    methods=["GET"]
)
@jwt_required()
def verify_token():

    return jsonify({
        "status": "success",
        "message": "Token valide"
    }), 200


# =========================================
# GOOGLE OAUTH
# =========================================

@auth_bp.route(
    "/google/start",
    methods=["POST"]
)
def google_start():

    data = request.get_json() or {}

    session_id = data.get("session_id")
    redirect_path = data.get("redirect_path", "/user/chat")

    try:
        oauth_start = start_google_oauth(
            session_id=session_id,
            redirect_path=redirect_path
        )
    except GoogleOAuthError as e:
        return jsonify({
            "status": "error",
            "error": e.code,
            "message": e.message
        }), e.status_code

    response = jsonify({
        "status": "success",
        "auth_url": oauth_start["auth_url"]
    })

    response.set_cookie(
        OAUTH_STATE_COOKIE_NAME,
        oauth_start["state"],
        max_age=OAUTH_STATE_TTL_SECONDS,
        httponly=True,
        secure=OAUTH_COOKIE_SECURE,
        samesite="Lax"
    )

    return response, 200


@auth_bp.route(
    "/google/callback",
    methods=["GET"]
)
def google_callback():

    error = request.args.get("error")

    if error:
        return redirect(
            f"{FRONTEND_URL}/user/chat?oauth=cancelled"
        )

    code = request.args.get("code")
    state = request.args.get("state")
    cookie_state = request.cookies.get(OAUTH_STATE_COOKIE_NAME)

    try:
        result = complete_google_callback(
            code=code,
            state=state,
            cookie_state=cookie_state
        )
    except GoogleOAuthError as e:
        response = redirect(
            f"{FRONTEND_URL}/user/chat?oauth_error={e.code}"
        )
        response.delete_cookie(OAUTH_STATE_COOKIE_NAME)
        return response

    response = redirect(
        f"{FRONTEND_URL}/auth/google/success?code={result['exchange_code']}"
    )
    response.delete_cookie(OAUTH_STATE_COOKIE_NAME)
    return response


@auth_bp.route(
    "/google/exchange",
    methods=["POST"]
)
def google_exchange():

    data = request.get_json() or {}
    exchange_code = data.get("code")

    try:
        result = exchange_login_code(exchange_code)
    except GoogleOAuthError as e:
        return jsonify({
            "status": "error",
            "error": e.code,
            "message": e.message
        }), e.status_code

    user = result["user"]

    token = create_access_token(
        identity=str(user["id"]),
        additional_claims={
            "role": user["role"]
        }
    )

    return jsonify({
        "status": "success",
        "message": "Connexion Google réussie",
        "token": token,
        "attached_conversations": result["attached_conversations"],
        "user": {
            "id": user["id"],
            "nom": user["nom"],
            "email": user["email"],
            "role": user["role"]
        }
    }), 200
