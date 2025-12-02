# Privacy Policy & Data Protection

## Overview
This E-commerce Customer Support Chatbot is designed with privacy and security as core principles. We are committed to protecting customer data and complying with relevant privacy regulations including GDPR, CCPA, and other applicable laws.

## Data Collection & Usage

### What Data We Collect
- **Chat Messages**: User questions and bot responses
- **Session Metadata**: Session IDs, timestamps, chat titles
- **Technical Data**: LLM provider selection, response mode preferences

### What We DO NOT Collect
- ❌ Personal Identifiable Information (PII) such as names, addresses, phone numbers
- ❌ Payment information
- ❌ Email addresses
- ❌ Social security numbers or government IDs
- ❌ IP addresses or tracking cookies

## Data Storage & Security

### Local Storage
- All chat sessions are stored **locally** in the `data/chats/` directory as JSON files
- No data is transmitted to external services except:
  - LLM provider APIs (OpenAI, Groq, or Gemini) for response generation
  - DuckDuckGo for web search (when enabled)

### Encryption
- Data at rest: Files are stored in plain text JSON (suitable for local development/testing)
- Data in transit: All API communications use HTTPS/TLS encryption
- **Production Recommendation**: Implement file-level or disk encryption for the `data/chats/` directory

### API Key Security
- ✅ All API keys are stored in environment variables (`.env` file)
- ✅ Never hardcoded in source code
- ✅ `.env` is in `.gitignore` to prevent accidental commits
- ✅ Access to API keys requires file system access to the deployment environment

## Data Retention & Deletion

### Retention Policy
- Chat sessions are retained indefinitely by default for user convenience
- **Recommended**: Implement automated cleanup of sessions older than 90 days

### User Rights
Users have the right to:
1. **Access**: View their chat history through the application
2. **Deletion**: Clear individual chat sessions or all data
3. **Portability**: Export chat data (JSON format)

### How to Delete Data

#### Delete Single Session
```python
# Via ChatManager API
from utils.chat_manager import ChatManager
manager = ChatManager()
manager.delete_session(session_id)
```

#### Delete All Sessions
```powershell
# Manual cleanup
Remove-Item -Path "data/chats/*" -Force
```

## Compliance Features

### GDPR Compliance
- ✅ **Right to Access**: Users can view all their chat data
- ✅ **Right to Erasure**: Sessions can be deleted
- ✅ **Right to Portability**: Data is in open JSON format
- ✅ **Data Minimization**: Only essential data is collected
- ✅ **Purpose Limitation**: Data used only for customer support
- ✅ **Storage Limitation**: Local storage, no unnecessary backups

### CCPA Compliance
- ✅ **No Sale of Data**: Data is never sold or shared with third parties
- ✅ **Transparent Collection**: This policy documents all data collection
- ✅ **Deletion Rights**: Users can request data deletion
- ✅ **No Discrimination**: Service quality unchanged regardless of privacy choices

## Third-Party Data Sharing

### LLM Providers
When a user interacts with the chatbot:
- The query and conversation history are sent to the selected LLM provider
- Providers: OpenAI, Groq, or Google Gemini
- **Important**: Review each provider's privacy policy:
  - [OpenAI Privacy Policy](https://openai.com/privacy/)
  - [Groq Privacy Policy](https://groq.com/privacy-policy/)
  - [Google Gemini Terms](https://ai.google.dev/gemini-api/terms)

### Web Search
- When web search is enabled, queries are sent to DuckDuckGo
- DuckDuckGo does not track users or store search history
- [DuckDuckGo Privacy Policy](https://duckduckgo.com/privacy)

## Security Measures

### Input Sanitization
- ✅ User inputs are sanitized before processing
- ✅ No code injection vulnerabilities
- ✅ Safe handling of special characters

### Content Filtering
- ✅ Strict SafeSearch enabled for web results
- ✅ Keyword-based content blocking
- ✅ Double-layer content filtering

### Logging Security
- ⚠️ **Important**: Logs may contain user queries
- ✅ Logs are stored locally
- ✅ Debug logs are sanitized of sensitive patterns
- **Production Recommendation**: Implement PII detection in logs

## Recommendations for Production Deployment

### Critical
1. ✅ **Use HTTPS**: Deploy behind HTTPS/TLS
2. ✅ **Environment Variable Security**: Use secure secrets management (Azure Key Vault, AWS Secrets Manager)
3. ⚠️ **Encrypt Data at Rest**: Enable disk/folder encryption for `data/chats/`
4. ⚠️ **Regular Backups**: With encryption and access controls

### Highly Recommended
5. ⚠️ **PII Detection**: Implement automated PII scanning in logs
6. ⚠️ **Data Retention Automation**: Auto-delete old sessions
7. ⚠️ **Audit Logging**: Track all data access and deletions
8. ⚠️ **Rate Limiting**: Prevent abuse and DOS attacks
9. ⚠️ **Session Timeout**: Auto-expire inactive sessions

### Optional Enhancements
10. User authentication and authorization
11. End-to-end encryption for chat storage
12. Data anonymization for analytics
13. Privacy-preserving analytics
14. Consent management system

## Contact & Data Requests

For data access, deletion, or privacy concerns:
- **Email**: [Configure your support email]
- **Response Time**: Within 30 days as required by GDPR/CCPA

## Policy Updates

- **Last Updated**: 2025-12-03
- **Version**: 1.0
- Users will be notified of material changes to this policy

## Disclaimer

This chatbot is designed for customer support purposes only. Users should not share:
- Financial information (credit card numbers, bank accounts)
- Passwords or authentication credentials
- Personal health information
- Government-issued IDs or social security numbers

---

**Note**: This privacy policy should be reviewed by legal counsel before production deployment to ensure full compliance with applicable regulations in your jurisdiction.
