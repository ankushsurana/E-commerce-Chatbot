# 🛍️ E-commerce Customer Support Chatbot

A production-ready intelligent chatbot built with Streamlit for e-commerce customer support. Features Retrieval-Augmented Generation (RAG), live web search, multiple LLM provider support, and flexible response modes.

## ✨ Features

- **🤖 Multi-LLM Support**: Switch between OpenAI GPT, Groq, and Google Gemini
- **📚 RAG Integration**: Retrieves relevant information from local knowledge base documents
- **🔍 Live Web Search**: Searches the web when knowledge base doesn't have answers
- **💬 Response Modes**: Toggle between Concise and Detailed response styles
- **🔒 Secure**: API keys managed via environment variables
- **📊 Production-Ready**: Robust error handling, logging, and modular architecture
- **🎨 User-Friendly UI**: Clean, intuitive Streamlit interface

## 📋 Prerequisites

- Python 3.8+
- At least one LLM API key (Groq and Gemini offer free tiers!)

## 🚀 Quick Start

### 1. Clone or Download the Project

```bash
cd AI_UseCase
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add at least ONE API key:

```env
# Choose at least one:
GROQ_API_KEY=your_groq_key_here           # FREE tier available
GEMINI_API_KEY=your_gemini_key_here       # FREE tier available
OPENAI_API_KEY=your_openai_key_here       # Paid service
```

**Get Free API Keys:**

- **Groq** (Recommended): [console.groq.com/keys](https://console.groq.com/keys) - Generous free tier
- **Google Gemini**: [ai.google.dev](https://ai.google.dev) - Free API access
- **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys) - Requires payment

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
AI_UseCase/
├── config/
│   └── config.py              # Configuration management
├── models/
│   ├── __init__.py
│   ├── llm.py                 # LLM provider integrations
│   └── embeddings.py          # Embedding models
├── utils/
│   ├── __init__.py
│   ├── rag.py                 # RAG pipeline
│   ├── web_search.py          # Web search integration
│   ├── logger.py              # Logging utilities
│   └── helpers.py             # Helper functions
├── data/
│   ├── faqs.txt              # E-commerce FAQs
│   ├── return_policy.txt     # Return policy
│   ├── shipping_policy.txt   # Shipping information
│   └── products.txt          # Product catalog
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── app.py                     # Main application
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🎯 Usage Guide

### Basic Usage

1. **Start the App**: Run `streamlit run app.py`
2. **Select LLM Provider**: Choose from available providers in the sidebar
3. **Set Response Mode**: Choose Concise or Detailed
4. **Enable Web Search**: (Optional) Toggle web search for real-time information
5. **Start Chatting**: Ask questions about products, orders, shipping, returns, etc.

### Example Questions

- "What is your return policy?"
- "How long does shipping take?"
- "Do you have the iPhone 15 Pro in stock?"
- "Can I track my order?"
- "What payment methods do you accept?"
- "Do you offer international shipping?"

### Response Modes

- **Concise**: Short, to-the-point answers (2-3 sentences)
- **Detailed**: Comprehensive explanations with additional context

### Web Search

Enable web search to fetch real-time information when the knowledge base doesn't have the answer. Useful for:
- Current promotions
- Latest product releases
- Real-time shipping updates
- Industry trends

## 🏗️ Architecture

### RAG Pipeline

1. **Document Loading**: Loads all `.txt` files from `data/` directory
2. **Chunking**: Splits documents into 500-character chunks with 50-character overlap
3. **Embedding**: Uses Sentence Transformers (`all-MiniLM-L6-v2`) to create embeddings
4. **Vector Store**: FAISS index for fast similarity search
5. **Retrieval**: Finds top-3 most relevant chunks for each query

### LLM Integration

- **Unified Interface**: Consistent API across all providers
- **Flexible Switching**: Change providers via UI dropdown
- **Error Handling**: Graceful fallbacks on API failures
- **Conversation History**: Maintains context across messages

### Web Search

- **Provider**: DuckDuckGo (free, no API key required)
- **Trigger**: Manual toggle or automatic when RAG returns no results
- **Results**: Top 3-5 most relevant web pages
- **Format**: Integrated into LLM context with source citations

## 🔧 Configuration

### LLM Models

Edit `config/config.py` to change default models:

```python
OPENAI_MODEL = "gpt-3.5-turbo"  # or "gpt-4"
GROQ_MODEL = "llama-3.1-8b-instant"  # or "mixtral-8x7b-32768"
GEMINI_MODEL = "gemini-1.5-flash"  # or "gemini-pro"
```

### RAG Settings

Adjust chunking and retrieval parameters:

```python
CHUNK_SIZE = 500           # Characters per chunk
CHUNK_OVERLAP = 50         # Overlap between chunks
TOP_K_RETRIEVAL = 3        # Number of chunks to retrieve
```

### Adding Documents

1. Add `.txt` files to the `data/` directory
2. Restart the application
3. The RAG pipeline will automatically load new documents

## 🌐 Deployment to Streamlit Cloud

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `app.py`
6. Click "Advanced settings" and add environment variables:
   - `GROQ_API_KEY` = your key
   - `GEMINI_API_KEY` = your key
   - `OPENAI_API_KEY` = your key
7. Click "Deploy"

Your app will be live at `https://your-app-name.streamlit.app`

## 🛠️ Troubleshooting

### "No API keys found"

**Solution**: Ensure `.env` file exists and contains at least one valid API key.

### "Failed to load knowledge base"

**Solution**: Check that `data/` directory exists with `.txt` files. Verify file permissions.

### "Error generating response"

**Solutions**:
- Verify API key is valid and has credits/quota
- Check internet connection
- Try a different LLM provider
- Check logs for specific error messages

### Vector store build fails

**Solution**: Ensure `sentence-transformers` is installed correctly. Try:

```bash
pip install --upgrade sentence-transformers
```

### Web search not working

**Solution**: DuckDuckGo may be blocked or rate-limited. Wait a few minutes and try again.

## 📦 Dependencies

- **streamlit**: Web UI framework
- **openai**: OpenAI API client
- **groq**: Groq API client
- **google-generativeai**: Google Gemini API client
- **sentence-transformers**: Text embedding models
- **faiss-cpu**: Vector similarity search
- **duckduckgo-search**: Free web search
- **python-dotenv**: Environment variable management

See `requirements.txt` for complete list with versions.

## 🔐 Security Best Practices

✅ **DO**:
- Store API keys in `.env` file (never commit to Git)
- Add `.env` to `.gitignore`
- Use environment variables in production
- Rotate API keys regularly
- Monitor API usage and costs

❌ **DON'T**:
- Commit API keys to Git
- Hardcode sensitive data
- Share `.env` file
- Use production keys in development

## 📝 Customization

### Change Chatbot Domain

1. Update knowledge base documents in `data/`
2. Modify system prompts in `config/config.py`
3. Adjust UI text in `app.py`

### Add More LLM Providers

1. Install provider client library
2. Add integration in `models/llm.py`
3. Add API key to `config/config.py`
4. Update UI dropdown in `app.py`

### Customize UI Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor="#your-color"
backgroundColor="#your-bg-color"
```

## 📊 Performance Tips

- **RAG**: Pre-build vector store for faster startup (automatic after first run)
- **Caching**: Streamlit caches RAG pipeline in session state
- **Concise Mode**: Use for faster responses with lower token usage
- **Model Selection**: Smaller models (e.g., Groq Llama-8B) are faster but less capable

## 🤝 Contributing

This is a use-case implementation. For production use:

1. Add comprehensive error tracking (e.g., Sentry)
2. Implement rate limiting
3. Add user authentication
4. Set up monitoring and analytics
5. Add automated tests
6. Implement conversation persistence (database)

## 📄 License

This project is provided as-is for educational and commercial use.

## 🆘 Support

For issues or questions:
- Check the Troubleshooting section above
- Review logs for error details
- Verify all dependencies are installed correctly
- Ensure API keys are valid and have quota

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [LangChain RAG Guide](https://python.langchain.com/docs/use_cases/question_answering/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)

---

**Built with ❤️ using Streamlit, Python, and modern AI technologies**
