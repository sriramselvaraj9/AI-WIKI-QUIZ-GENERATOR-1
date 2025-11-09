"""
Simple Wikipedia scraper.
Given a Wikipedia URL, extracts the article title and the main textual content (paragraphs).
"""
from typing import Tuple
import requests
from bs4 import BeautifulSoup


def scrape_wikipedia(url: str) -> Tuple[str, str]:
    """Return (title, text) for the Wikipedia article.

    This is intentionally robust: it looks for common containers and falls back to
    extracting visible paragraphs. Optimized for speed with shorter timeouts.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Use shorter timeout and connection pooling for speed
    try:
        resp = requests.get(url, headers=headers, timeout=(5, 10), stream=False)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        raise Exception("Wikipedia request timed out. Please try again or use a different article.")
    except requests.exceptions.ConnectionError:
        raise Exception("Failed to connect to Wikipedia. Please check your internet connection.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error accessing Wikipedia: {str(e)}")

    soup = BeautifulSoup(resp.text, "html.parser")

    # Title
    title_tag = soup.find(id="firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else soup.title.string if soup.title else url

    # Content: prefer mw-parser-output used on Wikipedia
    content = ""
    container = soup.find(class_="mw-parser-output")
    if container:
        paragraphs = container.find_all("p")
    else:
        # fallback: any paragraph in article
        article = soup.find("article") or soup
        paragraphs = article.find_all("p")

    text_parts = []
    for p in paragraphs:
        txt = p.get_text(strip=True)
        if txt:
            text_parts.append(txt)

    content = "\n\n".join(text_parts)

    # Optimize content length for faster processing - limit to first 2000 chars for speed
    if len(content) > 2000:
        content = content[:2000] + "..."
    elif len(content) < 200:
        # fallback to all text but still limit length
        content = soup.get_text(separator="\n\n")[:2000]

    return title, content