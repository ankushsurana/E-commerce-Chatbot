# 🔒 Security & Configuration Guide

## Overview

This E-commerce Customer Support Chatbot follows strict security best practices for managing API keys and sensitive configuration. **No API keys are hardcoded anywhere in the codebase.**

## ✅ Security Features Implemented

### 1. Centralized Configuration
All API keys and configuration settings are managed through a single module: `config/config.py`

**Key Benefits:**
- Single source of truth for all settings
- Easy to audit security
- Consistent across the entire codebase
- Simple to update and maintain

### 2. Environment Variable Management
All API keys are loaded from environment variables using `python-dotenv`:

```python
# In config/config.py
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

**Never** hardcode API keys in source code!

### 3. Git Ignore Protection
The `.gitignore` file prevents accidental commits of sensitive files:

```gitignore
# Environment Variables
.env

# Streamlit Secrets
.streamlit/secrets.toml
```

### 4. Template File for Setup
`.env.example` provides a safe template (no real keys):

```env
# OPENAI_API_KEY=your_openai_api_key_here
# GROQ_API_KEY=your_groq_api_key_here
# GEMINI_API_KEY=your_gemini_api_key_here
```

## 📁 Files Using Configuration

### ✅ config/config.py
**Status:** ✅ SECURE
- Loads API keys from environment variables via `os.getenv()`
- Provides helper methods for key validation
- Contains only constants and environment variable references
- **NO HARDCODED SECRETS**

### ✅ models/llm.py
**Status:** ✅ SECURE
- Imports configuration: `from config.config import config`
- Retrieves API keys: `config.get_api_key(provider)`
- Validates keys: `config.validate_api_key(provider)`
- **NO HARDCODED SECRETS**

### ✅ models/embeddings.py
**Status:** ✅ SECURE
- Imports configuration: `from config.config import config`
- Uses model settings: `config.EMBEDDING_MODEL`
- **NO HARDCODED SECRETS**

### ✅ utils/rag.py
**Status:** ✅ SECURE
- Imports configuration: `from config.config import config`
- Uses paths and settings: `config.DATA_DIR`, `config.CHUNK_SIZE`, etc.
- **NO HARDCODED SECRETS**

### ✅ app.py
**Status:** ✅ SECURE  
- Imports configuration: `from config.config import config`
- Uses config for validation: `config.validate_api_key()`
- **NO HARDCODED SECRETS**

### ✅ utils/web_search.py
**Status:** ✅ SECURE
- Uses DuckDuckGo (no API key required)
- **NO API KEYS NEEDED**

### ✅ utils/logger.py & utils/helpers.py
**Status:** ✅ SECURE
- Utility functions only
- **NO API KEYS NEEDED**

## 🔑 How to Set Up API Keys

### Method 1: Using .env File (Recommended)

1. **Copy the template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env file:**
   ```env
   # Add your actual API keys (uncomment and replace)
   GROQ_API_KEY=gsk_actual_key_here
   GEMINI_API_KEY=actual_gemini_key_here
   OPENAI_API_KEY=sk-actual_openai_key_here
   ```

3. **Save the file** (it's automatically gitignored)

### Method 2: System Environment Variables

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your_actual_key_here"
```

**Linux/Mac:**
```bash
export GROQ_API_KEY="your_actual_key_here"
```

### Method 3: Streamlit Cloud Secrets

When deploying to Streamlit Cloud:

1. Go to your app settings
2. Click "Secrets"
3. Add your keys in TOML format:
   ```toml
   GROQ_API_KEY = "your_actual_key_here"
   GEMINI_API_KEY = "your_actual_key_here"
   ```

## ⚠️ Security Checklist

Before committing code or deploying, verify:

- [ ] No API keys in source code files
- [ ] `.env` file is in `.gitignore`
- [ ] `.env.example` contains only placeholders
- [ ] All keys loaded via `os.getenv()`
- [ ] `config/config.py` uses environment variables only
- [ ] No secrets in version control history

## 🚨 What NOT to Do

❌ **NEVER** commit actual API keys to Git:
```python
# BAD - Don't do this!
OPENAI_API_KEY = "sk-1234567890abcdef"
```

❌ **NEVER** hardcode keys in any file:
```python
# BAD - Don't do this!
client = OpenAI(api_key="sk-real-key")
```

❌ **NEVER** share your `.env` file:
- Don't email it
- Don't upload it
- Don't share it on Slack/Discord

## ✅ What TO Do

✅ **USE** environment variables:
```python
# GOOD - Do this!
from config.config import config
api_key = config.get_api_key("openai")
```

✅ **USE** the centralized config module:
```python
# GOOD - Do this!
from config.config import config
if config.validate_api_key("groq"):
    client = LLMClient(provider="groq")
```

✅ **USE** `.gitignore` to protect secrets:
```gitignore
.env
.streamlit/secrets.toml
*.key
*.pem
```

## 🔍 How to Audit Security

### Quick Security Scan

Run these commands to check for potential issues:

```bash
# Search for potential hardcoded keys (should return ONLY config.py)
grep -r "API_KEY" --include="*.py" .

# Search for "api_key=" patterns
grep -r 'api_key=' --include="*.py" .

# Verify .env is gitignored
git check-ignore .env
```

### Expected Results

**config/config.py should contain:**
```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # ✅ GOOD
```

**Other files should contain:**
```python
from config.config import config  # ✅ GOOD
api_key = config.get_api_key("openai")  # ✅ GOOD
```

**No file should contain:**
```python
api_key = "sk-1234..."  # ❌ BAD - Hardcoded key
API_KEY = "actual_key"  # ❌ BAD - Hardcoded key
```

## 📊 Configuration Architecture

```
┌─────────────────────────────────────────────┐
│           Environment Variables              │
│  (.env file or system env vars)             │
│  - OPENAI_API_KEY                           │
│  - GROQ_API_KEY                             │
│  - GEMINI_API_KEY                           │
└──────────────────┬──────────────────────────┘
                   │
                   │ os.getenv()
                   ▼
┌─────────────────────────────────────────────┐
│          config/config.py                    │
│  - Loads keys once                          │
│  - Provides validation                      │
│  - Centralizes all settings                 │
└──────────────────┬──────────────────────────┘
                   │
                   │ import config
                   ▼
┌─────────────────────────────────────────────┐
│        Application Modules                   │
│  - models/llm.py                            │
│  - models/embeddings.py                     │
│  - utils/rag.py                             │
│  - app.py                                   │
│  ALL use: config.get_api_key()              │
└─────────────────────────────────────────────┘
```

## 🛡️ Best Practices Summary

1. **Centralize** all configuration in `config/config.py`
2. **Use** environment variables for all secrets
3. **Never** commit `.env` files
4. **Always** use `.env.example` as template
5. **Import** config module in all files needing configuration
6. **Validate** API keys before using them
7. **Audit** regularly for hardcoded secrets
8. **Rotate** API keys periodically
9. **Monitor** API usage for suspicious activity
10. **Document** configuration requirements clearly

## 📝 Adding New API Keys

If you need to add a new API service:

1. **Add to .env.example:**
   ```env
   # NEW_SERVICE_API_KEY=your_key_here
   ```

2. **Add to config/config.py:**
   ```python
   NEW_SERVICE_API_KEY = os.getenv("NEW_SERVICE_API_KEY")
   ```

3. **Add validation helper:**
   ```python
   @classmethod
   def get_new_service_key(cls):
       return cls.NEW_SERVICE_API_KEY
   ```

4. **Use in your code:**
   ```python
   from config.config import config
   api_key = config.get_new_service_key()
   ```

## 🚀 Deployment Security

### Streamlit Cloud
- Use built-in secrets management
- Never commit secrets.toml

### Docker
- Use environment variables: `-e GROQ_API_KEY=xxx`
- Or use Docker secrets

### AWS/GCP/Azure
- Use cloud secret managers (AWS Secrets Manager, GCP Secret Manager)
- Inject at runtime, not build time

## ✅ Security Verification Complete

**Status:** All files audited and verified secure.
**Last Checked:** 2025-12-01
**Conclusion:** No API keys are hardcoded. All configuration properly centralized.

---

**Remember:** Security is everyone's responsibility. When in doubt, never commit API keys!
