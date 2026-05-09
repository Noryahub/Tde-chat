import requests
import time
import pickle
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_URL = "https://www.tde.tg"
CRAWLED_PATH = os.path.join(os.path.dirname(__file__), "crawled_docs.pkl")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# URLs à ignorer (pas de contenu utile)
SKIP_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".zip", ".mp4"}
SKIP_KEYWORDS = ["login", "connexion", "compte", "register", "logout", "admin"]


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    # Rester sur le domaine TDE
    if parsed.netloc and parsed.netloc != "www.tde.tg":
        return False
    # Ignorer les fichiers médias
    if any(url.lower().endswith(ext) for ext in SKIP_EXTENSIONS):
        return False
    # Ignorer les pages de connexion
    if any(kw in url.lower() for kw in SKIP_KEYWORDS):
        return False
    return True


def crawl_links(start_url: str, max_pages: int = 80) -> list[str]:
    """
    Crawl récursif — collecte tous les liens internes du site TDE.
    """
    visited = set()
    to_visit = [start_url]
    all_links = []

    print(f"🔍 Crawling de {start_url}...")

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)

        if url in visited:
            continue

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code != 200:
                continue

            visited.add(url)
            all_links.append(url)
            print(f"  ✅ [{len(visited)}/{max_pages}] {url}")

            soup = BeautifulSoup(response.text, "html.parser")

            # Extraire tous les liens de la page
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"].strip()
                full_url = urljoin(BASE_URL, href)

                # Nettoyer les ancres et paramètres inutiles
                full_url = full_url.split("#")[0]

                if (
                    full_url not in visited
                    and full_url not in to_visit
                    and is_valid_url(full_url)
                    and full_url.startswith(BASE_URL)
                ):
                    to_visit.append(full_url)

            time.sleep(0.8)  # respecter le serveur

        except Exception as e:
            print(f"  ❌ Erreur {url} : {e}")
            continue

    print(f"\n📋 {len(all_links)} pages trouvées")
    return all_links


def scrape_page(url: str) -> dict:
    """Scrape le contenu texte d'une page."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Supprimer les balises inutiles
        for tag in soup(["script", "style", "nav", "footer", "header", "form"]):
            tag.decompose()

        # Extraire le titre de la page
        title = soup.title.string.strip() if soup.title else ""

        # Extraire les liens vers PDFs sur cette page
        pdf_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().endswith(".pdf"):
                pdf_links.append(urljoin(BASE_URL, href))

        # Texte principal
        text = soup.get_text(separator=" ", strip=True)
        lines = [l.strip() for l in text.splitlines() if len(l.strip()) > 40]
        clean_text = " ".join(lines)

        return {
            "url": url,
            "title": title,
            "content": clean_text,
            "pdf_links": pdf_links
        }

    except Exception as e:
        print(f"  ❌ Erreur scraping {url} : {e}")
        return {"url": url, "title": "", "content": "", "pdf_links": []}


def scrape_pdf(pdf_url: str) -> dict:
    """Extrait le texte d'un PDF depuis une URL."""
    try:
        import io
        import pdfplumber

        response = requests.get(pdf_url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        text = ""
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return {
            "url": pdf_url,
            "title": pdf_url.split("/")[-1],
            "content": text.strip(),
            "pdf_links": []
        }

    except Exception as e:
        print(f"  ❌ Erreur PDF {pdf_url} : {e}")
        return {"url": pdf_url, "title": "", "content": "", "pdf_links": []}


def scrape_all(force_recrawl: bool = False) -> list[dict]:
    """
    Pipeline complet :
    1. Crawl tous les liens du site
    2. Scrape chaque page
    3. Détecte et extrait les PDFs
    4. Sauvegarde le résultat
    """
    if os.path.exists(CRAWLED_PATH) and not force_recrawl:
        print("📦 Chargement des docs depuis le cache...")
        with open(CRAWLED_PATH, "rb") as f:
            return pickle.load(f)

    # 1. Crawl des liens
    all_links = crawl_links(BASE_URL, max_pages=80)

    # 2. Scraping de chaque page
    documents = []
    pdf_urls_found = set()

    print("\n📄 Scraping des pages...")
    for url in all_links:
        doc = scrape_page(url)
        if doc["content"]:
            documents.append(doc)
            # Collecter les PDFs trouvés
            for pdf_url in doc.get("pdf_links", []):
                pdf_urls_found.add(pdf_url)
        time.sleep(0.5)

    # 3. Extraction des PDFs
    if pdf_urls_found:
        print(f"\n📑 {len(pdf_urls_found)} PDFs trouvés — extraction en cours...")
        for pdf_url in pdf_urls_found:
            pdf_doc = scrape_pdf(pdf_url)
            if pdf_doc["content"]:
                documents.append(pdf_doc)
                print(f"  ✅ PDF extrait : {pdf_url}")

    # 4. Sauvegarde cache
    with open(CRAWLED_PATH, "wb") as f:
        pickle.dump(documents, f)

    print(f"\n✅ {len(documents)} documents collectés au total")
    return documents