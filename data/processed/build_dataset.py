# ==========================================
# build_dataset.py
# Build Dataset HuggingFace NER
# ==========================================

from datasets import Dataset
from datasets import DatasetDict

import os
import json
import random

from data.ner_data_generator import generate_dataset

# ==========================================
# LABELS
# ==========================================

LABELS = {

    0: "O",

    1: "B-PROBLEME",
    2: "I-PROBLEME",

    3: "B-VILLE",
    4: "I-VILLE",
}

# ==========================================
# SAVE JSONL
# ==========================================

def save_jsonl(data, filepath):

    with open(filepath, "w", encoding="utf-8") as f:

        for sample in data:

            f.write(
                json.dumps(
                    sample,
                    ensure_ascii=False
                ) + "\n"
            )

# ==========================================
# BUILD DATASET
# ==========================================

def build_dataset(

        n_samples=5000,

        save_path="data/processed/ner_tde_dataset"

):

    # ======================================
    # GENERATION
    # ======================================

    print("🚀 Génération dataset...")

    data = generate_dataset(n_samples)

    random.shuffle(data)

    # ======================================
    # SPLIT
    # ======================================

    split_index = int(len(data) * 0.9)

    train_data = data[:split_index]

    test_data = data[split_index:]

    # ======================================
    # HF DATASET
    # ======================================

    dataset = DatasetDict({

        "train": Dataset.from_list(train_data),

        "test": Dataset.from_list(test_data),
    })

    # ======================================
    # SAVE
    # ======================================

    os.makedirs(save_path, exist_ok=True)

    dataset.save_to_disk(save_path)

    print("✅ HuggingFace Dataset sauvegardé")

    # ======================================
    # JSONL
    # ======================================

    train_json = os.path.join(
        save_path,
        "train.jsonl"
    )

    test_json = os.path.join(
        save_path,
        "test.jsonl"
    )

    save_jsonl(train_data, train_json)

    save_jsonl(test_data, test_json)

    print(f"✅ JSONL sauvegardé : {train_json}")
    print(f"✅ JSONL sauvegardé : {test_json}")

    # ======================================
    # LABELS JSON
    # ======================================

    labels_path = os.path.join(
        save_path,
        "labels.json"
    )

    with open(labels_path, "w", encoding="utf-8") as f:

        json.dump(
            LABELS,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(f"✅ Labels sauvegardés : {labels_path}")

    # ======================================
    # STATS
    # ======================================

    print("\n========================")
    print(dataset)

    print("\n🔍 EXEMPLES\n")

    for sample in random.sample(train_data, 5):

        print("------------------")

        print(sample)

    return dataset

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    build_dataset(
        n_samples=5000
    )