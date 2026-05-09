# backend/app/rag/build_knowledge_base.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from backend.app.rag.scraper import scrape_all
from backend.app.rag.indexer import build_index_from_docs

docs = scrape_all(force_recrawl=False)
print(f"{len(docs)} documents prêts pour l'indexation")
build_index_from_docs(docs)  # ← une seule fois