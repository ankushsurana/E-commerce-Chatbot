import logging
from typing import List, Dict, Optional
from duckduckgo_search import DDGS
from config.config import config


SAFE_SEARCH_BLACKLIST = [ 
    "gambling", "betting",
    "violence", "gore", "kill", "murder",
    "hack", "crack", "warez",
    "drug", "cocaine", "heroin",
    "dating", "escort"
]   

def is_safe_content(text: str) -> bool:
    if not text:
        return True
        
    text_lower = text.lower()
    for keyword in SAFE_SEARCH_BLACKLIST:
        if keyword in text_lower:
            return False
    return True

def search_web(query: str, max_results: int = None, timeout: int = None) -> List[Dict[str, str]]:
    logger = logging.getLogger(__name__)
    
    if max_results is None:
        max_results = config.MAX_SEARCH_RESULTS
    if timeout is None:
        timeout = config.SEARCH_TIMEOUT
    
    try:
        logger.info(f"Performing web search for: {query}")
        
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query,
                max_results=max_results * 2,
                timelimit=None,
                safesearch='on' 
            ))
        
        formatted_results = []
        blocked_count = 0
        
        for result in results:
            if len(formatted_results) >= max_results:
                break
                
            title = result.get('title', 'No title')
            link = result.get('href', '')
            snippet = result.get('body', 'No description')
            
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
