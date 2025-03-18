import requests
from bs4 import BeautifulSoup
from llm import summarize_text

def scrape_website(query):
    """Fetches and extracts text content from a given website URL."""
    url = "https://www.sutherlandglobal.com/about-us/leadership/dilip-vellodi"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        raw_text = soup.get_text()[:2000]  
        print(raw_text)
        return summarize_text(raw_text, query)
    except requests.RequestException as e:
        return f"Failed to fetch website content: {e}"
