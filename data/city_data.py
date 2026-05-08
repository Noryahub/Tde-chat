import random

# =========================
# LABELS
# =========================
LABELS = {
    "O": 0,
    "B-PROBLEME": 1,
    "I-PROBLEME": 2,
    "B-VILLE": 3,
    "I-VILLE": 4,
}

# =========================
# DONNÉES
# =========================
villes = [
    ["agoe"], ["tokoin"], ["adidogome"],
    ["lome"], ["kara"], ["atakpame"]
]

problemes = [
    ["fuite"],
    ["eau", "sale"],
    ["coupure"],
    ["basse", "pression"],
    ["plus", "d'eau"],
    ["tuyau", "cassé"]
]

prefixes = [
    ["je", "veux", "signaler"],
    ["svp"],
    ["urgent"],
    ["bonjour"],
    []
]

connecteurs = [
    ["à"],
    ["dans"],
    ["au", "niveau", "de"]
]

contextes = [
    ["il", "y", "a"],
    ["j'ai"],
    ["on", "constate"],
    []
]

suffixes = [
    [],
    ["svp"],
    ["urgent"],
    ["merci"]
]

# =========================
# BRUIT UTILISATEUR
# =========================
def add_noise(tokens, prob=0.15):
    noisy = []
    for t in tokens:
        if random.random() < prob and len(t) > 3:
            t = t[:-1]  # faute légère réaliste
        noisy.append(t)
    return noisy

# =========================
# TAGGING
# =========================
def tag_sequence(tokens, entity_tokens, label_b, label_i):
    tags = ["O"] * len(tokens)

    for i in range(len(tokens)):
        if tokens[i:i+len(entity_tokens)] == entity_tokens:
            tags[i] = label_b
            for j in range(1, len(entity_tokens)):
                tags[i+j] = label_i

    return tags

def merge_tags(base, new):
    return [n if n != "O" else b for b, n in zip(base, new)]

# =========================
# GENERATION SAMPLE
# =========================
def generate_sample():

    ville = random.choice(villes)
    prob = random.choice(problemes)

    prefix = random.choice(prefixes)
    contexte = random.choice(contextes)
    connecteur = random.choice(connecteurs)
    suffix = random.choice(suffixes)

    structure = random.choice([
        "classic",
        "ville_first",
        "probleme_first",
        "natural",
        "mix"
    ])

    if structure == "classic":
        tokens = prefix + prob + connecteur + ville + suffix

    elif structure == "ville_first":
        tokens = connecteur + ville + contexte + prob + suffix

    elif structure == "probleme_first":
        tokens = prob + connecteur + ville + suffix

    elif structure == "natural":
        tokens = contexte + prob + connecteur + ville + suffix

    else:  # mix
        tokens = prefix + connecteur + ville + ["il", "y", "a"] + prob + suffix

    tokens = [t for t in tokens if t]

    # =========================
    # TAGGING AVANT BRUIT
    # =========================
    tags = ["O"] * len(tokens)

    tags = merge_tags(tags, tag_sequence(tokens, prob, "B-PROBLEME", "I-PROBLEME"))
    tags = merge_tags(tags, tag_sequence(tokens, ville, "B-VILLE", "I-VILLE"))

    # =========================
    # BRUIT (30% des cas)
    # =========================
    if random.random() < 0.3:
        tokens = add_noise(tokens, prob=0.15)

    tags_ids = [LABELS[t] for t in tags]

    return {
        "tokens": tokens,
        "ner_tags": tags_ids
    }

# =========================
# GENERATE DATASET
# =========================
def generate_dataset(n=3000):
    return [generate_sample() for _ in range(n)]