from sentence_transformers import SentenceTransformer
import os

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# Le modèle sera sauvegardé dans le dossier sentence_model
SAVE_PATH = os.path.dirname(__file__)

print("Téléchargement du modèle...")

model = SentenceTransformer(MODEL_NAME)

model.save(SAVE_PATH)

print(f"✅ Modèle enregistré dans : {SAVE_PATH}")