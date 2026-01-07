# 🚀 GitHub Deployment Guide

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Create a new repository:
   - **Name**: `api-sdk-generator`
   - **Description**: `🚀 Transform API documentation into production-ready TypeScript SDKs using AI`
   - **Visibility**: Public (or Private)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)

## Step 2: Push to GitHub

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/api-sdk-generator.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 3: Configure Repository Settings

### Add Topics (Optional)
Go to your repository → Settings → Topics and add:
- `ai`
- `sdk-generator`
- `typescript`
- `openai`
- `streamlit`
- `api-documentation`
- `code-generation`

### Add Description
Set the description to:
```
🚀 Transform API documentation into production-ready TypeScript SDKs using AI
```

### Add Website (Optional)
If you deploy to Streamlit Cloud, add the URL here.

## Step 4: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click "New app"
3. Select your repository: `YOUR_USERNAME/api-sdk-generator`
4. Set main file path: `app.py`
5. Click "Deploy"

### Add Secrets (Optional)
In Streamlit Cloud app settings → Secrets, add:

```toml
OPENAI_API_KEY = "sk-..."
```

This provides a default API key (optional - users can still provide their own).

## Step 5: Update README

After deployment, update the README.md with:
- Your actual GitHub username in URLs
- Streamlit Cloud deployment URL (if deployed)
- Your contact information

## 🎉 You're Done!

Your project is now live on GitHub and ready to share!

### Share Your Project

- **GitHub**: `https://github.com/YOUR_USERNAME/api-sdk-generator`
- **Streamlit**: `https://YOUR_APP_NAME.streamlit.app` (after deployment)

### Next Steps

1. ⭐ Star your own repo to show it's active
2. 📝 Add screenshots to README
3. 🎥 Create a demo video
4. 📢 Share on social media
5. 🤝 Invite contributors
