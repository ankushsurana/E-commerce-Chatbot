# 🚀 Quick Setup Guide - E-commerce Customer Support Chatbot

## Step 1: Install Dependencies

Open your terminal/command prompt and run:

```bash
cd "c:/Users/ASUS/Downloads/NeoStats AI Engineer Use Case/NeoStats AI Engineer Use Case/AI_UseCase"
pip install -r requirements.txt
```

**Note**: This will install Streamlit, OpenAI, Groq, Gemini, Sentence Transformers, FAISS, and other required libraries.

## Step 2: Get API Key (Choose ONE)

You only need **ONE** API key from any of these providers:

### Option 1: Groq (Recommended - FREE)
1. Visit: https://console.groq.com/keys
2. Sign up for free account
3. Create new API key
4. Copy the key

### Option 2: Google Gemini (FREE)
1. Visit: https://ai.google.dev
2. Click "Get API key in Google AI Studio"
3. Create new API key
4. Copy the key

### Option 3: OpenAI (Paid)
1. Visit: https://platform.openai.com/api-keys
2. Create account and add payment method
3. Create new API key
4. Copy the key

## Step 3: Configure API Key

### Method 1: Using .env file (Recommended)

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file and add your API key:
   ```
   # If using Groq:
   GROQ_API_KEY=your_actual_groq_key_here
   
   # OR if using Gemini:
   GEMINI_API_KEY=your_actual_gemini_key_here
   
   # OR if using OpenAI:
   OPENAI_API_KEY=your_actual_openai_key_here
   ```

3. Save the file

### Method 2: Using Environment Variables

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your_actual_groq_key_here"
```

**Mac/Linux:**
```bash
export GROQ_API_KEY="your_actual_groq_key_here"
```

## Step 4: Run the Chatbot

```bash
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501`

## Step 5: Use the Chatbot

1. **Select LLM Provider**: Choose from the dropdown in sidebar
2. **Choose Response Mode**: Select "Concise" or "Detailed"
3. **Optional**: Enable "Web Search" for real-time information
4. **Start Chatting**: Ask questions about products, orders, shipping, returns!

## 🎯 Example Questions to Try

- "What is your return policy?"
- "How long does shipping take?"
- "Do you have the iPhone 15 Pro in stock?"
- "Can I track my order?"
- "What payment methods do you accept?"
- "How do I exchange a product?"
- "Do you offer international shipping?"

## ⚡ Quick Troubleshooting

### "No API keys found"
- Make sure you created `.env` file
- Check that API key is uncommented (remove #)
- Verify the key is correct

### "Failed to load knowledge base"
- Check that `data/` folder has `.txt` files
- Run: `pip install sentence-transformers faiss-cpu`

### Dependencies installation fails
Try upgrading pip first:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 📚 Features Available

✅ **RAG (Retrieval-Augmented Generation)**
   - Automatically loads e-commerce knowledge base
   - Retrieves relevant information for accurate answers
   - Shows sources for transparency

✅ **Web Search (Optional)**
   - Enable in sidebar for real-time information
   - Uses DuckDuckGo (free, no API needed)
   - Great for current promotions or news

✅ **Multiple LLM Providers**
   - Switch between OpenAI, Groq, Gemini
   - Each has different strengths
   - Only needs one API key to work

✅ **Response Modes**
   - **Concise**: Quick, short answers
   - **Detailed**: Comprehensive explanations

## 🌐 Deploy to Internet (Streamlit Cloud)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "E-commerce chatbot"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file: `app.py`
   - Add API key in "Advanced settings" → "Secrets"
   - Click "Deploy"

Your chatbot will have a public URL like: `https://your-app.streamlit.app`

## 📞 Need Help?

Check the full README.md for:
- Detailed documentation
- Architecture explanation
- Advanced customization
- Complete troubleshooting guide

---

**That's it! You're ready to go! 🎉**

Run `streamlit run app.py` and start chatting!
