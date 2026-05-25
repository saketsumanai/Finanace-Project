# ⚡ Quick Deploy Guide

## 🚀 Push to GitHub (5 minutes)

```bash
# 1. Configure Git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 2. Create repository on GitHub
# Go to: https://github.com/new
# Name: oil-gas-valuation-platform
# Click: Create repository

# 3. Push your code
cd "/Users/saketsmac/Desktop/Finanace Project"
git remote add origin https://github.com/YOUR_USERNAME/oil-gas-valuation-platform.git
git push -u origin main

# Done! ✅
```

---

## 🌐 Deploy to Heroku (10 minutes)

```bash
# 1. Install Heroku CLI
brew install heroku/brew/heroku

# 2. Login
heroku login

# 3. Create app
heroku create your-app-name

# 4. Add database & cache
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev

# 5. Set environment variables
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(64))")
heroku config:set GEMINI_API_KEY=AIzaSyCctuqFULVRYTgl3AMRHD1CyItf_0muX1Q
heroku config:set ALPHA_VANTAGE_API_KEY=421057MQ0P4ACM7T
heroku config:set FIREBASE_PROJECT_ID=oil-gas-f78c8

# 6. Deploy
git push heroku main

# 7. Open app
heroku open

# Done! ✅
```

---

## 🖥️ Deploy to VPS (30 minutes)

```bash
# 1. SSH into server
ssh root@your-server-ip

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt install docker-compose nginx certbot python3-certbot-nginx -y

# 3. Clone repository
git clone https://github.com/YOUR_USERNAME/oil-gas-valuation-platform.git
cd oil-gas-valuation-platform

# 4. Configure environment
cp .env.example .env
nano .env  # Add your API keys

# 5. Start services
docker-compose up -d

# 6. Set up SSL
certbot --nginx -d yourdomain.com

# Done! ✅
```

---

## 📦 What's Already Done

✅ Git repository initialized
✅ All files committed
✅ .gitignore configured
✅ README.md created
✅ LICENSE added (MIT)
✅ .env.example created
✅ Deployment guides written
✅ Docker configured

---

## 🔑 Your API Keys

**Gemini AI**: `AIzaSyCctuqFULVRYTgl3AMRHD1CyItf_0muX1Q`
**Alpha Vantage**: `421057MQ0P4ACM7T`
**Firebase Project**: `oil-gas-f78c8`

---

## 📚 Full Documentation

- **GitHub Setup**: [GITHUB_SETUP.md](./GITHUB_SETUP.md)
- **Deployment**: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- **User Guide**: [AI_CHAT_USER_GUIDE.md](./AI_CHAT_USER_GUIDE.md)
- **System Guide**: [SYSTEM_FULLY_OPERATIONAL.md](./SYSTEM_FULLY_OPERATIONAL.md)

---

## 🆘 Quick Help

**Push failed?**
```bash
git pull origin main --rebase
git push origin main
```

**Need SSH key?**
```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
cat ~/.ssh/id_ed25519.pub
# Add to GitHub: Settings → SSH keys
```

**Forgot to add remote?**
```bash
git remote add origin https://github.com/YOUR_USERNAME/repo-name.git
```

---

## ✨ You're Ready!

1. **Choose your deployment method** (Heroku is easiest)
2. **Follow the commands above**
3. **Your app will be live!** 🎉

**Questions?** Check the full guides or open an issue on GitHub.
