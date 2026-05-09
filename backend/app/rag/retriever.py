import numpy as np
from backend.app.rag.indexer import load_index, embedder

# Ne pas charger au démarrage — chargement à la première requête
_index = None
_chunks = None


def _ensure_loaded():
    global _index, _chunks
    if _index is None:
        _index, _chunks = load_index()

def retrieve(query: str, top_k: int = 3) -> list[dict]:
    _ensure_loaded()

    # Index pas encore construit → retourner liste vide
    if _index is None:
        print("⚠️ Index FAISS non disponible — RAG désactivé")
        return []

    query_embedding = embedder.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = _index.search(query_embedding, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:
            results.append({
                "text": _chunks[idx]["text"],
                "source": _chunks[idx]["source"],
                "score": float(distances[0][i])
            })

    return results