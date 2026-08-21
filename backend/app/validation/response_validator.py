import re
import unicodedata

# Uniquement les URLs non-TDE — le reste est géré par le prompt
PATTERNS_HALLUCINATION = [
    r"(?:https?://|www\.)[^\s]*(?<!\btde\.tg\b)[^\s]*",  # URLs autres que tde.tg
]

MAX_RESPONSE_LENGTH = 1200
MIN_RESPONSE_LENGTH = 10

# Mots-outils / fonctions français très fréquents et distincts de l'anglais.
# Utilisés comme signal positif (présence d'au moins un mot-outil français).
MOTS_OUTILS_FRANCAIS = {
    "le", "la", "les", "un", "une", "des", "du", "de", "et", "ou", "que", "qui",
    "ce", "cette", "je", "tu", "il", "elle", "nous", "vous", "ils", "elles",
    "est", "sont", "a", "ont", "pour", "par", "sur", "avec", "dans", "en", "au",
    "aux", "pas", "plus", "ne", "se", "sa", "son", "ses", "leur", "leurs", "mon",
    "ton", "ma", "ce", "cet", "chez", "vers", "sans", "sous", "entre", "apres",
    "avant", "pendant", "comme", "mais", "donc", "car", "si", "quand", "comment",
    "ou", "pourquoi", "quel", "quelle", "notre", "votre", "leur", "meme", "tout",
    "tous", "toute", "chaque", "ici", "la", "y", "d", "l", "j", "n", "s", "c",
    "son", "une", "des", "aux", "du", "bonjour", "bonsoir", "merci", "oui",
    "non", "salut", "information",
}

# Suffixes morphologiques typiquement français (complémentaire, pas une règle stricte).
SUFFIXES_FRANCAIS = (
    "tion", "ment", "eur", "euse", "ique", "able", "ible", "aux", "ence",
    "ance", "ite", "eaux", "age", "iste", "esse",
)

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
    """Vérifie raisonnablement qu'une réponse est compatible avec le français.

    Approche positive (présence de signaux français : mots-outils, diacritiques,
    morphologie) couplée à un garde-fou (ratio) pour éviter qu'une phrase non
    française ne passe à cause de quelques mots isolés.
    Ne rejette PAS une phrase française courte ou nominale.
    """
    raw_tokens = re.findall(r"[a-zàâäéèêëîïôöùûüç0-9']+", response.lower())
    if not raw_tokens:
        return False

    french_like = 0
    has_function_word = False
    has_diacritic = False

    for tok in raw_tokens:
        nfd = unicodedata.normalize("NFD", tok)
        if any(unicodedata.category(c) == "Mn" for c in nfd):
            has_diacritic = True
        stripped = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
        if stripped in MOTS_OUTILS_FRANCAIS:
            has_function_word = True
            french_like += 1
        elif stripped.endswith(SUFFIXES_FRANCAIS):
            french_like += 1
        elif has_diacritic and len(stripped) >= 4:
            # mot portant un diacritique et suffisamment long → probablement français
            french_like += 1

    ratio = french_like / len(raw_tokens)

    # Acceptation : assez d'indices français ET
    # (mot-outil français OU diacritique OU ratio élevé)
    if french_like >= 2 and (has_function_word or has_diacritic or ratio >= 0.5):
        return True
    return False


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