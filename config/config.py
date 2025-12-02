"""
Configuration Management for E-commerce Chatbot
Manages API keys, model settings, and application constants securely.

SECURITY NOTICE:
- ALL API keys are loaded from environment variables
- NEVER hardcode API keys in this file or any other source file
- API keys should be set in .env file (not committed to Git)
- Use .env.example as a template for creating your .env file
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Centralized configuration management for the E-commerce Chatbot
    
    All API keys and sensitive configuration should be managed through environment variables.
    This ensures security and flexibility across different deployment environments.
    """
    
    # ============================================================================
    # API KEYS - LOADED FROM ENVIRONMENT VARIABLES
    # ============================================================================
    # These are loaded from .env file or system environment variables
    # NEVER hardcode actual API keys here
    
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # ============================================================================
    # LLM PROVIDER SETTINGS
    # ============================================================================
    
    # Default LLM provider to use (options: "openai", "groq", "gemini")
    DEFAULT_LLM_PROVIDER: str = "groq"
    
    # Model names for each provider
    OPENAI_MODEL: str = "gpt-3.5-turbo"  # Alternative: "gpt-4", "gpt-4-turbo"
    GROQ_MODEL: str = "llama-3.1-8b-instant"  # Alternative: "mixtral-8x7b-32768", "llama-3.1-8b-instant"
    GEMINI_MODEL: str = "gemini-1.5-flash"  # Alternative: "gemini-pro", "gemini-1.5-pro"
    
    # ============================================================================
    # MODEL PARAMETERS
    # ============================================================================
    
    # Temperature: Controls randomness (0.0 = deterministic, 1.0 = creative)
    TEMPERATURE: float = 0.7
    
    # Maximum tokens in response
    MAX_TOKENS: int = 1000
    
    # Top-p sampling for nucleus sampling
    TOP_P: float = 0.9
    
    # ============================================================================
    # RESPONSE MODE SETTINGS
    # ============================================================================
    
    # Maximum tokens for concise responses
    CONCISE_MAX_TOKENS: int = 150
    
    # Maximum tokens for detailed responses
    DETAILED_MAX_TOKENS: int = 1000
    
    # ============================================================================
    # RAG (RETRIEVAL-AUGMENTED GENERATION) SETTINGS
    # ============================================================================
    
    # Embedding model for vector embeddings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Text chunking parameters
    CHUNK_SIZE: int = 500  # Characters per chunk
    CHUNK_OVERLAP: int = 50  # Overlap between chunks
    
    # Retrieval parameters
    TOP_K_RETRIEVAL: int = 3  # Number of chunks to retrieve
    SIMILARITY_THRESHOLD: float = 0.5  # Minimum similarity score
    
    # ============================================================================
    # FILE PATHS
    # ============================================================================
    
    # Directory containing knowledge base documents
    DATA_DIR: str = "data"
    
    # Path to save/load vector store
    VECTOR_STORE_PATH: str = "data/vector_store"
    
    # ============================================================================
    # WEB SEARCH SETTINGS
    # ============================================================================
    
    # Maximum number of web search results to retrieve
    MAX_SEARCH_RESULTS: int = 5
    
    # Timeout for web search requests (seconds)
    SEARCH_TIMEOUT: int = 10
    
    # ============================================================================
    # APPLICATION SETTINGS
    # ============================================================================
    
    # Application title
    APP_TITLE: str = "🛍️ E-commerce Customer Support Chatbot"
    
    # Application description
    APP_DESCRIPTION: str = "Intelligent assistant for product inquiries, order status, returns, and promotions"
    
    # ============================================================================
    # SYSTEM PROMPTS
    # ============================================================================
    
    CONCISE_SYSTEM_PROMPT: str = """You are a helpful e-commerce customer support assistant. 
Provide SHORT, CONCISE, and ACCURATE answers. Keep responses under 2-3 sentences.
Answer naturally as if the information is your own knowledge.
Do NOT say "according to the knowledge base" or "based on the provided context".
Base your answers STRICTLY on the provided context but do not explicitly mention it.
Be clear, direct, and professional."""
    
    DETAILED_SYSTEM_PROMPT: str = """You are a knowledgeable e-commerce customer support assistant.
Provide DETAILED, ACCURATE, and CLEAR answers.
Answer naturally as if the information is your own knowledge.
Do NOT say "according to the knowledge base" or "based on the provided context".
Base your answers STRICTLY on the provided context but do not explicitly mention it.
Include relevant details and step-by-step instructions where applicable.
Be professional, friendly, and ensure the customer understands the information clearly."""
    
    # ============================================================================
    # HELPER METHODS
    # ============================================================================
    
    @classmethod
    def validate_api_key(cls, provider: str) -> bool:
        """
        Validate that API key exists for the specified provider
        
        Args:
            provider: LLM provider name ("openai", "groq", "gemini")
            
        Returns:
            bool: True if API key is configured, False otherwise
        """
        key_map = {
            "openai": cls.OPENAI_API_KEY,
            "groq": cls.GROQ_API_KEY,
            "gemini": cls.GEMINI_API_KEY
        }
        
        api_key = key_map.get(provider.lower())
        return api_key is not None and len(api_key.strip()) > 0
    
    @classmethod
    def get_api_key(cls, provider: str) -> Optional[str]:
        """
        Get API key for the specified provider
        
        Args:
            provider: LLM provider name
            
        Returns:
            API key string or None if not configured
        """
        key_map = {
            "openai": cls.OPENAI_API_KEY,
            "groq": cls.GROQ_API_KEY,
            "gemini": cls.GEMINI_API_KEY
        }
        return key_map.get(provider.lower())
    
    @classmethod
    def get_model_name(cls, provider: str) -> str:
        """
        Get model name for the specified provider
        
        Args:
            provider: LLM provider name
            
        Returns:
            Model name string
        """
        model_map = {
            "openai": cls.OPENAI_MODEL,
            "groq": cls.GROQ_MODEL,
            "gemini": cls.GEMINI_MODEL
        }
        return model_map.get(provider.lower(), cls.GROQ_MODEL)
    
    @classmethod
    def get_system_prompt(cls, mode: str = "detailed") -> str:
        """
        Get system prompt based on response mode
        
        Args:
            mode: Response mode ("concise" or "detailed")
            
        Returns:
            System prompt string
        """
        return cls.CONCISE_SYSTEM_PROMPT if mode.lower() == "concise" else cls.DETAILED_SYSTEM_PROMPT
    
    @classmethod
    def get_max_tokens(cls, mode: str = "detailed") -> int:
        """
        Get max tokens based on response mode
        
        Args:
            mode: Response mode ("concise" or "detailed")
            
        Returns:
            Maximum token count
        """
        return cls.CONCISE_MAX_TOKENS if mode.lower() == "concise" else cls.DETAILED_MAX_TOKENS
    
    @classmethod
    def get_available_providers(cls) -> list:
        """
        Get list of available LLM providers (those with API keys configured)
        
        Returns:
            List of provider names that have valid API keys
        """
        available = []
        if cls.validate_api_key("openai"):
            available.append("openai")
        if cls.validate_api_key("groq"):
            available.append("groq")
        if cls.validate_api_key("gemini"):
            available.append("gemini")
        return available


# Create singleton instance for easy import
config = Config()


# ============================================================================
# CONFIGURATION VALIDATION
# ============================================================================

def validate_configuration():
    """
    Validate that at least one LLM provider is configured
    Returns a tuple of (is_valid, error_message)
    """
    available_providers = config.get_available_providers()
    
    if not available_providers:
        error_msg = """
        ⚠️ NO API KEYS CONFIGURED!
        
        Please configure at least one LLM provider API key in your .env file:
        
        1. Copy .env.example to .env
        2. Add your API key(s):
           - GROQ_API_KEY=your_key_here (free tier available)
           - GEMINI_API_KEY=your_key_here (free tier available)
           - OPENAI_API_KEY=your_key_here (paid service)
        3. Restart the application
        
        Get free API keys at:
        - Groq: https://console.groq.com/keys
        - Gemini: https://ai.google.dev
        - OpenAI: https://platform.openai.com/api-keys (paid)
        """
        return False, error_msg
    
    return True, f"✅ Configured providers: {', '.join(available_providers)}"


# ============================================================================
# USAGE EXAMPLE
# ============================================================================
"""
To use this configuration in your code:

from config.config import config

# Get API key
api_key = config.get_api_key("groq")

# Check if provider is available
if config.validate_api_key("groq"):
    # Use Groq
    pass

# Get model name
model = config.get_model_name("openai")

# Get system prompt
prompt = config.get_system_prompt("concise")

# Validate configuration
is_valid, message = validate_configuration()
if not is_valid:
    print(message)
"""
