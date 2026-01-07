# Deployment Guide

## Streamlit Community Cloud Deployment

### Prerequisites

1. GitHub account
2. Streamlit Community Cloud account (free at https://streamlit.io/cloud)
3. OpenAI API key (for testing)

### Steps

1. **Push to GitHub**

```bash
git init
git add .
git commit -m "Initial commit: API SDK Generator"
git remote add origin https://github.com/yourusername/api-sdk-generator.git
git push -u origin main
```

2. **Connect to Streamlit Cloud**

- Go to https://share.streamlit.io/
- Click "New app"
- Select your repository
- Set main file path: `app.py`
- Click "Deploy"

3. **Configure Secrets (Optional)**

If you want to provide a default API key:

- Go to App Settings → Secrets
- Add:
```toml
OPENAI_API_KEY = "sk-..."
```

### Environment Variables

The app uses the following environment variables (all optional):

- `OPENAI_API_KEY`: Default OpenAI API key
- `LOG_LEVEL`: Logging level (default: INFO)
- `MAX_FILE_SIZE_MB`: Maximum upload size (default: 5)
- `LLM_TIMEOUT_SECONDS`: LLM request timeout (default: 120)

### Testing Deployment

1. Visit your deployed app URL
2. Test all 5 steps:
   - Input selection (URL, file, text)
   - LLM configuration
   - Review & edit
   - SDK configuration
   - Preview & download

### Troubleshooting

**Issue**: App crashes on startup
- Check logs in Streamlit Cloud dashboard
- Verify all dependencies in requirements.txt

**Issue**: LLM extraction fails
- Check API key is valid
- Verify network connectivity
- Check timeout settings

**Issue**: File upload fails
- Check file size limits
- Verify file format is supported

## Local Development

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/api-sdk-generator.git
cd api-sdk-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Production Considerations

### Security

- ✅ API keys stored in session only
- ✅ No persistent storage of sensitive data
- ✅ HTTPS-only communication
- ✅ Input validation and sanitization
- ✅ Generated code security scanning

### Performance

- Consider caching for:
  - Document fetching
  - LLM responses
  - Template rendering
- Monitor Streamlit Cloud resource usage
- Optimize for concurrent users

### Monitoring

- Use Streamlit Cloud analytics
- Monitor error rates
- Track generation success rates
- Collect user feedback

## Future Enhancements

- [ ] Add more LLM providers (Anthropic, Gemini)
- [ ] Support more languages (Python, Go, Java)
- [ ] Add webhook utilities
- [ ] Implement streaming support
- [ ] Add pagination support
- [ ] Create API for programmatic access
