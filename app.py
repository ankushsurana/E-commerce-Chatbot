import streamlit as st
import logging
import os
from typing import Optional


from config.config import config
from models.llm import LLMClient
from utils.rag import RAGPipeline
from utils.web_search import search_web, format_search_results
from utils.logger import setup_logger
from utils.helpers import format_response, refine_query, contextualize_query
from utils.chat_manager import ChatManager
from utils.recommendation_engine import RecommendationEngine

logger = setup_logger(__name__, level=logging.INFO)


def initialize_rag_pipeline() -> Optional[RAGPipeline]:
    try:
        with st.spinner("Loading knowledge base..."):
            rag = RAGPipeline()
            rag.initialize()
            logger.info("RAG pipeline initialized successfully")
            return rag
    except Exception as e:
        logger.error(f"Failed to initialize RAG: {str(e)}")
        st.error(f"⚠️ Could not load knowledge base: {str(e)}")
        return None


def get_llm_client(provider: str) -> Optional[LLMClient]:
    try:
        client = LLMClient(provider=provider)
        logger.info(f"LLM client initialized: {provider}")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize LLM client: {str(e)}")
        st.error(f"⚠️ Error initializing {provider}: {str(e)}")
        return None


def generate_response(
    llm_client: LLMClient,
    user_message: str,
    rag_pipeline: Optional[RAGPipeline],
    response_mode: str,
    use_web_search: bool = False,
    chat_history: list = None
) -> tuple[str, list]:
    """
   Generate response with RAG and optional web search
    
    Args:
        llm_client: LLM client instance
        user_message: User's message
        rag_pipeline: RAG pipeline instance
        response_mode: Response mode (concise/detailed)
        use_web_search: Whether to use web search
        chat_history: Current chat history for contextualization
        
    Returns:
        Tuple of (response, sources)
    """
    try:
        context = ""
        sources = []
        
        search_query = user_message
        if chat_history and llm_client:
            try:
                with st.spinner("Understanding context..."):
                    search_query = contextualize_query(user_message, chat_history, llm_client)
            except Exception as e:
                logger.warning(f"Contextualization failed: {str(e)}")

        refined_query = search_query
        if llm_client:
            try:
                with st.spinner("Analyzing query..."):
                    refined_query = refine_query(search_query, llm_client)
            except Exception as e:
                logger.warning(f"Query refinement failed: {str(e)}")
        
        if rag_pipeline:
            try:
                rag_context = rag_pipeline.get_context_for_query(refined_query)
                if rag_context:
                    context = f"**Context Information:**\n{rag_context}\n\n"
                    results = rag_pipeline.retrieve(refined_query)
                    sources = [{"type": "knowledge_base", "source": meta['source']} 
                              for _, meta, _ in results]
                    logger.info("RAG context retrieved")
            except Exception as e:
                logger.warning(f"RAG retrieval failed: {str(e)}")
        
        if use_web_search or (not context and use_web_search):
            try:
                with st.spinner("🔍 Searching the web..."):
                    search_results = search_web(refined_query, max_results=3)
                    if search_results:
                        web_context = format_search_results(search_results)
                        context += f"**Additional Context:**\n{web_context}\n\n"
                        sources.extend([{"type": "web", "source": r['link'], "title": r['title']} 
                                       for r in search_results])
                        logger.info("Web search context retrieved")
            except Exception as e:
                logger.warning(f"Web search failed: {str(e)}")
        
        enhanced_message = user_message
        if context:
            enhanced_message = f"{context}**User Question:** {user_message}"
        
        response = llm_client.chat(
            user_message=enhanced_message,
            conversation_history=chat_history or [],
            mode=response_mode.lower()
        )
        
        formatted_response = format_response(response, mode=response_mode.lower())
        
        return formatted_response, sources
    
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return f"⚠️ Error generating response: {str(e)}", []


def display_sources(sources: list):
    pass


def display_recommendations_panel(recommendations: list):
    if not recommendations:
        return
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🛍️ Recommended for You")
    
    for product in recommendations:
        with st.sidebar.expander(f"{product.get('name', 'Product')}"):
            st.markdown(f"**${product.get('price', 'N/A')}**")
            st.markdown(f"⭐ {product.get('rating', 'N/A')}/5")
            st.markdown(f"*{product.get('description', '')}*")
            if product.get('stock') == 'in-stock':
                st.success("✅ In Stock")
            st.markdown(f"_Category: {product.get('category', 'N/A')}_")


def initialize_session_state():
    if 'chat_manager' not in st.session_state:
        st.session_state.chat_manager = ChatManager()
        
    if 'current_session_id' not in st.session_state:
        session_id = st.session_state.chat_manager.create_session()
        st.session_state.current_session_id = session_id
        st.session_state.chat_history = []
        
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        
    if 'rag_pipeline' not in st.session_state:
        st.session_state.rag_pipeline = None
        
    if 'rag_initialized' not in st.session_state:
        st.session_state.rag_initialized = False
    
    if 'recommendation_engine' not in st.session_state:
        st.session_state.recommendation_engine = None
        
    if 'messages_since_recommendation' not in st.session_state:
        st.session_state.messages_since_recommendation = 0
        
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
        
    if 'show_recommendations' not in st.session_state:
        st.session_state.show_recommendations = True


def load_chat_session(session_id: str):
    session = st.session_state.chat_manager.load_session(session_id)
    if session:
        st.session_state.current_session_id = session_id
        st.session_state.chat_history = session.get("messages", [])
        st.rerun()


def create_new_chat():
    if not st.session_state.chat_history:
        return

    session_id = st.session_state.chat_manager.create_session()
    st.session_state.current_session_id = session_id
    st.session_state.chat_history = []
    st.session_state.messages_since_recommendation = 0
    st.session_state.user_profile = {}
    st.rerun()


def render_sidebar():
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        st.subheader("💬 Chat History")
        if st.button("➕ New Chat", use_container_width=True):
            create_new_chat()
            
        st.divider()
    
        st.subheader("LLM Provider")
        
        available_providers = []
        if config.validate_api_key("openai"):
            available_providers.append("OpenAI")
        if config.validate_api_key("groq"):
            available_providers.append("Groq")
        if config.validate_api_key("gemini"):
            available_providers.append("Gemini")
        
        if not available_providers:
            st.error("⚠️ No API keys configured!")
            st.info("Please add API keys to your `.env` file or environment variables.")
            st.code("""
OPENAI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
            """)
            return None, None, None
        
        provider = st.selectbox(
            "Select Provider",
            available_providers,
            index=0
        )
        
        st.subheader("Response Mode")
        response_mode = st.radio(
            "Select response style",
            ["Concise", "Detailed"],
            index=1,
            help="Concise: Short answers. Detailed: Comprehensive explanations."
        )
        
        # Web Search Toggle
        st.subheader("Features")
        use_web_search = st.checkbox(
            "Enable Web Search",
            value=False,
            help="Search the web when knowledge base doesn't have answer"
        )
        
        # Personalization Toggle
        st.session_state.show_recommendations = st.checkbox(
            "Personalized Recommendations",
            value=True,
            help="Get AI-powered product suggestions based on your interests"
        )
        
        st.divider()
        if st.button("🗑️ Clear Current Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.messages_since_recommendation = 0
            st.session_state.user_profile = {}
            # Update storage
            st.session_state.chat_manager.save_session(
                st.session_state.current_session_id,
                {
                    "id": st.session_state.current_session_id,
                    "title": "New Chat",
                    "messages": []
                }
            )
            st.rerun()
        
        return provider.lower(), response_mode, use_web_search


def main():
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon="🛍️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1f77b4;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 2rem;
        }
        .stChatMessage {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    initialize_session_state()
    
    if not st.session_state.rag_initialized:
        st.session_state.rag_pipeline = initialize_rag_pipeline()
        st.session_state.rag_initialized = True
    
    if st.session_state.recommendation_engine is None and st.session_state.show_recommendations:
        try:
            st.session_state.recommendation_engine = RecommendationEngine()
            logger.info("Recommendation engine initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize recommendation engine: {str(e)}")
    
    provider, response_mode, use_web_search = render_sidebar()
    
    st.markdown(f'<h1 class="main-title">{config.APP_TITLE}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{config.APP_DESCRIPTION}</p>', unsafe_allow_html=True)
    
    if not provider:
        st.warning("⚠️ Please configure at least one API key to use the chatbot.")
        st.markdown("""
        ### Quick Setup Guide
        
        1. Create a `.env` file in the project root
        2. Add at least one API key:
           ```
           GROQ_API_KEY=your_groq_api_key
           ```
        3. Restart the application
        
        **Get Free API Keys:**
        - [Groq](https://console.groq.com/keys) - Generous free tier
        - [Google Gemini](https://ai.google.dev) - Free tier available
        - [OpenAI](https://platform.openai.com/api-keys) - Paid service
        """)
        return
    
    llm_client = get_llm_client(provider)
    
    if not llm_client:
        return
    
    if (st.session_state.show_recommendations and 
        st.session_state.recommendation_engine and 
        st.session_state.chat_history):
        
        try:
            st.session_state.user_profile = st.session_state.recommendation_engine.analyze_user_behavior(
                st.session_state.chat_history
            )
            
            if st.session_state.recommendation_engine.should_show_recommendations(
                st.session_state.user_profile,
                st.session_state.messages_since_recommendation
            ):
                recommendations = st.session_state.recommendation_engine.get_product_recommendations(
                    st.session_state.user_profile,
                    limit=config.RECOMMENDATION_DISPLAY_LIMIT,
                    llm_client=llm_client
                )
                
                if recommendations:
                    display_recommendations_panel(recommendations)
                    st.session_state.messages_since_recommendation = 0
        except Exception as e:
            logger.error(f"Recommendation error: {str(e)}")
    
    for idx, message in enumerate(st.session_state.chat_history):
        role = message.get('role')
        content = message.get('content')
        sources = message.get('sources', [])
        
        with st.chat_message(role):
            st.markdown(content)
            if role == 'assistant' and sources:
                display_sources(sources)
    
    if user_input := st.chat_input("Ask about products, orders, shipping, returns, or policies..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        st.session_state.messages_since_recommendation += 1
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response, sources = generate_response(
                        llm_client=llm_client,
                        user_message=user_input,
                        rag_pipeline=st.session_state.rag_pipeline,
                        response_mode=response_mode,
                        use_web_search=use_web_search,
                        chat_history=st.session_state.chat_history[:-1] # Exclude current message from history for context
                    )
                    
                    st.markdown(response)
                    display_sources(sources)
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response,
                        "sources": sources
                    })
                    
                    current_title = "New Chat"
                    if len(st.session_state.chat_history) == 2:
                        current_title = user_input[:30] + "..." if len(user_input) > 30 else user_input
                        st.session_state.chat_manager.update_session_title(
                            st.session_state.current_session_id, 
                            current_title
                        )
                    
                    st.session_state.chat_manager.save_session(
                        st.session_state.current_session_id,
                        {
                            "id": st.session_state.current_session_id,
                            "title": current_title,
                            "messages": st.session_state.chat_history,
                            "user_profile": st.session_state.user_profile
                        }
                    )
                    
                except Exception as e:
                    error_msg = f"⚠️ Error: {str(e)}"
                    st.error(error_msg)
                    logger.error(f"Chat error: {str(e)}")


if __name__ == "__main__":
    main()