# 🔐 Setting Up Streamlit Secrets

Since `.env` files are not uploaded to GitHub for security, you must configure your API keys in Streamlit Cloud using **Secrets**.

## Step 1: Go to Streamlit Cloud

1. Log in to [share.streamlit.io](https://share.streamlit.io/)
2. Click on your deployed app
3. Click the **"⋮"** (three dots) menu in the top right
4. Select **"Settings"**
5. Go to the **"Secrets"** tab

## Step 2: Add Your Keys

Copy and paste the following into the Secrets text area (TOML format):

```toml
# LLM API Keys (Add at least one)
GROQ_API_KEY = "your_actual_groq_key_here"
GEMINI_API_KEY = "your_actual_gemini_key_here"
OPENAI_API_KEY = "your_actual_openai_key_here"

# Optional Configuration
MAX_SEARCH_RESULTS = 5
SEARCH_TIMEOUT = 10
APP_TITLE = "🛍️ E-commerce Chatbot"
```

## Step 3: Save and Reboot

1. Click **"Save"**
2. The app might auto-reload. If not, go to the menu and click **"Reboot app"**.

## ✅ How It Works

- **Locally:** The app reads from your `.env` file.
- **On Cloud:** The app reads from these Secrets.
- **Security:** Your keys are encrypted and never exposed in the code or GitHub.

---

**Troubleshooting:**
If you see "No API keys configured", double-check that the variable names in Secrets match exactly (e.g., `GROQ_API_KEY`).
