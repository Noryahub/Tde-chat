import re
import unicodedata
from collections import Counter

import numpy as np
from backend.app.rag.indexer import load_index, embedder

# Ne pas charger au démarrage — chargement à la première requête
_index = None
_chunks = None

# Taille du pool de candidats récupérés via FAISS (dense).
# Le reranking hybride s'applique ensuite sur ce pool.
CANDIDATE_K = 50

# Mots-outils français/anglais retirés du calcul de recouvrement lexical
# pour ne garder que les termes porteurs de sens.
STOPWORDS = {
    "le", "la", "les", "un", "une", "des", "du", "de", "et", "ou", "que", "qui",
    "ce", "cette", "je", "tu", "il", "elle", "nous", "vous", "ils", "elles",
    "est", "sont", "a", "ont", "pour", "par", "sur", "avec", "dans", "en", "au",
    "aux", "pas", "plus", "ne", "se", "sa", "son", "ses", "leur", "leurs", "mon",
    "ton", "ma", "ce", "cet", "chez", "vers", "sans", "sous", "entre", "apres",
    "avant", "pendant", "comme", "mais", "donc", "car", "si", "quand", "comment",
    "ou", "pourquoi", "quel", "quelle", "notre", "votre", "leur", "meme", "tout",
    "tous", "toute", "chaque", "ici", "y", "comment", "faire", "trouver", "ou",
    "the", "a", "an", "of", "to", "in", "is", "are", "for", "with", "on", "at",
    "by", "this", "that", "it", "and", "or", "how", "what", "why", "where",
    "when", "can", "do", "you", "i", "my", "your",
}

# Vocabulaire procédural/informatif générique (TDE) - catégories multiples.
PROCEDURAL_TERMS = {
    "branchement", "abonnement", "facture", "factures", "paiement", "payer",
    "agence", "agences", "horaire", "horaires", "fuite", "fuites", "consommation",
    "resiliation", "résiliation", "reclamation", "réclamation", "demande",
    "dossier", "piece", "pièces", "pieces", "document", "documents", "formulaire",
    "plan", "masse", "geometre", "géomètre", "delai", "délai", "procedure",
    "procédure", "etape", "étape", "étapes", "realisation", "réalisation",
    "constituer", "fournir", "necessaire", "nécessaire", "requis", "tarif",
    "tarifs", "cout", "coût", "montant", "inscription", "depense", "dépense",
    "compteur", "compteurs", "eau", "potable", "signalement", "devis",
}

# Marqueurs de navigation / boilerplate forts et non ambigus.
# On évite les termes vagues (ex. "contactez", "menu") qui apparaissent
# légitimement dans du contenu informatif.
NAV_STRONG = (
    "voir +", "lire +", "plan du site", "mentions légales",
    "mentions legales", "espace client", "espaceclient", "accueil",
)

# Expansion de requête générique par thématique TDE (dictionnaire de synonymes
# métier). Permet de rapprocher dans l'espace dense les pages dédiées (ex.
# infos-branchement) qui contiennent le vocabulaire procédural associé, sans
# cibler un document précis. S'applique à toutes les thématiques.
TOPIC_EXPANSION = {
    "branchement": ["dossier", "pieces", "piece", "formulaire", "plan", "masse",
                    "geometre", "delai", "procedure", "cout", "realisation",
                    "constituer", "demande", "document"],
    "abonnement": ["dossier", "piece", "formulaire", "demande", "inscription",
                   "documents", "contrat"],
    "facture": ["paiement", "echeance", "montant", "reglement", "moyen", "compteur"],
    "paiement": ["facture", "caisse", "agence", "moyen", "reglement", "echeance"],
    "fuite": ["fuite", "urgence", "contact", "service", "client", "incident"],
    "agence": ["agence", "horaire", "adresse", "localisation", "proche", "accueil"],
    "consommation": ["eau", "economie", "reduire", "gaspillage", "economiser"],
    "resiliation": ["resiliation", "dossier", "demande", "contrat"],
    "reclamation": ["reclamation", "incident", "signalement", "contact", "client"],
    "devis": ["branchement", "cout", "tarif", "montant", "etude"],
    "compteur": ["compteur", "vol", "deplacement", "change", "panne"],
    # Concepts de contact / coordonnées (génériques, sans aucun numéro codé en dur)
    "whatsapp": ["whatsapp", "contact", "telephone", "numero"],
    "telephone": ["telephone", "contact", "numero", "whatsapp", "adresse"],
    "numero": ["numero", "contact", "telephone", "whatsapp", "adresse", "email", "horaires"],
    "vert": ["numero", "contact", "telephone"],
    "contact": ["contact", "telephone", "whatsapp", "adresse", "email", "horaires", "numero"],
    "adresse": ["adresse", "contact", "telephone", "email"],
    "email": ["email", "contact", "adresse"],
    "horaires": ["horaires", "contact", "telephone", "adresse"],
}


def _ensure_loaded():
    global _index, _chunks
    if _index is None:
        _index, _chunks = load_index()


def _normalize_source(src: str) -> str:
    if not src:
        return ""
    s = src.strip().lower()
    s = s.split("#")[0].split("?")[0]
    s = re.sub(r"^https?://", "", s)
    s = s.rstrip("/")
    return s


def _strip_accents(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def _tokenize(text: str) -> list:
    text = _strip_accents(text.lower())
    return [t for t in re.findall(r"[a-z0-9]+", text) if len(t) > 2]


def _dense_scores(distances: list) -> np.ndarray:
    d = np.array(distances, dtype=float)
    mn, mx = d.min(), d.max()
    if mx - mn < 1e-9:
        return np.full_like(d, 0.5)
    # distance L2 décroissante → similarité croissante
    return (mx - d) / (mx - mn)


def _lexical_score(query_content_tokens: list, chunk_token_set: set) -> float:
    if not query_content_tokens:
        return 0.0
    q = set(query_content_tokens)
    hits = sum(1 for t in q if t in chunk_token_set)
    return hits / len(q)


def _procedural_score(chunk_tokens: list) -> float:
    hits = sum(1 for t in set(chunk_tokens) if t in PROCEDURAL_TERMS)
    if not chunk_tokens:
        return 0.0
    return min(1.0, hits / 4.0)


def _boilerplate_penalty(text_lower: str) -> float:
    penalty = 0.0
    # liens "Voir +" / "Lire +" : signaux de navigation répétée
    penalty += 0.30 * text_lower.count("voir +")
    penalty += 0.30 * text_lower.count("lire +")
    for m in ("plan du site", "mentions légales", "mentions legales",
              "espace client", "espaceclient", "accueil"):
        if m in text_lower:
            penalty += 0.20
    return min(0.6, penalty)


# ---------------------------------------------------------------------------
# Signal FACTUEL : détection de coordonnées / informations de contact dans un
# chunk. Ce signal ne favorise un chunk factuel QUE lorsque la requête demande
# ce type d'information (gated par les drapeaux de requête ci-dessous), afin de
# ne pas attirer un footer de contact vers une requête de branchement.
# ---------------------------------------------------------------------------
_PHONE_RE = re.compile(r"\d{2}[\s]?\d{2}[\s]?\d{2}[\s]?\d{2}")
_EMAIL_RE = re.compile(r"[\w.\-]+@[\w.\-]+")


def _chunk_factual_flags(text_lower: str) -> dict:
    # Normalisation des accents pour les comparaisons de sous-chaînes
    # (ex. "Numéro Vert" -> "numero vert").
    tl = _strip_accents(text_lower)
    return {
        "whatsapp": "whatsapp" in text_lower,
        "phone": bool(_PHONE_RE.search(text_lower))
                 or "telephone" in text_lower
                 or "numero" in text_lower,
        "numero_vert": "numero vert" in tl,
        "email": bool(_EMAIL_RE.search(text_lower)),
        "url": "http" in text_lower,
        "tde_url": "tde.tg" in text_lower,
        "adresse": "adresse" in text_lower,
        "horaires": "horaires" in text_lower or "heures d" in text_lower,
    }


def _query_contact_flags(q_tokens: list) -> dict:
    return {
        "whatsapp": "whatsapp" in q_tokens,
        "phone": "telephone" in q_tokens or "numero" in q_tokens,
        "numero_vert": "vert" in q_tokens,
        "contact": "contact" in q_tokens,
        "adresse": "adresse" in q_tokens,
        "email": "email" in q_tokens,
        "horaires": "horaires" in q_tokens,
    }


def _factual_score(qf: dict, ff: dict) -> float:
    # Spécificité maximale atteinte (pas une somme) : un chunk factuel précis
    # (ex. WhatsApp) doit pouvoir battre un chunk procédural long.
    s = 0.0
    if qf["whatsapp"] and ff["whatsapp"]:
        s = max(s, 1.0)
    if qf["numero_vert"] and ff["numero_vert"]:
        s = max(s, 1.0)
    if qf["phone"] and ff["phone"]:
        s = max(s, 0.6)
    if qf["email"] and ff["email"]:
        s = max(s, 0.8)
    if qf["adresse"] and ff["adresse"]:
        s = max(s, 0.6)
    if qf["horaires"] and ff["horaires"]:
        s = max(s, 0.6)
    if qf["contact"] and (ff["whatsapp"] or ff["phone"] or ff["email"]
                          or ff["tde_url"] or ff["adresse"]):
        s = max(s, 0.5)
    return s


def retrieve(query: str, top_k: int = 3) -> list[dict]:
    _ensure_loaded()

    # Index pas encore construit → retourner liste vide
    if _index is None:
        print("⚠️ Index FAISS non disponible — RAG désactivé")
        return []

    query_embedding = embedder.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    # Expansion de requête (générique, par thématique) pour rapprocher les
    # pages dédiées dans l'espace dense. N'altère pas le contrat de retour.
    q_tokens = _tokenize(query)
    expansion = []
    for tok in q_tokens:
        if tok in TOPIC_EXPANSION:
            expansion.extend(TOPIC_EXPANSION[tok])
    if expansion:
        expanded = query + " " + " ".join(expansion)
        query_embedding = np.array(embedder.encode([expanded])).astype("float32")

    # Étape A — pool dense élargi via FAISS
    distances, indices = _index.search(query_embedding, CANDIDATE_K)

    candidates = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        chunk = _chunks[idx]
        candidates.append({
            "idx": int(idx),
            "text": chunk["text"],
            "source": chunk.get("source", ""),
            "title": chunk.get("title", ""),
            "dist": float(dist),
        })

    if not candidates:
        return []

    # Étape B — reranking hybride sur le pool
    dense = _dense_scores([c["dist"] for c in candidates])
    query_tokens = _tokenize(query)
    query_content = [t for t in query_tokens if t not in STOPWORDS]
    # Termes thématiques détectés dans la requête (ceux ayant déclenché
    # l'expansion). Sert de signal générique « la page traite bien du sujet ».
    q_topics = set(t for t in query_tokens if t in TOPIC_EXPANSION)
    # Drapeaux de contact : activent le signal factuel uniquement si la
    # requête porte sur des coordonnées (WhatsApp, téléphone, etc.).
    query_flags = _query_contact_flags(query_tokens)

    for i, c in enumerate(candidates):
        c_tokens = _tokenize(c["text"])
        c_token_set = set(c_tokens)
        c["dense"] = float(dense[i])
        c["lex"] = _lexical_score(query_content, c_token_set)
        c["proc"] = _procedural_score(c_tokens)
        c["bp"] = _boilerplate_penalty(c["text"].lower())
        # Un chunk riche en contenu informatif (proc élevé) voit sa pénalité
        # de boilerplate atténuée : on ne veut pas punir une page utile qui
        # contiendrait quelques liens de navigation.
        bp_eff = c["bp"] * (1.0 - 0.4 * c["proc"])
        # Bonus si le chunk contient réellement le terme thématique demandé
        # (ex. « agence », « branchement »). Générique, non codé sur un document.
        topic_hit = 1.0 if (q_topics & c_token_set) else 0.0
        # Signal factuel : le chunk contient-il les coordonnées demandées ?
        # Gated par query_flags => n'attire PAS un footer de contact vers une
        # requête procédurale (branchement, paiement, ...).
        factual = _factual_score(query_flags, _chunk_factual_flags(c["text"].lower()))
        c["factual"] = factual
        # score final : similarité dense + lexique + procédural + factuel - boilerplate
        # Le signal factuel (poids 0.30) permet à un chunk court contenant
        # exactement la coordonnée demandée de dépasser un long chunk
        # procédural (proc=1) qui ne répondrait pas à la question.
        c["final"] = (
            0.28 * c["dense"]
            + 0.32 * c["lex"]
            + 0.25 * c["proc"]
            + 0.10 * topic_hit
            + 0.30 * factual
            - 0.20 * bp_eff
        )

    candidates.sort(key=lambda x: x["final"], reverse=True)

    # Diversité / déduplication des sources (max 2 chunks par source normalisée)
    selected = []
    src_count = {}
    seen_text = set()
    for c in candidates:
        nsrc = _normalize_source(c["source"])
        if nsrc in src_count and src_count[nsrc] >= 2:
            continue
        if c["text"] in seen_text:
            continue
        selected.append(c)
        src_count[nsrc] = src_count.get(nsrc, 0) + 1
        seen_text.add(c["text"])
        if len(selected) >= top_k:
            break

    return [
        {
            "text": c["text"],
            "source": c["source"],
            "score": round(float(c["final"]), 4),
        }
        for c in selected
    ]
