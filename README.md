# 🚀 API SDK Generator

> Transform unstructured API documentation into production-ready TypeScript SDKs in under 60 seconds using AI.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.39.0-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-22%20passed-success.svg)](tests/)

---

## ✨ Features

- **🔍 Smart Documentation Analysis** - Analyzes docs before extraction to detect setup guides vs API references
- **🤖 Dual AI Support** - Choose between OpenAI (GPT-4-turbo) or Google Gemini for extraction
- **📄 Multi-Format Support** - Accepts URLs, PDFs, HTML files, or plain text
- **💡 Intelligent Guidance** - Recommends additional URLs when partial documentation detected
- **✏️ Interactive Review** - Edit and refine extracted API specifications
- **⚙️ Customizable SDKs** - Configure retry logic, rate limiting, and error handling
- **🔒 Security-First** - Built-in security scanning and sensitive data redaction
- **📦 Production-Ready** - Generates complete TypeScript projects with tests and documentation

---

## 🎯 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys)) OR
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/api-sdk-generator.git
cd api-sdk-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🎬 How It Works

### 6-Step Workflow

1. **📄 Input** - Provide API documentation via URL, file upload, or text paste
2. **🔍 Analysis** - AI analyzes documentation structure and provides guidance
3. **🤖 Configure** - Choose LLM provider (OpenAI/Gemini) and enter API key
4. **✏️ Review** - Verify and edit the extracted API specification
5. **⚙️ Customize** - Configure SDK features and package metadata
6. **📥 Download** - Get your complete TypeScript SDK as a ZIP file

### 🔍 Smart Documentation Analysis

Before extraction, the system analyzes your documentation to:
- Detect if you provided setup guides vs actual API references
- Count endpoints and identify missing sections
- Suggest additional URLs for complete API coverage
- Warn about partial documentation (e.g., only auth endpoints)

**Example**: If you provide `docs.example.com/setup`, the analyzer will detect it's a guide with 0 endpoints and suggest `docs.example.com/reference` instead.

### Example

```typescript
// Generated SDK usage
import { StripeAPI } from './stripe-sdk';

const client = new StripeAPI({
  apiKey: 'sk_test_...',
  baseURL: 'https://api.stripe.com/v1'
});

// Automatic retry logic and rate limiting
const charge = await client.createCharge({
  amount: 2000,
  currency: 'usd'
});
```

---

## 🏗️ Generated SDK Features

Every generated SDK includes:

- ✅ **TypeScript Support** - Full type definitions and IntelliSense
- ✅ **Retry Logic** - Exponential backoff with circuit breaker
- ✅ **Rate Limiting** - Token bucket algorithm
- ✅ **Error Handling** - Comprehensive error classes
- ✅ **Logging** - Configurable logging with sensitive data redaction
- ✅ **Authentication** - Support for API key, Bearer, OAuth2, and Basic auth
- ✅ **Documentation** - Auto-generated README with usage examples

---

## 📚 Documentation

- **[Deployment Guide](DEPLOYMENT.md)** - Deploy to Streamlit Cloud
- **[Project Summary](PROJECT_SUMMARY.md)** - Complete feature overview
- **[Examples](examples/)** - Sample API documentation (Stripe, GitHub, Twilio)

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

**Test Results**: 22/22 tests passing ✅

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **AI**: OpenAI GPT-4-turbo / Google Gemini 2.0 Flash
- **Validation**: Pydantic
- **Templates**: Jinja2
- **Testing**: Pytest

---

## � Security

- API keys stored in session only (never persisted)
- Automatic sensitive data redaction in logs
- Security scanning for generated code
- Input validation and sanitization
- HTTPS-only communication

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- OpenAI for GPT-4-turbo API
- Google for Gemini API
- Streamlit for the amazing framework
- The open-source community

---

## 📧 Contact

**Project Link**: [https://github.com/yourusername/api-sdk-generator](https://github.com/yourusername/api-sdk-generator)

---

<div align="center">
Made with ❤️ by the API SDK Generator team
</div>
