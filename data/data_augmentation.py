import random
import re
from data_generator import intents


# =========================
# 🏷️ ENTITÉS TDE
# =========================
ENTITIES_DE = [
    "de la tde",
    "de la société togolaise des eaux"
]

ENTITIES_A = [
    "à la tde",
    "à la société togolaise des eaux"
]

ENTITIES_SIMPLE = [
    "la tde",
    "la société togolaise des eaux"
]


# =========================
# 🎯 MOTS CLÉS
# =========================
KEYWORDS_DE = [
    "prix", "tarif", "facture", "coût", "consommation"
]

KEYWORDS_A = [
    "abonnement", "souscrire", "contact", "agence", "service client"
]

KEYWORDS_SIMPLE = [
    "eau", "service"
]


# =========================
# 🔧 FONCTION PRINCIPALE
# =========================
def insert_entity_smart(sentence):
    s = sentence.lower()

    # 🚫 éviter doublons
    if "tde" in s or "société togolaise des eaux" in s:
        return sentence

    # 1️⃣ cas "de la tde"
    for kw in KEYWORDS_DE:
        if kw in s:
            entity = random.choice(ENTITIES_DE)
            return re.sub(rf"\b{kw}\b", f"{kw} {entity}", sentence, count=1, flags=re.IGNORECASE)

    # 2️⃣ cas "à la tde"
    for kw in KEYWORDS_A:
        if kw in s:
            entity = random.choice(ENTITIES_A)
            return re.sub(rf"\b{kw}\b", f"{kw} {entity}", sentence, count=1, flags=re.IGNORECASE)

    # 3️⃣ cas simple
    for kw in KEYWORDS_SIMPLE:
        if kw in s:
            entity = random.choice(ENTITIES_SIMPLE)
            return re.sub(rf"\b{kw}\b", f"{kw} {entity}", sentence, count=1, flags=re.IGNORECASE)

    # 4️⃣ fallback naturel
    entity = random.choice(ENTITIES_SIMPLE)
    return f"{sentence} concernant {entity}"


# =========================
# 🧠 ENRICHISSEMENT DATASET
# =========================
def enrich_intents(intents):
    new_intents = {}

    for intent, phrases in intents.items():

        # ⚠️ éviter biais
        if intent == "info_generale_tde":
            new_intents[intent] = phrases
            continue

        new_phrases = []

        for p in phrases:
            new_phrases.append(p)

            # ✅ seulement 50% enrichies
            if random.random() < 0.5:
                enriched = insert_entity_smart(p)
                new_phrases.append(enriched)

        new_intents[intent] = new_phrases

    return new_intents


# =========================
# 🧪 TEST
# =========================
if __name__ == "__main__":

    test_phrases = [
        "combien coûte l’eau",
        "je veux m’abonner",
        "je ne comprends pas ma facture",
        "comment contacter le service client",
        "où se trouve votre agence",
    ]

    for t in test_phrases:
        print("Original :", t)
        print("Enrichi  :", insert_entity_smart(t))
        print("-" * 40)