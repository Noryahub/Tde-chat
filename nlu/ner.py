import os

from transformers import AutoTokenizer
from transformers import AutoModelForTokenClassification
from transformers import pipeline

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "app",
    "models",
    "ner_model"
)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

model = AutoModelForTokenClassification.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

ner_pipeline = pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"
)

def extract_entities(text):
    return ner_pipeline(text)