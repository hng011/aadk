from . import settings
import requests
from bs4 import BeautifulSoup
from google.adk.tools import FunctionTool


def search_paper(domain: str, limit: int = 3):
    """Fetches latest or specific number of paper requested by user  from arXiv for the given domain.

    Args:
        domain (str): _description_
        limit (int, optional): _description_. Defaults to 3.
        
    Returns:
        List of papers that successfully fetched
    """
    
    if limit > settings.MAXIMUM_PAPER:
        return f"Limit to {settings.MAXIMUM_PAPER} papers for each request"
    
    url = f"https://arxiv.org/search/?query={domain}&searchtype=all&abstracts=show&order=-announced_date_first&size=50"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    papers = soup.find_all("li", class_="arxiv-result")[:limit]

    for paper in papers:
        title = paper.find("p", class_="title").text.strip()
        authors = paper.find("p", class_="authors").text.strip().replace("Authors:", "").strip()
        abstract = paper.find("span", class_="abstract-full").text.strip().replace("\n", " ")
        source_url = paper.find("p", class_="list-title").find("a")["href"]
        pdf_url = paper.find("p", class_="list-title").find("span").find("a")["href"]

        results.append({
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "source_url": source_url,
            "pdf_url": pdf_url
        })
            
    return results


search_paper = FunctionTool(search_paper)