import re
from collections import Counter
from data_generator import intents


# =========================
# 🔧 CONFIG
# =========================
TDE_PATTERNS = [
    r"\btde\b",
    r"soci[eé]t[eé]\s+togolaise\s+des\s+eaux"
]

STOPWORDS = {
    "le", "la", "les", "de", "des", "du", "un", "une",
    "je", "tu", "il", "elle", "nous", "vous",
    "est", "suis", "es", "sont",
    "quoi", "comment", "pourquoi", "svp", "bonjour", "bonsoir"
}


# =========================
# 🧠 UTILS
# =========================
def contains_tde(text):
    text = text.lower()
    return any(re.search(p, text) for p in TDE_PATTERNS)


def tokenize(text):
    tokens = re.findall(r"\b\w+\b", text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]


# =========================
# 📊 ANALYSE TDE
# =========================
def analyze_tde_distribution(data):
    print("\n📊 DISTRIBUTION 'TDE'\n")

    for intent, phrases in data.items():
        phrases = [p for p in phrases if p.strip()]

        total = len(phrases)
        with_tde = sum(1 for p in phrases if contains_tde(p))
        ratio = with_tde / total if total > 0 else 0

        print(intent)
        print(f"  total : {total}")
        print(f"  avec TDE : {with_tde}")
        print(f"  ratio : {ratio:.2f}")
        print("-" * 40)


# =========================
# 🚨 DETECTION BIAIS
# =========================
def detect_bias(data):
    print("\n🚨 MOTS DOMINANTS (BIAIS)\n")

    intent_word_counts = {}
    global_counts = Counter()

    for intent, phrases in data.items():
        words = []

        for p in phrases:
            if not p.strip():
                continue
            words.extend(tokenize(p))

        counter = Counter(words)
        intent_word_counts[intent] = counter
        global_counts.update(counter)

    for intent, counter in intent_word_counts.items():
        print(f"\n🔹 {intent}")

        for word, count in counter.most_common(8):
            global_freq = global_counts[word]
            dominance = count / global_freq if global_freq > 0 else 0

            if dominance >= 0.6:
                print(f"   ⚠️ {word} → biais ({dominance:.2f})")
            else:
                print(f"   {word} ({count})")


# =========================
# 🚀 LANCEMENT
# =========================
if __name__ == "__main__":
    print("🚀 Analyse dataset en cours...")

    analyze_tde_distribution(intents)
    detect_bias(intents)

    print("\n✅ Analyse terminée")