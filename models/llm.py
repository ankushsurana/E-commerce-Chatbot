from typing import List, Dict, Optional
import logging
from config.config import config


class LLMClient:
    
    def __init__(self, provider: str = "groq"):
        self.provider = provider.lower()
        self.logger = logging.getLogger(__name__)
        self.client = None
        
        if not config.validate_api_key(self.provider):
            raise ValueError(
                f"API key for {self.provider} not configured. "
                f"Please set {self.provider.upper()}_API_KEY in your .env file."
            )
        
        try:
            self._initialize_client()
        except Exception as e:
            self.logger.error(f"Failed to initialize {provider} client: {str(e)}")
            raise
    
    def _initialize_client(self):        
        if self.provider == "openai":
            try:
                from openai import OpenAI
                api_key = config.get_api_key("openai")
                self.client = OpenAI(api_key=api_key)
                self.logger.info("OpenAI client initialized successfully")
            except ImportError:
                raise ImportError("openai package not installed. Install with: pip install openai")
        
        elif self.provider == "groq":
            try:
                from groq import Groq
                api_key = config.get_api_key("groq")
                self.client = Groq(api_key=api_key)
                self.logger.info("Groq client initialized successfully")
            except ImportError:
                raise ImportError("groq package not installed. Install with: pip install groq")
        
        elif self.provider == "gemini":
            try:
                import google.generativeai as genai
                api_key = config.get_api_key("gemini")
                genai.configure(api_key=api_key)
                model_name = config.get_model_name("gemini")
                self.client = genai.GenerativeModel(model_name)
                self.logger.info("Gemini client initialized successfully")
            except ImportError:
                raise ImportError("google-generativeai package not installed. Install with: pip install google-generativeai")
        
        else:
            raise ValueError(f"Unsupported provider: {self.provider}. Choose from: openai, groq, gemini")
    
    def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate response from LLM
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (uses config default if None)
            max_tokens: Maximum tokens in response (uses config default if None)
            
        Returns:
            Generated response text
        """
        try:
            temp = temperature if temperature is not None else config.TEMPERATURE
            tokens = max_tokens if max_tokens is not None else config.MAX_TOKENS
            
            if self.provider in ["openai", "groq"]:
                return self._generate_openai_style(messages, temp, tokens)
            elif self.provider == "gemini":
                return self._generate_gemini(messages, temp, tokens)
            
        except Exception as e:
            self.logger.error(f"Error generating response with {self.provider}: {str(e)}")
            raise
    
    def _generate_openai_style(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float, 
        max_tokens: int
    ) -> str:
        
        try:
            model_name = config.get_model_name(self.provider)
            
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=config.TOP_P
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            self.logger.error(f"{self.provider} API error: {str(e)}")
            raise
    
    def _generate_gemini(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float, 
        max_tokens: int
    ) -> str:
        
        try:
            chat_history = []
            prompt = ""
            
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                if role == "system":
                    prompt = content + "\n\n"
                elif role == "user":
                    if chat_history:
                        chat_history.append({"role": "user", "parts": [content]})
                    else:
                        prompt += content
                elif role == "assistant":
                    chat_history.append({"role": "model", "parts": [content]})
            
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                "top_p": config.TOP_P,
            }
            
            if chat_history:
                chat = self.client.start_chat(history=chat_history[:-1])
                response = chat.send_message(
                    chat_history[-1]["parts"][0],
                    generation_config=generation_config
                )
            else:
                response = self.client.generate_content(
                    prompt,
                    generation_config=generation_config
                )
            
            return response.text.strip()
        
        except Exception as e:
            self.logger.error(f"Gemini API error: {str(e)}")
            raise
    
    def chat(
        self, 
        user_message: str, 
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        mode: str = "detailed"
    ) -> str:
        """
        High-level chat interface
        
        Args:
            user_message: User's message
            system_prompt: Optional system prompt (uses config default if not provided)
            conversation_history: Previous conversation messages
            mode: Response mode ("concise" or "detailed") - affects prompt and tokens
            
        Returns:
            Assistant's response
        """
        try:
            messages = []
            
            sys_prompt = system_prompt if system_prompt else config.get_system_prompt(mode)
            messages.append({"role": "system", "content": sys_prompt})
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": user_message})
            
            max_tokens = config.get_max_tokens(mode)
            
            sanitized_messages = []
            for msg in messages:
                sanitized_msg = {
                    "role": msg.get("role"),
                    "content": msg.get("content")
                }
                sanitized_messages.append(sanitized_msg)
            
            response = self.generate_response(sanitized_messages, max_tokens=max_tokens)
            
            return response
        
        except Exception as e:
            self.logger.error(f"Chat error: {str(e)}")
            raise
    
    @staticmethod
    def is_provider_available(provider: str) -> bool:
        return config.validate_api_key(provider)
    
    @staticmethod
    def get_available_providers() -> List[str]:
        return config.get_available_providers()