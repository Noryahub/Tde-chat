import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

INDEX_PATH = os.path.join(os.path.dirname(__file__), "faiss_index.bin")
CHUNKS_PATH = os.path.join(os.path.dirname(__file__), "chunks.pkl")

embedder = SentenceTransformer(EMBED_MODEL)


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def build_index_from_docs(documents: list[dict]):
    """
    Reçoit la liste de docs de scrape_all()
    et construit l'index FAISS.
    """
    all_chunks = []
    for doc in documents:
        if not doc["content"]:
            continue
        chunks = chunk_text(doc["content"])
        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "source": doc["url"],
                "title": doc.get("title", "")
            })

    print(f"📦 {len(all_chunks)} chunks créés")

    texts = [c["text"] for c in all_chunks]
    print("⚙️ Calcul des embeddings...")
    embeddings = embedder.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(all_chunks, f)

    print(f"✅ Index FAISS sauvegardé ({index.ntotal} vecteurs)")




def load_index():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNKS_PATH):
        print("⚠️ Index FAISS introuvable — lance build_knowledge_base.py d'abord.")
        return None, None          # ← retourne None au lieu de crasher

    index = faiss.read_index(INDEX_PATH)
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

    print(f"✅ Index chargé — {index.ntotal} vecteurs")
    return index, chunks