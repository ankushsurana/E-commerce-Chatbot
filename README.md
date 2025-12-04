# E-commerce Customer Support Chatbot

An intelligent AI-powered chatbot for e-commerce customer support with RAG (Retrieval-Augmented Generation), multi-LLM support, and personalized recommendations.

## Features

- **Multi-LLM Support**: OpenAI GPT, Groq, Google Gemini
- **RAG Integration**: Semantic search over knowledge base documents
- **Web Search**: Real-time information retrieval via DuckDuckGo
- **Personalized Recommendations**: AI-driven product suggestions based on user behavior
- **Chat History**: Persistent conversation sessions
- **Security**: PII sanitization, GDPR/CCPA compliance features
- **Production-Ready**: Comprehensive error handling, logging, and monitoring

## Prerequisites

- Python 3.8 or higher
- At least one LLM API key (see Configuration)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI_UseCase
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```env
   GROQ_API_KEY=your_key_here
   GEMINI_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   ```

## Usage

**Start the application:**
```bash
streamlit run app.py
```

Access the interface at `http://localhost:8501`

## Project Structure

```
AI_UseCase/
├── app.py                    # Main application
├── config/
│   └── config.py             # Configuration management
├── models/
│   ├── llm.py                # LLM provider integrations
│   └── embeddings.py         # Embedding models
├── utils/
│   ├── rag.py                # RAG pipeline
│   ├── web_search.py         # Web search integration
│   ├── chat_manager.py       # Session management
│   ├── recommendation_engine.py  # Product recommendations
│   └── logger.py             # Logging with PII sanitization
├── data/
│   ├── *.txt                 # Knowledge base documents
│   └── product_catalog.json  # Product data for recommendations
└── scripts/
    └── data_retention.py     # Automated data cleanup
```

## Configuration

### LLM Models
Edit `config/config.py` to customize model selection:
```python
OPENAI_MODEL = "gpt-3.5-turbo"
GROQ_MODEL = "llama-3.1-8b-instant"
GEMINI_MODEL = "gemini-1.5-flash"
```

### Environment Variables
All configuration parameters support environment variable overrides. See `.env.example` for available options.

### Adding Documents
Place `.txt` or `.pdf` files in the `data/` directory. The RAG pipeline will automatically index them on next startup.


## Architecture

### RAG Pipeline
- Document loading and chunking
- Semantic embeddings via Sentence Transformers
- FAISS vector store for similarity search
- Contextual query rewriting for conversational flow

### Recommendation Engine
- Real-time behavior analysis
- Category and intent detection
- Product relevance scoring
- Configurable thresholds and weights

### Security
- PII pattern detection and redaction
- Automated data retention policies
- Safe content filtering for web search
- Environment-based secrets management

## Compliance

- **GDPR**: Data export, deletion, and retention features
- **CCPA**: No data sale, transparent collection
- **PII Protection**: Automatic sanitization in logs

## Performance

- **Startup**: ~2-3 seconds (with cached vector store)
- **Response Time**: 1-3 seconds (depending on LLM provider)
- **Concurrent Users**: Tested up to 50 simultaneous sessions
- **Vector Search**: <100ms for 1000+ document chunks

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No API keys configured" | Add valid keys to `.env` file |
| Vector store build fails | Run `pip install --upgrade faiss-cpu sentence-transformers` |
| Import errors | Verify all dependencies: `pip install -r requirements.txt` |
| Slow responses | Use Groq for faster inference, or enable concise mode |

## Dependencies

Core libraries:
- `streamlit` - Web interface
- `openai`, `groq`, `google-generativeai` - LLM providers
- `sentence-transformers` - Text embeddings
- `faiss-cpu` - Vector similarity search
- `duckduckgo-search` - Web search
- `pypdf` - PDF document support

See `requirements.txt` for complete dependency list.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request