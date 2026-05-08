import csv
import re

# =========================
# 🔎 MOTS CLÉS PAR INTENT
# =========================
intent_keywords = {
    "info_tarif": ["tarif", "prix", "coût", "facture"],
    "simulation_facture": ["estimer", "simulation", "prévoir"],
    "info_generale_tde": ["tde", "rôle", "mission"],
    "demande_branchement": ["branchement", "installer", "raccordement"],
    "info_branchement": ["procédure", "étapes"],
    "suivi_demande_branchement": ["statut", "suivi", "où en est"],
    "documents_branchement": ["documents", "pièces", "dossier"],
    "documents_resiliation": ["résiliation", "arrêter contrat"],
    "documents_reabonnement": ["réabonnement", "réactiver"],
    "documents_generaux": ["documents", "administratif"],
    "demande_document": ["document", "justificatif"],
    "info_reabonnement": ["remettre eau", "réactiver compteur"],
    "resiliation": ["résilier", "arrêter abonnement"],
    "modification_abonnement": ["modifier", "changer nom"],
    "reclamation_facture": ["facture", "erreur", "élevée"],
    "signaler_coupure": ["pas d’eau", "coupure"],
    "signaler_basse_pression": ["faible pression"],
    "signaler_fuite": ["fuite", "cassée"],
    "signaler_eau_sale": ["sale", "trouble"],
    "zone_couverture": ["zone", "quartier"],
    "eligibilite_branchement": ["éligible", "avoir eau"],
    "conseil_consommation": ["économiser", "réduire"],
    "info_consommation_moyenne": ["consommation moyenne"],
    "contact_service_client": ["numéro", "contacter"],
    "horaire_agence": ["heure", "horaire", "ouvrir"],
    "fallback": ["je comprends pas", "hein"]
}

# =========================
# 🧹 CLEAN TEXT
# =========================
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\sàéèùâêîôûç]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# =========================
# 🔍 DETECT INTENT (approx)
# =========================
def detect_intent(text):
    scores = {}

    for intent, keywords in intent_keywords.items():
        score = 0
        for kw in keywords:
            if kw in text:
                score += 1
        scores[intent] = score

    best_intent = max(scores, key=scores.get)
    return best_intent, scores[best_intent]

# =========================
# ⚠️ MULTI-INTENT DETECTION
# =========================
def is_ambiguous(text):
    return " et " in text or " aussi " in text

# =========================
# 🚀 CORRECTION DATASET
# =========================
def correct_dataset(input_file, output_file):
    corrected = []
    skipped = []

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            text = clean_text(row["text"])
            label = row["intent"]

            # 🔍 détecter incohérence
            predicted_intent, score = detect_intent(text)

            # ⚠️ ambigu
            if is_ambiguous(text):
                skipped.append((text, label))
                continue

            # ⚠️ incohérence
            if predicted_intent != label and score > 0:
                label = predicted_intent  # correction auto

            corrected.append((text, label))

    # 💾 save
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "intent"])
        writer.writerows(corrected)

    print(f"✅ Corrigé : {len(corrected)}")
    print(f"⚠️ Ambigus ignorés : {len(skipped)}")

# =========================
# ▶️ RUN
# =========================
correct_dataset("dataset_last.csv", "dataset_clean.csv")

