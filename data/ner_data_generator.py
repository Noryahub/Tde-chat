# ==========================================
# ner_data_generator.py
# Générateur NER avancé — TDE CHATBOT
# ==========================================

import random

# ==========================================
# LABELS BIO
# ==========================================

LABELS = {
    "O": 0,

    "B-PROBLEME": 1,
    "I-PROBLEME": 2,

    "B-VILLE": 3,
    "I-VILLE": 4,
}

# ==========================================
# VILLES / QUARTIERS
# ==========================================

VILLES = [

    ["agoe"],
    ["agoe-assiyeye"],
    ["tokoin"],
    ["tokoin", "lycee"],
    ["adidogome"],
    ["nyekonakpoe"],
    ["agbodrafo"],
    ["kara"],
    ["atakpame"],
    ["lome"],
    ["baguida"],
    ["hedzranawoe"],
]

# ==========================================
# PROBLÈMES
# ==========================================

PROBLEMES = [

    ["fuite"],
    ["tuyau", "cassé"],
    ["eau", "sale"],
    ["coupure"],
    ["coupure", "d'eau"],
    ["plus", "d'eau"],
    ["absence", "d'eau"],
    ["basse", "pression"],
    ["faible", "pression"],
    ["robinet", "sec"],
    ["eau", "marron"],
]

# ==========================================
# SYNONYMES / VARIANTES
# ==========================================

SYNONYMES_PROBLEMES = [

    ["ya", "pas", "d'eau"],
    ["eau", "coupée"],
    ["débit", "faible"],
    ["canal", "cassé"],
    ["eau", "trouble"],
]

# ==========================================
# CONTEXTE UTILISATEUR
# ==========================================

PREFIXES = [

    ["bonjour"],
    ["svp"],
    ["urgent"],
    ["aidez-moi"],
    ["s'il", "vous", "plait"],
    [],
]

CONTEXTES = [

    ["il", "y", "a"],
    ["je", "remarque"],
    ["nous", "avons"],
    ["j'ai"],
    ["on", "constate"],
    [],
]

CONNECTEURS = [

    ["à"],
    ["dans"],
    ["vers"],
    ["au", "niveau", "de"],
]

SUFFIXES = [

    [],
    ["svp"],
    ["merci"],
    ["depuis", "hier"],
    ["depuis", "ce", "matin"],
]

# ==========================================
# PHRASES SANS ENTITÉS
# ==========================================

NO_ENTITY_SENTENCES = [

    ["bonjour"],
    ["merci"],
    ["je", "veux", "des", "informations"],
    ["quels", "sont", "les", "tarifs"],
    ["je", "ne", "comprends", "pas"],
    ["pouvez-vous", "m'aider"],
]

# ==========================================
# BRUIT UTILISATEUR
# ==========================================

NOISE_MAP = {

    "eau": ["o", "d0", "eo"],
    "plus": ["plu"],
    "pression": ["presion"],
    "cassé": ["cass"],
    "bonjour": ["bjr"],
    "svp": ["stp"],
}

# ==========================================
# AJOUT BRUIT
# ==========================================

def add_noise(tokens, prob=0.10):

    noisy = []

    for token in tokens:

        if random.random() < prob:

            if token in NOISE_MAP:
                token = random.choice(NOISE_MAP[token])

            elif len(token) > 4:
                token = token[:-1]

        noisy.append(token)

    return noisy

# ==========================================
# TAGGING
# ==========================================

def tag_entity(tokens, entity_tokens, label_b, label_i):

    tags = ["O"] * len(tokens)

    for i in range(len(tokens)):

        if tokens[i:i + len(entity_tokens)] == entity_tokens:

            tags[i] = label_b

            for j in range(1, len(entity_tokens)):
                tags[i + j] = label_i

    return tags

# ==========================================
# MERGE TAGS
# ==========================================

def merge_tags(base, new):

    return [

        n if n != "O" else b

        for b, n in zip(base, new)
    ]

# ==========================================
# SAMPLE NORMAL
# ==========================================

def generate_normal_sample():

    ville = random.choice(VILLES)

    probleme = random.choice(
        PROBLEMES + SYNONYMES_PROBLEMES
    )

    prefix = random.choice(PREFIXES)

    contexte = random.choice(CONTEXTES)

    connecteur = random.choice(CONNECTEURS)

    suffix = random.choice(SUFFIXES)

    structure = random.choice([

        "classic",
        "ville_first",
        "probleme_first",
        "natural",
        "conversation",

    ])

    # ======================================
    # STRUCTURES
    # ======================================

    if structure == "classic":

        tokens = (
            prefix +
            contexte +
            probleme +
            connecteur +
            ville +
            suffix
        )

    elif structure == "ville_first":

        tokens = (
            ville +
            contexte +
            probleme +
            suffix
        )

    elif structure == "probleme_first":

        tokens = (
            probleme +
            connecteur +
            ville
        )

    elif structure == "conversation":

        tokens = (
            ["dans", "mon", "quartier"] +
            ville +
            ["nous", "avons"] +
            probleme
        )

    else:

        tokens = (
            contexte +
            probleme +
            connecteur +
            ville
        )

    tokens = [t for t in tokens if t]

    # ======================================
    # TAGS
    # ======================================

    tags = ["O"] * len(tokens)

    tags = merge_tags(
        tags,
        tag_entity(
            tokens,
            probleme,
            "B-PROBLEME",
            "I-PROBLEME"
        )
    )

    tags = merge_tags(
        tags,
        tag_entity(
            tokens,
            ville,
            "B-VILLE",
            "I-VILLE"
        )
    )

    # ======================================
    # BRUIT APRÈS TAGGING
    # IMPORTANT
    # ======================================

    if random.random() < 0.25:
        tokens = add_noise(tokens)

    return {

        "tokens": tokens,

        "ner_tags": [
            LABELS[t]
            for t in tags
        ]
    }

# ==========================================
# SAMPLE SANS ENTITÉ
# ==========================================

def generate_no_entity_sample():

    tokens = random.choice(NO_ENTITY_SENTENCES)

    return {

        "tokens": tokens,

        "ner_tags": [0] * len(tokens)
    }

# ==========================================
# MULTI ENTITÉS
# ==========================================

def generate_multi_problem_sample():

    ville = random.choice(VILLES)

    p1 = random.choice(PROBLEMES)

    p2 = random.choice(PROBLEMES)

    tokens = (
        ["bonjour"] +
        p1 +
        ["et"] +
        p2 +
        ["à"] +
        ville
    )

    tags = ["O"] * len(tokens)

    tags = merge_tags(
        tags,
        tag_entity(tokens, p1,
                   "B-PROBLEME",
                   "I-PROBLEME")
    )

    tags = merge_tags(
        tags,
        tag_entity(tokens, p2,
                   "B-PROBLEME",
                   "I-PROBLEME")
    )

    tags = merge_tags(
        tags,
        tag_entity(tokens, ville,
                   "B-VILLE",
                   "I-VILLE")
    )

    return {

        "tokens": tokens,

        "ner_tags": [
            LABELS[t]
            for t in tags
        ]
    }

# ==========================================
# DATASET FINAL
# ==========================================

def generate_dataset(n_samples=5000):

    dataset = []

    for _ in range(n_samples):

        r = random.random()

        # 70%
        if r < 0.70:
            sample = generate_normal_sample()

        # 20%
        elif r < 0.90:
            sample = generate_no_entity_sample()

        # 10%
        else:
            sample = generate_multi_problem_sample()

        dataset.append(sample)

    random.shuffle(dataset)

    return dataset


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    data = generate_dataset(20)

    for sample in data:

        print(sample)