import re

# Uniquement les hallucinations vraiment dangereuses
PATTERNS_HALLUCINATION = [
    r"\+228\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{2}",  # numéros de téléphone inventés
    r"\b0\d{1}\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{2}\b",  # format mobile inventé
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",  # emails inventés
    r"(?:https?://|www\.)[^\s]+(?<!tde\.tg)[^\s]*",  # URLs autres que tde.tg
]

# Mots interdits — promesses non tenables uniquement
MOTS_INTERDITS = [
    "je garantis",
    "je vous assure que",
    "dans l'heure",
]

# Remplacements pour mots interdits
REPLACEMENTS = {
    "je garantis": "nous vous informons",
    "je vous assure que": "selon nos informations",
    "dans l'heure": "dans les meilleurs délais",
}

MAX_RESPONSE_LENGTH = 1200
MIN_RESPONSE_LENGTH = 10

MOTS_FRANCAIS = ["vous", "votre", "nous", "pour", "est", "les", "des", "une", "que"]


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
            print(f"⚠️ Hallucination détectée — pattern : {pattern}")
            return False, f"Pattern suspect : {pattern}"
    return True, ""


def _clean_hallucinations(response: str) -> str:
    for pattern in PATTERNS_HALLUCINATION:
        response = re.sub(
            pattern, "[information non disponible]",
            response, flags=re.IGNORECASE
        )
    return response


def _clean_mots_interdits(response: str) -> str:
    for mot, replacement in REPLACEMENTS.items():
        response = response.replace(mot, replacement)
    return response


def _check_langue(response: str) -> bool:
    response_lower = response.lower()
    score = sum(1 for mot in MOTS_FRANCAIS if mot in response_lower)
    return score >= 2


def validate_response(response: str, intent: str = None) -> dict:
    """
    Valide et nettoie la réponse générée par le LLM.
    Retourne : { valid, response, use_fallback, reason }
    """
    if not response or not response.strip():
        return {"valid": False, "response": None,
                "use_fallback": True, "reason": "Réponse vide"}

    # 1. Longueur
    length_ok, response = _check_length(response)
    if not length_ok:
        return {"valid": False, "response": None,
                "use_fallback": True, "reason": response}

    # 2. Hallucinations
    hall_ok, reason = _check_hallucinations(response)
    if not hall_ok:
        response_cleaned = _clean_hallucinations(response)
        if response_cleaned != response:
            print("✅ Hallucination nettoyée")
            response = response_cleaned
        else:
            return {"valid": False, "response": None,
                    "use_fallback": True, "reason": reason}

    # 3. Mots interdits
    for mot in MOTS_INTERDITS:
        if mot in response.lower():
            response = _clean_mots_interdits(response)
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