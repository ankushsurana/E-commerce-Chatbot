"""
Web Search Integration Module
Provides live web search capability using DuckDuckGo with STRICT safety filters.
"""

import logging
from typing import List, Dict, Optional
from duckduckgo_search import DDGS

# Security: Blacklist for filtering inappropriate content
SAFE_SEARCH_BLACKLIST = [
    "porn", "xxx", "sex", "adult", "nude", "erotic", "hentai", 
    "gambling", "casino", "betting",
    "violence", "gore", "kill", "murder",
    "hack", "crack", "warez",
    "drug", "cocaine", "heroin",
    "dating", "escort"
]

def is_safe_content(text: str) -> bool:
    """
    Check if text contains inappropriate content based on blacklist
    
    Args:
        text: Text to check (title, snippet, url)
        
    Returns:
        True if safe, False if inappropriate
    """
    if not text:
        return True
        
    text_lower = text.lower()
    for keyword in SAFE_SEARCH_BLACKLIST:
        # Check for exact word matches or clear substrings
        if keyword in text_lower:
            return False
    return True

def search_web(query: str, max_results: int = 5, timeout: int = 10) -> List[Dict[str, str]]:
    """
    Perform web search using DuckDuckGo with STRICT SafeSearch
    
    Args:
        query: Search query
        max_results: Maximum number of results to return
        timeout: Timeout in seconds
        
    Returns:
        List of search result dictionaries with 'title', 'link', 'snippet'
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Performing web search for: {query}")
        
        # Initialize DDGS client
        with DDGS() as ddgs:
            # Perform search with STRICT SafeSearch
            # safesearch='on' enforces strict filtering
            results = list(ddgs.text(
                query,
                max_results=max_results * 2, # Fetch more to allow for filtering
                timelimit=None,
                safesearch='on' 
            ))
        
        # Format and Filter results
        formatted_results = []
        blocked_count = 0
        
        for result in results:
            if len(formatted_results) >= max_results:
                break
                
            title = result.get('title', 'No title')
            link = result.get('href', '')
            snippet = result.get('body', 'No description')
            
            # Content Safety Check
            if (is_safe_content(title) and 
                is_safe_content(snippet) and 
                is_safe_content(link)):
                
                formatted_results.append({
                    'title': title,
                    'link': link,
                    'snippet': snippet
                })
            else:
                blocked_count += 1
                logger.warning(f"Blocked unsafe result: {link}")
        
        logger.info(f"Found {len(formatted_results)} safe results (Blocked: {blocked_count})")
        return formatted_results
    
    except Exception as e:
        logger.error(f"Web search error: {str(e)}")
        return []


def format_search_results(results: List[Dict[str, str]]) -> str:
    """
    Format search results into a readable string for LLM context
    
    Args:
        results: List of search result dictionaries
        
    Returns:
        Formatted string of search results
    """
    if not results:
        return "No web search results found."
    
    formatted_parts = []
    for idx, result in enumerate(results, 1):
        formatted_parts.append(
            f"{idx}. {result['title']}\n"
            f"   {result['snippet']}\n"
            f"   URL: {result['link']}"
        )
    
    return "\n\n".join(formatted_parts)


def get_web_context(query: str, max_results: int = 3) -> Optional[str]:
    """
    Get formatted web search context for a query
    
    Args:
        query: Search query
        max_results: Maximum number of results
        
    Returns:
        Formatted context string or None if search fails
    """
    logger = logging.getLogger(__name__)
    
    try:
        results = search_web(query, max_results=max_results)
        
        if not results:
            logger.warning("No web search results found")
            return None
        
        context = "Web Search Results:\n\n" + format_search_results(results)
        return context
    
    except Exception as e:
        logger.error(f"Error getting web context: {str(e)}")
        return None
