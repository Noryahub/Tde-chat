import re
import unicodedata

# Détection d'URL (formes http(s):// et www.)
URL_RE = re.compile(r"https?://[^\s]+|www\.[^\s]+", re.IGNORECASE)
# Domaine officiel de la TdE. Toute URL de ce domaine est potentiellement valide
# (provenant du site officiel) ; seules les URL externes sont des hallucinations.
# La distinction « connue / inconnue » (présente ou non dans le contexte RAG)
# est appliquée quand le contexte est fourni (voir validate_response).
TDE_DOMAIN = "tde.tg"

MAX_RESPONSE_LENGTH = 1200
MIN_RESPONSE_LENGTH = 2

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


def _extract_urls(text: str) -> list:
    return URL_RE.findall(text or "")


def _known_urls(context_docs) -> set:
    """Ensemble des URL présentes dans le contexte RAG (source + texte)."""
    known = set()
    for d in context_docs or []:
        if isinstance(d, dict):
            if d.get("source"):
                known.add(d["source"].rstrip("/").lower())
            for u in _extract_urls(d.get("text", "")):
                known.add(u.rstrip("/").lower())
    return known


def _is_tde_url(url: str) -> bool:
    return TDE_DOMAIN in (url or "").lower()


def _check_hallucinations(response: str, context_docs=None) -> tuple:
    urls = _extract_urls(response)
    if not urls:
        return True, ""
    known = _known_urls(context_docs) if context_docs is not None else None
    for url in urls:
        u = url.rstrip("/").lower()
        if known is not None:
            # Mode context-aware : conserve les URL présentes dans le contexte,
            # traite les autres (même tde.tg) comme hallucinations.
            if u in known:
                continue
            print("⚠️ URL non présente dans le contexte détectée")
            return False, "URL non autorisée"
        else:
            # Fallback sans contexte : seules les URL externes sont filtrées.
            if not _is_tde_url(url):
                print("⚠️ URL externe détectée")
                return False, "URL non autorisée"
    return True, ""


def _clean_hallucinations(response: str, context_docs=None) -> str:
    known = _known_urls(context_docs) if context_docs is not None else None

    def _replace(m):
        url = m.group(0)
        u = url.rstrip("/").lower()
        if known is not None:
            return url if u in known else "[information non disponible]"
        return url if _is_tde_url(url) else "[information non disponible]"

    return URL_RE.sub(_replace, response)


def _clean_formulations(response: str) -> str:
    for mot, replacement in REPLACEMENTS.items():
        response = response.replace(mot, replacement)
    return response


def _check_langue(response: str) -> bool:
    """Vérifie raisonnablement qu'une réponse est compatible avec le français.

    Heuristique locale robuste basée sur plusieurs signaux :
    mots-outils français, diacritiques, morphologie française (-tion, -ment...),
    ratio de tokens « français plausibles », et un garde-fou contre l'anglais
    (un texte manifestement anglais n'a ni mot-outil français ni diacritique).

    Accepte :
    - les phrases courtes (« Oui. », « Non. », « Le 8994 est gratuit. ») ;
    - les réponses essentiellement numériques / coordonnées (« +228 92 23 33 33 »,
      « 8994 », « contact@tde.tg ») ;
    - les termes techniques anglais courants dans un texte français (WhatsApp,
      email, web, PDF, TDE…) ;
    mais rejette les textes manifestement anglais.
    """
    if not response or not response.strip():
        return False

    # Tokens alphabétiques uniquement (on ignore chiffres, ponctuation, @…)
    alpha_tokens = re.findall(r"[a-zàâäéèêëîïôöùûüç]+", response.lower())

    # Réponse essentiellement numérique / coordonnée (téléphone, WhatsApp,
    # montant, email…) : pas de token alpha => aucun motif français à vérifier,
    # on accepte (le contenu factuel est valide).
    if not alpha_tokens:
        return True

    french_like = 0
    has_function_word = False
    has_diacritic = False

    for tok in alpha_tokens:
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
            french_like += 1

    ratio = french_like / len(alpha_tokens)

    # 1) Présence d'un mot-outil français => français (même phrase très courte).
    if has_function_word:
        return True
    # 2) Diacritique + au moins un autre signal (évite l'anglais accentué isolé).
    if has_diacritic and french_like >= 2:
        return True
    # 3) Peu de tokens mais porteurs d'un diacritique (ex. « Téléphone : 92 … »).
    if has_diacritic and len(alpha_tokens) <= 2:
        return True
    # 4) Assez de tokens français plausibles avec un bon ratio.
    if french_like >= 2 and ratio >= 0.5:
        return True
    return False


def validate_response(response: str, intent: str = None, context_docs: list = None) -> dict:
    """
    Validation légère — le prompt gère les règles métier principales.
    Ce module reste un filet de sécurité pour les cas extrêmes.

    `context_docs` (optionnel, rétro-compatible) : liste de chunks RAG
    {'source':..., 'text':...}. Quand il est fourni, les URL présentes dans le
    contexte sont considérées comme valides et les autres URL (même tde.tg) sont
    traitées comme hallucinations. En son absence, seules les URL externes
    (hors domaine TdE) sont filtrées.
    """
    if not response or not response.strip():
        return {"valid": False, "response": None,
                "use_fallback": True, "reason": "Réponse vide"}

    # 1. Longueur (une réponse courte mais valide reste acceptée)
    length_ok, response = _check_length(response)
    if not length_ok:
        return {"valid": False, "response": None,
                "use_fallback": True, "reason": response}

    # 2. URLs suspectes / hallucinations
    hall_ok, reason = _check_hallucinations(response, context_docs)
    if not hall_ok:
        response = _clean_hallucinations(response, context_docs)
        print("URL nettoyée")

    # 3. Formulations non conformes
    for mot in REPLACEMENTS:
        if mot in response.lower():
            response = _clean_formulations(response)
            print("Formulation nettoyée")
            break

    # 4. Langue française
    if not _check_langue(response):
        return {"valid": False, "response": None,
                "use_fallback": True, "reason": "Réponse pas en français"}

    return {
        "valid": True,
        "response": response.strip(),
        "use_fallback": False,
        "reason": ""
    }