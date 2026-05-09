import os
import torch

from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

# Racine projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Chemin réel du modèle
MODEL_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "app",
    "models",
    "intent_model"
)

print("MODEL PATH =", MODEL_PATH)
print("DOSSIER EXISTE =", os.path.exists(MODEL_PATH))

# Vérification
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Modèle introuvable : {MODEL_PATH}")

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

# Modèle
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

model.eval()

def process_predict(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=64
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.nn.functional.softmax(outputs.logits, dim=1)

    predicted_class = torch.argmax(probs, dim=1).item()

    confidence = probs[0][predicted_class].item()

    label = model.config.id2label[predicted_class]

    return {
        "intent": label,
        "confidence": round(confidence, 3)
    }
# Après le chargement du modèle
# Remplace le bloc MAPPING_PATH par ceci
model.config.id2label = {
    0:  "conseil_consommation",
    1:  "contact_service_client",
    2:  "demande_branchement",
    3:  "demande_documents",
    4:  "eligibilite_branchement",
    5:  "fallback",
    6:  "gestion_abonnement",
    7:  "gestion_facture",
    8:  "horaire_agence",
    9:  "info_branchement",
    10: "info_consommation",
    11: "info_generale",
    12: "info_tarif",
    13: "signaler_probleme",
    14: "suivi_branchement",
    15: "zone_couverture"
}
model.config.label2id = {v: k for k, v in model.config.id2label.items()}
print("Mapping chargé :", model.config.id2label)
print("ID2LABEL :", model.config.id2label)