from langchain.tools import tool 
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re 


load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
    results = tavily.search(query=query,max_results=5)

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    
    return "\n----\n".join(out)

   
    

@tool
def scrape_url(url: str) -> str:
    """
    Scrape and extract clean readable content from a URL.
    Uses multiple extraction strategies for better reliability.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    try:
        # ── Fetch page ─────────────────────────────────────
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        html = response.text

        # ──────────────────────────────────────────────────
        # Strategy 1 → trafilatura (BEST for articles/blogs)
        # ──────────────────────────────────────────────────
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False
        )

        if extracted and len(extracted.strip()) > 200:
            cleaned = re.sub(r'\s+', ' ', extracted)
            return cleaned[:5000]

        # ──────────────────────────────────────────────────
        # Strategy 2 → readability
        # ──────────────────────────────────────────────────
        doc = Document(html)
        clean_html = doc.summary()

        soup = BeautifulSoup(clean_html, "html.parser")

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        if text and len(text.strip()) > 200:
            cleaned = re.sub(r'\s+', ' ', text)
            return cleaned[:5000]

        # ──────────────────────────────────────────────────
        # Strategy 3 → fallback full page extraction
        # ──────────────────────────────────────────────────
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        cleaned = re.sub(r'\s+', ' ', text)

        if cleaned:
            return cleaned[:5000]

        return "Could not extract meaningful content from the page."

    except requests.exceptions.Timeout:
        return "Request timed out while scraping the URL."

    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {str(e)}"

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"


# ──────────────────────────────────────────────────────
# Quick manual test for both tools
# Run:  python multi-agent-researcher/src/tools/tools.py
# ──────────────────────────────────────────────────────
# if __name__ == "__main__":
#     print("\n=== TEST 1: web_search ===")
#     query = "latest developments in AI agents 2026"
#     print(f"Query: {query}\n")
#     try:
#         search_result = web_search.invoke({"query": query})
#         print(search_result)
#         print(f"\n[web_search returned {len(search_result)} characters]")
#     except Exception as e:
#         print(f"[web_search FAILED] {type(e).__name__}: {e}")

#     print("\n=== TEST 2: scrape_url (valid page) ===")
#     url = "https://www.python.org/about/"
#     print(f"URL: {url}\n")
#     try:
#         scrape_result = scrape_url.invoke({"url": url})
#         print(scrape_result[:1000])
#         print(f"\n[scrape_url returned {len(scrape_result)} characters]")
#     except Exception as e:
#         print(f"[scrape_url FAILED] {type(e).__name__}: {e}")

#     print("\n=== TEST 2b: scrape_url (error handling) ===")
#     bad_url = "https://httpbin.org/status/404"
#     print(f"URL: {bad_url}\n")
#     try:
#         print(scrape_url.invoke({"url": bad_url}))
#     except Exception as e:
#         print(f"[scrape_url FAILED] {type(e).__name__}: {e}")


