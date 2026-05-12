import re

# Uniquement les URLs non-TDE — le reste est géré par le prompt
PATTERNS_HALLUCINATION = [
    r"(?:https?://|www\.)[^\s]*(?<!\btde\.tg\b)[^\s]*",  # URLs autres que tde.tg
]

MAX_RESPONSE_LENGTH = 1200
MIN_RESPONSE_LENGTH = 10

MOTS_FRANCAIS = ["vous", "votre", "nous", "pour", "est", "les", "des", "une", "que"]

# Remplacements pour formulations non conformes
REPLACEMENTS = {
    "je garantis": "nous vous informons",
    "je vous assure que": "selon nos informations",
    "dans l'heure": "dans les meilleurs délais",
}


def _check_length(response: str) -> tuple:
    if len(response) < MIN_RESPONSE_LENGTH:
        return False, "Réponse trop courte"
    if len(response) > MAX_RESPONSE_LENGTH:
        truncated = response[:MAX_RESPONSE_LENGTH]
        last_dot = truncated.rfind(".")
        if last_dot > 0:
            return True, truncated[:last_dot + 1]
        return True, truncated
    return True, response


def _check_hallucinations(response: str) -> tuple:
    for pattern in PATTERNS_HALLUCINATION:
        if re.search(pattern, response, re.IGNORECASE):
            print(f"⚠️ URL suspecte détectée")
            return False, "URL non autorisée"
    return True, ""


def _clean_hallucinations(response: str) -> str:
    for pattern in PATTERNS_HALLUCINATION:
        response = re.sub(
            pattern, "[information non disponible]",
            response, flags=re.IGNORECASE
        )
    return response


def _clean_formulations(response: str) -> str:
    for mot, replacement in REPLACEMENTS.items():
        response = response.replace(mot, replacement)
    return response


def _check_langue(response: str) -> bool:
    response_lower = response.lower()
    score = sum(1 for mot in MOTS_FRANCAIS if mot in response_lower)
    return score >= 2


def validate_response(response: str, intent: str = None) -> dict:
    """
    Validation légère — le prompt gère les règles métier principales.
    Ce module reste un filet de sécurité pour les cas extrêmes.
    """
    if not response or not response.strip():
        return {"valid": False, "response": None,
                "use_fallback": True, "reason": "Réponse vide"}

    # 1. Longueur
    length_ok, response = _check_length(response)
    if not length_ok:
        return {"valid": False, "response": None,
                "use_fallback": True, "reason": response}

    # 2. URLs suspectes
    hall_ok, reason = _check_hallucinations(response)
    if not hall_ok:
        response_cleaned = _clean_hallucinations(response)
        print("URL nettoyée")
        response = response_cleaned

    # 3. Formulations non conformes
    for mot in REPLACEMENTS:
        if mot in response.lower():
            response = _clean_formulations(response)
            print("Formulation nettoyée")
            break

    # 4. Langue
    if not _check_langue(response):
        return {"valid": False, "response": None,
                "use_fallback": True, "reason": "Réponse pas en français"}

    return {
        "valid": True,
        "response": response.strip(),
        "use_fallback": False,
        "reason": ""
    }