import os
import re
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import warnings
warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "app",
    "models",
    "ner_model"
)

print("NER MODEL PATH =", MODEL_PATH)
print("NER DOSSIER EXISTE =", os.path.exists(MODEL_PATH))

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Modèle NER introuvable : {MODEL_PATH}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForTokenClassification.from_pretrained(MODEL_PATH, local_files_only=True)

ner_pipeline = pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"
)

SCORE_THRESHOLD = 0.70

VILLES_TOGO = [
    "agoe", "agoè", "lome", "lomé", "kara", "tokoin",
    "adidogome", "adidogomé", "tsevie", "tsévié",
    "dapaong", "sokode", "sokodé", "atakpame", "atakpamé",
    "nyekonakpoe", "be", "bè", "cacaveli", "baguida",
    "avepozo", "djidjole", "hedzranawoe", "agoenyive",
    "legbassito", "kodjoviakope", "tabligbo", "kpalime",
    "kpalimé", "mango", "bassar", "bafilo", "notse",
    "notsé", "vogan", "aneho", "aného", "djagble",
    "djagblé", "zio", "golfe", "kloto", "kozah"
]


def _fallback_ville(text: str):
    """
    Détecte une ville par correspondance de mot entier.
    Évite les faux positifs comme "be" dans "robinets".
    """
    text_lower = text.lower()
    # Extraire les mots entiers du texte
    words = set(re.findall(r'\b\w+\b', text_lower))

    for ville in VILLES_TOGO:
        ville_words = ville.split()
        if len(ville_words) == 1:
            # Ville en un mot — correspondance mot entier uniquement
            if ville in words:
                idx = text_lower.find(ville)
                return text[idx:idx + len(ville)]
        else:
            # Ville en plusieurs mots — recherche dans le texte
            if ville in text_lower:
                idx = text_lower.find(ville)
                return text[idx:idx + len(ville)]

    return None


def _is_incomplete(localisation: str) -> bool:
    """Vérifie si la localisation détectée est un fragment incomplet."""
    if not localisation:
        return True
    if len(localisation) <= 3:
        return True
    if localisation[0].islower():
        return True
    loc_lower = localisation.lower()
    for ville in VILLES_TOGO:
        if ville.startswith(loc_lower) and ville != loc_lower:
            return True
    return False


def extract_entities(text: str) -> dict:
    """
    Extrait les entités d'un texte.
    Utilise start/end pour reconstruire depuis le texte original.
    Fallback sur liste de villes (mot entier) si NER échoue.
    Retourne : { "localisation": str|None, "probleme": str|None }
    """
    raw_results = ner_pipeline(text)
    print("NER RAW :", raw_results)

    entities = {"localisation": None, "probleme": None}
    ville_spans = []
    probleme_spans = []

    for entity in raw_results:
        if entity["score"] < SCORE_THRESHOLD:
            continue

        label = entity["entity_group"]
        if label == "VILLE":
            ville_spans.append((entity["start"], entity["end"]))
        elif label == "PROBLEME":
            probleme_spans.append((entity["start"], entity["end"]))

    if ville_spans:
        entities["localisation"] = text[ville_spans[0][0]:ville_spans[-1][1]].strip()

    if probleme_spans:
        raw = text[probleme_spans[0][0]:probleme_spans[-1][1]].strip()
        entities["probleme"] = raw.replace(" '", "'").replace("' ", "'")

    # Fallback si localisation absente ou fragment incomplet
    if _is_incomplete(entities["localisation"]):
        fallback = _fallback_ville(text)
        if fallback:
            print(f"NER FALLBACK VILLE : {fallback} (remplace '{entities['localisation']}')")
            entities["localisation"] = fallback
        else:
            entities["localisation"] = None

    print("NER ENTITES :", entities)
    return entities


# =========================================
# TESTS
# =========================================
if __name__ == "__main__":
    tests = [
        "fuite à Agoè",
        "coupure d'eau à Tokoin",
        "eau sale vers Kara",
        "plus d'eau à Adidogomé",
        "basse pression à Lomé",
        "tuyau cassé à Nyekonakpoe",
        "je veux signaler une fuite à Kara",
        "bonjour il y a une fuite à Bè",
        "je suis à Agoè",
        "j'habite à Adidogomé",
        "suis-je éligible au branchement à Adidogomé ?",
        "bonjour je voudrais des informations",
        "quels sont vos horaires ?",
        #Nouveaux tests anti-faux positifs
        "depuis hier nuit l'eau ne sort plus de nos robinets",
        "comment résoudre ce problème de pression ?",
        "je voudrais savoir les tarifs",
    ]

    print("\n" + "=" * 50)
    print("TESTS NER — TDE CHATBOT")
    print("=" * 50)

    for text in tests:
        print(f"\TEXT : {text}")
        result = extract_entities(text)
        print(f"LOCALISATION : {result['localisation'] or '—'}")
        print(f"PROBLEME     : {result['probleme'] or '—'}")