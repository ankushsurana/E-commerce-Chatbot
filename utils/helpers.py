"""
Helper Utilities Module
Contains various helper functions for text processing and formatting
"""

import re
from typing import Optional
import logging

# Configure logger
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
        # Get last few messages for context (last 3 turns)
        recent_history = history[-6:] if len(history) > 6 else history
        
        # Format history for prompt
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
        
        contextualized = llm_client.generate_response(messages, temperature=0.1, max_tokens=100)
        logger.info(f"Contextualized: '{query}' -> '{contextualized}'")
        return contextualized.strip()
        
    except Exception as e:
        logger.warning(f"Contextualization failed: {str(e)}")
        return query


def refine_query(query: str, llm_client=None) -> str:
    """
    Refine user query using LLM to correct spelling and grammar
    and extract core intent for better RAG retrieval.
    
    Args:
        query: Original user query
        llm_client: Initialized LLMClient instance (optional)
        
    Returns:
        Refined query string
    """
    try:
        # If no LLM client provided, return original query (fallback)
        if not llm_client:
            return query
            
        # Simple refinement prompt
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
        
        # Use a low temperature for deterministic correction
        refined_query = llm_client.generate_response(messages, temperature=0.1, max_tokens=100)
        
        # Log the refinement if it changed
        if refined_query.lower().strip() != query.lower().strip():
            logger.info(f"Query refined: '{query}' -> '{refined_query}'")
            
        return refined_query.strip()
        
    except Exception as e:
        logger.warning(f"Query refinement failed: {str(e)}")
        return query


def format_response(response: str, mode: str = "detailed") -> str:
    """
    Format response based on mode
    
    Args:
        response: Raw response text
        mode: Response mode ("concise" or "detailed")
        
    Returns:
        Formatted response
    """
    # Clean up whitespace
    response = response.strip()
    
    # Remove excessive newlines
    response = re.sub(r'\n{3,}', '\n\n', response)
    
    return response


def truncate_text(text: str, max_length: int = 150, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)].strip() + suffix


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def format_sources(sources: list) -> str:
    """
    Format source citations
    
    Args:
        sources: List of source dictionaries
        
    Returns:
        Formatted sources string
    """
    if not sources:
        return ""
    
    formatted = "Sources:\n"
    for idx, source in enumerate(sources, 1):
        if isinstance(source, dict):
            source_name = source.get('source', 'Unknown')
            formatted += f"{idx}. {source_name}\n"
        else:
            formatted += f"{idx}. {source}\n"
    
    return formatted


def estimate_tokens(text: str) -> int:
    """
    Rough estimation of token count (approximately 4 chars per token)
    
    Args:
        text: Text to estimate
        
    Returns:
        Estimated token count
    """
    return len(text) // 4


def build_prompt_with_context(query: str, context: str, system_prompt: Optional[str] = None) -> str:
    """
    Build a complete prompt with context
    
    Args:
        query: User query
        context: Retrieved context
        system_prompt: Optional system prompt
        
    Returns:
        Complete prompt string
    """
    parts = []
    
    if system_prompt:
        parts.append(system_prompt)
    
    if context:
        parts.append(f"Context Information:\n{context}")
    
    parts.append(f"User Question: {query}")
    
    return "\n\n".join(parts)
