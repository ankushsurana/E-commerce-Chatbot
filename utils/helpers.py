import re
from typing import Optional
import logging
from config.config import config

logger = logging.getLogger(__name__)


def contextualize_query(query: str, history: list, llm_client) -> str:
    """
    Rewrite query to be standalone based on chat history
    
    Args:
        query: Current user query
        history: Chat history list
        llm_client: LLM client instance
        
    Returns:
        Contextualized query
    """
    if not history or not llm_client:
        return query
        
    try:
        recent_history = history[-6:] if len(history) > 6 else history
        
        history_str = ""
        for msg in recent_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role != "system":
                history_str += f"{role}: {content}\n"
        
        if not history_str:
            return query

        messages = [
            {
                "role": "system",
                "content": """You are a query contextualization assistant.
Rewrite the user's latest query to be a standalone question that can be understood without the chat history.
Replace pronouns (it, they, this) with specific entities from the history.
Do NOT answer the question. ONLY output the rewritten query.
If the query is already standalone, output it exactly as is."""
            },
            {
                "role": "user",
                "content": f"Chat History:\n{history_str}\n\nLatest Query: {query}\n\nStandalone Query:"
            }
        ]
        
        contextualized = llm_client.generate_response(
            messages, 
            temperature=config.CONTEXTUALIZATION_TEMPERATURE, 
            max_tokens=config.CONTEXTUALIZATION_MAX_TOKENS
        )
        logger.info(f"Contextualized: '{query}' -> '{contextualized}'")
        return contextualized.strip()
        
    except Exception as e:
        logger.warning(f"Contextualization failed: {str(e)}")
        return query


def refine_query(query: str, llm_client=None) -> str:
    try:
        if not llm_client:
            return query
            
        messages = [
            {
                "role": "system", 
                "content": "You are a query refinement assistant. Your task is to correct spelling and grammar mistakes in the user's query and output ONLY the corrected version. Do not add any explanations or extra text. Keep the intent exactly the same."
            },
            {
                "role": "user", 
                "content": query
            }
        ]
        
        refined_query = llm_client.generate_response(
            messages, 
            temperature=config.REFINEMENT_TEMPERATURE, 
            max_tokens=config.REFINEMENT_MAX_TOKENS
        )
        
        if refined_query.lower().strip() != query.lower().strip():
            logger.info(f"Query refined: '{query}' -> '{refined_query}'")
            
        return refined_query.strip()
        
    except Exception as e:
        logger.warning(f"Query refinement failed: {str(e)}")
        return query


def format_response(response: str, mode: str = "detailed") -> str:
    response = response.strip()
    
    response = re.sub(r'\n{3,}', '\n\n', response)
    
    return response
