"""
Search module for the Q&A agent.
Provides functionality to search the web using DuckDuckGo.
"""

from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_duckduckgo(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Search DuckDuckGo for the given query and return results.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
        
    Returns:
        List of search result dictionaries with title, body, and href
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return results
    except Exception as e:
        logger.error(f"DuckDuckGo search error: {e}")
        return []

def format_search_results(results: List[Dict[str, str]]) -> List[str]:
    """
    Format search results into a list of readable strings.
    
    Args:
        results: List of search result dictionaries
        
    Returns:
        List of formatted search result strings
    """
    formatted_results = []
    for r in results:
        formatted = f"Title: {r.get('title', 'No title')}\n"
        formatted += f"Content: {r.get('body', 'No content')}\n"
        formatted += f"URL: {r.get('href', 'No URL')}"
        formatted_results.append(formatted)
    return formatted_results

def fetch_webpage_content(url: str, max_length: int = 1000) -> Optional[str]:
    """
    Fetch and extract the main content from a webpage.
    
    Args:
        url: The URL to fetch
        max_length: Maximum length of content to return
        
    Returns:
        Extracted text content or None if failed
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        
        # Get text
        text = soup.get_text(separator='\n')
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Truncate if needed
        if len(text) > max_length:
            text = text[:max_length] + "..."
            
        return text
    except Exception as e:
        logger.error(f"Error fetching webpage content from {url}: {e}")
        return None

def research_question(question: str, max_results: int = 3, fetch_content: bool = False) -> List[str]:
    """
    Research a question by searching DuckDuckGo and optionally fetching webpage content.
    
    Args:
        question: The question to research
        max_results: Maximum number of search results to return
        fetch_content: Whether to fetch and include webpage content
        
    Returns:
        List of research results as formatted strings
    """
    # Search DuckDuckGo
    search_results = search_duckduckgo(question, max_results)
    
    if not search_results:
        logger.warning(f"No search results found for question: {question}")
        return []
    
    # If fetch_content is True, fetch and add webpage content
    if fetch_content:
        for result in search_results:
            url = result.get('href')
            if url:
                content = fetch_webpage_content(url)
                if content:
                    result['webpage_content'] = content
    
    # Format the results
    return format_search_results(search_results)

if __name__ == "__main__":
    # Test the search functionality
    test_question = "What is the capital of France?"
    results = research_question(test_question)
    print(f"Research results for: {test_question}")
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:\n{result}")
