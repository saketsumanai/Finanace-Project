# 📦 GitHub Setup & Deployment Guide

Complete guide to push your project to GitHub and deploy it.

## 🎯 Quick Start

Your repository is already initialized! Follow these steps:

### Step 1: Configure Git (One-time setup)

```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

### Step 2: Create GitHub Repository

1. **Go to GitHub**: https://github.com/new
2. **Repository name**: `oil-gas-valuation-platform` (or your preferred name)
3. **Description**: "AI-powered Oil & Gas M&A Valuation Platform"
4. **Visibility**: Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. **Click**: "Create repository"

### Step 3: Push to GitHub

```bash
# Navigate to your project
cd "/Users/saketsmac/Desktop/Finanace Project"

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/oil-gas-valuation-platform.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main
```

**If you get an authentication error**, use a Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control)
4. Generate and copy the token
5. Use it as your password when pushing

### Step 4: Verify Upload

1. Go to your GitHub repository
2. You should see all files uploaded
3. README.md should display automatically

---

## 🔐 Protecting Sensitive Information

### Important: Never Commit Secrets!

Your `.gitignore` is already configured to exclude:
- `.env` files
- API keys
- Passwords
- Uploaded files
- Database files

### If You Accidentally Committed Secrets:

```bash
# Remove file from git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret/file" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin --force --all
```

**Then immediately**:
1. Rotate all exposed API keys
2. Change all passwords
3. Update Firebase credentials

---

## 📝 Repository Setup Checklist

### Essential Files (Already Created ✅)

- [x] `README.md` - Project documentation
- [x] `.gitignore` - Ignore sensitive files
- [x] `LICENSE` - MIT License
- [x] `.env.example` - Environment template
- [x] `DEPLOYMENT_GUIDE.md` - Deployment instructions
- [x] `docker-compose.yml` - Docker configuration

### Recommended Additions

#### 1. Create `.github/workflows/ci.yml` for CI/CD

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm test

  build:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker images
        run: docker-compose build
```

#### 2. Create `CONTRIBUTING.md`

```markdown
# Contributing Guidelines

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Code Style

- Backend: Follow PEP 8, use Black formatter
- Frontend: Follow ESLint rules, use Prettier
- Write meaningful commit messages

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Maintain test coverage above 80%
```

#### 3. Create Issue Templates

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. macOS, Ubuntu]
 - Browser: [e.g. Chrome, Safari]
 - Version: [e.g. 1.0.0]
```

---

## 🚀 Deployment Options

### Option 1: Deploy to Heroku (Easiest)

```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # macOS
# or download from https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(64))")
heroku config:set GEMINI_API_KEY=your-gemini-key
heroku config:set ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key
heroku config:set FIREBASE_PROJECT_ID=your-project-id

# Deploy
git push heroku main

# Open app
heroku open
```

### Option 2: Deploy to DigitalOcean App Platform

1. Go to: https://cloud.digitalocean.com/apps
2. Click "Create App"
3. Connect your GitHub repository
4. Configure:
   - **Backend**: Dockerfile in `backend/`
   - **Frontend**: Dockerfile in `frontend/`
   - **Database**: Add PostgreSQL
   - **Redis**: Add Redis
5. Set environment variables
6. Deploy!

### Option 3: Deploy to AWS (Advanced)

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed AWS deployment instructions.

### Option 4: Deploy to Your Own VPS

```bash
# SSH into your server
ssh root@your-server-ip

# Clone repository
git clone https://github.com/YOUR_USERNAME/oil-gas-valuation-platform.git
cd oil-gas-valuation-platform

# Copy and configure environment
cp .env.example .env
nano .env  # Edit with your values

# Start services
docker-compose up -d

# Set up Nginx reverse proxy (see DEPLOYMENT_GUIDE.md)
```

---

## 🔄 Continuous Deployment

### Automatic Deployment on Push

#### Using GitHub Actions + DigitalOcean

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to DigitalOcean
        uses: digitalocean/action-doctl@v2
        with:
          token: ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}
      
      - name: Trigger deployment
        run: |
          doctl apps create-deployment ${{ secrets.APP_ID }}
```

#### Using GitHub Actions + Heroku

```yaml
name: Deploy to Heroku

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "your-app-name"
          heroku_email: "your-email@example.com"
```

---

## 📊 Repository Management

### Branch Strategy

```
main (production)
  ├── develop (staging)
  │   ├── feature/new-charts
  │   ├── feature/export-excel
  │   └── bugfix/auth-issue
  └── hotfix/critical-bug
```

### Recommended Workflow

1. **Main branch**: Production-ready code
2. **Develop branch**: Integration branch
3. **Feature branches**: New features
4. **Hotfix branches**: Critical fixes

```bash
# Create develop branch
git checkout -b develop
git push -u origin develop

# Create feature branch
git checkout develop
git checkout -b feature/new-feature
# ... make changes ...
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
# Create Pull Request on GitHub

# Merge to develop, then to main
```

### Semantic Versioning

Use tags for releases:

```bash
# Create a release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# List tags
git tag -l
```

---

## 🔒 Security Best Practices

### 1. Use GitHub Secrets

Store sensitive data in GitHub Secrets:
1. Go to: Repository → Settings → Secrets and variables → Actions
2. Add secrets:
   - `GEMINI_API_KEY`
   - `ALPHA_VANTAGE_API_KEY`
   - `SECRET_KEY`
   - `DATABASE_URL`

### 2. Enable Branch Protection

1. Go to: Repository → Settings → Branches
2. Add rule for `main` branch:
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Include administrators

### 3. Enable Dependabot

1. Go to: Repository → Settings → Security & analysis
2. Enable:
   - ✅ Dependency graph
   - ✅ Dependabot alerts
   - ✅ Dependabot security updates

### 4. Add Security Policy

Create `SECURITY.md`:

```markdown
# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please email:
security@yourcompany.com

Do not create a public GitHub issue.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |
```

---

## 📈 Repository Badges

Add badges to your README.md:

```markdown
![Build Status](https://github.com/YOUR_USERNAME/oil-gas-valuation-platform/workflows/CI/badge.svg)
![License](https://img.shields.io/github/license/YOUR_USERNAME/oil-gas-valuation-platform)
![Stars](https://img.shields.io/github/stars/YOUR_USERNAME/oil-gas-valuation-platform)
![Issues](https://img.shields.io/github/issues/YOUR_USERNAME/oil-gas-valuation-platform)
```

---

## 🎉 You're All Set!

Your project is now:
- ✅ Version controlled with Git
- ✅ Ready to push to GitHub
- ✅ Documented with README
- ✅ Configured for deployment
- ✅ Protected with .gitignore
- ✅ Licensed (MIT)

### Next Steps:

1. **Push to GitHub** (see Step 3 above)
2. **Set up CI/CD** (optional but recommended)
3. **Deploy to production** (choose your platform)
4. **Share with the world!** 🚀

---

## 🆘 Troubleshooting

### "Permission denied (publickey)"

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
```

### "Repository not found"

```bash
# Check remote URL
git remote -v

# Update remote URL
git remote set-url origin https://github.com/YOUR_USERNAME/oil-gas-valuation-platform.git
```

### "Failed to push some refs"

```bash
# Pull first
git pull origin main --rebase

# Then push
git push origin main
```

---

**Need help?** Open an issue on GitHub or check the [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
