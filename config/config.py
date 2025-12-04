import os
from typing import Optional
from dotenv import load_dotenv

import streamlit as st

load_dotenv()


class Config:
    def _get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
        try:
            return st.secrets.get(key, os.getenv(key, default))
        except (FileNotFoundError, AttributeError):
            return os.getenv(key, default)

    OPENAI_API_KEY: Optional[str] = _get_secret("OPENAI_API_KEY")
    GROQ_API_KEY: Optional[str] = _get_secret("GROQ_API_KEY")
    GEMINI_API_KEY: Optional[str] = _get_secret("GEMINI_API_KEY")
    
    DEFAULT_LLM_PROVIDER: str = "groq"
    
    OPENAI_MODEL: str = "gpt-3.5-turbo"  
    GROQ_MODEL: str = "llama-3.1-8b-instant" 
    GEMINI_MODEL: str = "gemini-1.5-flash" 
    
    TEMPERATURE: float = 0.7
    
    MAX_TOKENS: int = 1000
    
    TOP_P: float = 0.9
    
    CONCISE_MAX_TOKENS: int = 150
    
    DETAILED_MAX_TOKENS: int = 1000
    
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    CHUNK_SIZE: int = 500 
    CHUNK_OVERLAP: int = 50 
    
    TOP_K_RETRIEVAL: int = 3 
    SIMILARITY_THRESHOLD: float = 0.5 
    
    DATA_DIR: str = "data"
    
    VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "data/vector_store")
    
    CHAT_STORAGE_DIR: str = os.getenv("CHAT_STORAGE_DIR", "data/chats")
    
    PRODUCT_CATALOG_PATH: str = os.getenv("PRODUCT_CATALOG_PATH", "data/product_catalog.json")
    
    MAX_SEARCH_RESULTS: int = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
    
    SEARCH_TIMEOUT: int = int(os.getenv("SEARCH_TIMEOUT", "10"))
    
    APP_TITLE: str = "🛍️ E-commerce Customer Support Chatbot"
    
    APP_DESCRIPTION: str = "Intelligent assistant for product inquiries, order status, returns, and promotions"
    
    CONCISE_SYSTEM_PROMPT: str = """You are a helpful e-commerce customer support assistant. 
Provide SHORT, CONCISE, and ACCURATE answers. Keep responses under 2-3 sentences.
Answer naturally as if the information is your own knowledge.
Do NOT say "according to the knowledge base" or "based on the provided context".
Base your answers STRICTLY on the provided context but do not explicitly mention it.
Be clear, direct, and professional.Always aim to solve the customer's query quickly and politely."""
    
    DETAILED_SYSTEM_PROMPT: str = """You are a knowledgeable e-commerce customer support assistant.
Provide DETAILED, ACCURATE, and CLEAR answers.
Answer naturally as if the information is your own knowledge.
Do NOT say "according to the knowledge base" or "based on the provided context".
Base your answers STRICTLY on the provided context but do not explicitly mention it.
Include relevant details and step-by-step instructions where applicable.
Be professional, friendly, and ensure the customer understands the information clearly.
Your goal is to ensure the customer feels confident that their problem is solved."""
    
    MAX_RECOMMENDATIONS: int = int(os.getenv("MAX_RECOMMENDATIONS", "5"))
    RECOMMENDATION_DISPLAY_LIMIT: int = int(os.getenv("RECOMMENDATION_DISPLAY_LIMIT", "3"))
    
    HIGH_PURCHASE_INTENT_THRESHOLD: float = float(os.getenv("HIGH_PURCHASE_INTENT_THRESHOLD", "0.5"))
    
    MIN_MESSAGES_FOR_RECOMMENDATION: int = int(os.getenv("MIN_MESSAGES_FOR_RECOMMENDATION", "3"))
    ENGAGED_USER_RECOMMENDATION_INTERVAL: int = int(os.getenv("ENGAGED_USER_RECOMMENDATION_INTERVAL", "7"))
    
    
    HIGH_ENGAGEMENT_MESSAGE_COUNT: int = int(os.getenv("HIGH_ENGAGEMENT_MESSAGE_COUNT", "5"))
    MEDIUM_ENGAGEMENT_MESSAGE_COUNT: int = int(os.getenv("MEDIUM_ENGAGEMENT_MESSAGE_COUNT", "2"))
    
    INTENT_MATCH_DIVISOR: float = float(os.getenv("INTENT_MATCH_DIVISOR", "3.0"))
    
    CATEGORY_MATCH_WEIGHT: float = float(os.getenv("CATEGORY_MATCH_WEIGHT", "0.3"))
    RATING_WEIGHT: float = float(os.getenv("RATING_WEIGHT", "0.3"))
    STOCK_AVAILABILITY_WEIGHT: float = float(os.getenv("STOCK_AVAILABILITY_WEIGHT", "0.2"))
    
    RECOMMENDATION_TEMPERATURE: float = float(os.getenv("RECOMMENDATION_TEMPERATURE", "0.7"))
    RECOMMENDATION_MAX_TOKENS: int = int(os.getenv("RECOMMENDATION_MAX_TOKENS", "100"))
    
    CONTEXTUALIZATION_TEMPERATURE: float = float(os.getenv("CONTEXTUALIZATION_TEMPERATURE", "0.1"))
    CONTEXTUALIZATION_MAX_TOKENS: int = int(os.getenv("CONTEXTUALIZATION_MAX_TOKENS", "100"))
    
    REFINEMENT_TEMPERATURE: float = float(os.getenv("REFINEMENT_TEMPERATURE", "0.1"))
    REFINEMENT_MAX_TOKENS: int = int(os.getenv("REFINEMENT_MAX_TOKENS", "100"))
    
    DEFAULT_RETENTION_DAYS: int = int(os.getenv("DEFAULT_RETENTION_DAYS", "90"))
    
    # HELPER METHODS
    
    @classmethod
    def validate_api_key(cls, provider: str) -> bool:
        key_map = {
            "openai": cls.OPENAI_API_KEY,
            "groq": cls.GROQ_API_KEY,
            "gemini": cls.GEMINI_API_KEY
        }
        
        api_key = key_map.get(provider.lower())
        return api_key is not None and len(api_key.strip()) > 0
    
    @classmethod
    def get_api_key(cls, provider: str) -> Optional[str]:
        key_map = {
            "openai": cls.OPENAI_API_KEY,
            "groq": cls.GROQ_API_KEY,
            "gemini": cls.GEMINI_API_KEY
        }
        return key_map.get(provider.lower())
    
    @classmethod
    def get_model_name(cls, provider: str) -> str:
        model_map = {
            "openai": cls.OPENAI_MODEL,
            "groq": cls.GROQ_MODEL,
            "gemini": cls.GEMINI_MODEL
        }
        return model_map.get(provider.lower(), cls.GROQ_MODEL)
    
    @classmethod
    def get_system_prompt(cls, mode: str = "detailed") -> str:
        return cls.CONCISE_SYSTEM_PROMPT if mode.lower() == "concise" else cls.DETAILED_SYSTEM_PROMPT
    
    @classmethod
    def get_max_tokens(cls, mode: str = "detailed") -> int:

        return cls.CONCISE_MAX_TOKENS if mode.lower() == "concise" else cls.DETAILED_MAX_TOKENS
    
    @classmethod
    def get_available_providers(cls) -> list:
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

def validate_configuration():
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
