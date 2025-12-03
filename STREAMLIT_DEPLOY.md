# Streamlit Cloud Deployment Package

This package contains a production-ready e-commerce customer support chatbot.

## Files Required for Deployment

- `app.py` - Main application
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - UI configuration
- `config/` - Configuration module
- `models/` - LLM integrations
- `utils/` - Helper utilities
- `data/` - Knowledge base documents

## Quick Deploy to Streamlit Cloud

1. **Push code to GitHub**
2. **Go to** https://streamlit.io/cloud
3. **Click "New app"**
4. **Select repository:** `ankushsurana/E-commerce-Chatbot`
5. **Set main file:** `app.py`
6. **Add secrets** (in Advanced settings):
   ```
   GROQ_API_KEY = "your_groq_key"
   GEMINI_API_KEY = "your_gemini_key"
   OPENAI_API_KEY = "your_openai_key"
   ```
7. **Deploy!**

## Deployment Verified ✅

This package has been optimized for Streamlit Cloud with:
- Compatible dependency versions
- Proper numpy pinning (`<2.0.0`)
- Removed conflicting packages
- Cloud-optimized configuration

Your app will be live at: `https://[your-app-name].streamlit.app`
