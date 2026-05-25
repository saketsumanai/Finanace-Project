# 📦 Installation Guide for Oil & Gas M&A Valuation Platform

## Current Status

Your system needs the following software installed to run the application:
- ✅ macOS (Already have)
- ❌ Docker Desktop
- ❌ Node.js and npm
- ❓ Python 3 (need to verify)

---

## 🎯 Recommended Installation Path

### Option 1: Docker Desktop (Easiest - Recommended)

Docker Desktop will allow you to run the entire application with a single command.

#### Step 1: Install Docker Desktop

1. **Download Docker Desktop for Mac:**
   - Visit: https://www.docker.com/products/docker-desktop/
   - Click "Download for Mac"
   - Choose the version for your Mac:
     - **Apple Silicon (M1/M2/M3)**: Download "Mac with Apple chip"
     - **Intel Mac**: Download "Mac with Intel chip"

2. **Install Docker Desktop:**
   - Open the downloaded `.dmg` file
   - Drag Docker icon to Applications folder
   - Open Docker from Applications
   - Follow the setup wizard
   - Docker will ask for permissions - grant them
   - Wait for Docker to start (you'll see a whale icon in menu bar)

3. **Verify Installation:**
   ```bash
   # Open Terminal and run:
   docker --version
   docker-compose --version
   ```

#### Step 2: Run the Application

Once Docker is installed:

```bash
# 1. Open Terminal
# 2. Navigate to project
cd "/Users/saketsmac/Desktop/Finanace Project"

# 3. Start all services
docker-compose up

# Wait 2-3 minutes for all services to start
# When you see "Application startup complete", it's ready!
```

#### Step 3: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/v1/docs

---

### Option 2: Manual Installation (For Developers)

If you prefer to run services individually:

#### Step 1: Install Homebrew (Package Manager)

```bash
# Open Terminal and run:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Follow the instructions to add Homebrew to your PATH
```

#### Step 2: Install Node.js

```bash
# Install Node.js (includes npm)
brew install node@18

# Verify installation
node --version  # Should show v18.x.x
npm --version   # Should show 9.x.x or higher
```

#### Step 3: Install Python

```bash
# Check if Python 3 is already installed
python3 --version

# If not installed or version is < 3.11:
brew install python@3.11

# Verify installation
python3 --version  # Should show 3.11.x
```

#### Step 4: Install PostgreSQL

```bash
# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL
brew services start postgresql@15

# Create database
createdb oilgas_valuation
```

#### Step 5: Install Redis

```bash
# Install Redis
brew install redis

# Start Redis
brew services start redis
```

#### Step 6: Setup Backend

```bash
# Navigate to backend
cd "/Users/saketsmac/Desktop/Finanace Project/backend"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << 'EOF'
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/oilgas_valuation
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-change-in-production-please-use-long-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["http://localhost:3000"]
PROJECT_NAME=Oil & Gas M&A Valuation Platform
VERSION=1.0.0
ENVIRONMENT=development
EOF

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Keep this terminal open. Backend will run at http://localhost:8000

#### Step 7: Setup Frontend (New Terminal)

```bash
# Open a NEW terminal window
# Navigate to frontend
cd "/Users/saketsmac/Desktop/Finanace Project/frontend"

# Install dependencies
npm install

# Create .env file
cat > .env << 'EOF'
VITE_API_URL=http://localhost:8000
EOF

# Start frontend development server
npm run dev
```

Keep this terminal open. Frontend will run at http://localhost:3000

---

## 🚀 Quick Start Commands

### After Installing Docker Desktop:

```bash
# Terminal 1: Start everything
cd "/Users/saketsmac/Desktop/Finanace Project"
docker-compose up

# Access at http://localhost:3000
```

### After Manual Installation:

```bash
# Terminal 1: Backend
cd "/Users/saketsmac/Desktop/Finanace Project/backend"
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd "/Users/saketsmac/Desktop/Finanace Project/frontend"
npm run dev
```

---

## 📋 Installation Checklist

### Docker Desktop Method:
- [ ] Download Docker Desktop for Mac
- [ ] Install Docker Desktop
- [ ] Start Docker Desktop
- [ ] Verify with `docker --version`
- [ ] Run `docker-compose up`
- [ ] Access http://localhost:3000

### Manual Method:
- [ ] Install Homebrew
- [ ] Install Node.js (`brew install node@18`)
- [ ] Install Python (`brew install python@3.11`)
- [ ] Install PostgreSQL (`brew install postgresql@15`)
- [ ] Install Redis (`brew install redis`)
- [ ] Setup backend (venv, pip install, migrations)
- [ ] Setup frontend (npm install)
- [ ] Start backend (`uvicorn app.main:app --reload`)
- [ ] Start frontend (`npm run dev`)
- [ ] Access http://localhost:3000

---

## 🎯 Recommended: Docker Desktop

**Why Docker Desktop is recommended:**
- ✅ Single installation
- ✅ One command to start everything
- ✅ No manual database setup
- ✅ Consistent environment
- ✅ Easy to stop/start
- ✅ No conflicts with other software

**Installation time:** ~10 minutes
**Running time:** 2-3 minutes to start

---

## 📞 Next Steps

1. **Choose your installation method:**
   - **Easy**: Install Docker Desktop (recommended)
   - **Advanced**: Manual installation

2. **Follow the installation steps above**

3. **Once installed, run the application:**
   - Docker: `docker-compose up`
   - Manual: Start backend and frontend separately

4. **Access the application:**
   - Open browser: http://localhost:3000
   - Register a new user
   - Create a project
   - Start financial modeling!

---

## 🆘 Need Help?

### Docker Desktop Installation Issues:

**Issue: "Docker Desktop requires macOS 11 or newer"**
- Solution: Update your macOS to Big Sur (11) or later

**Issue: "Docker Desktop won't start"**
- Solution: Restart your Mac and try again
- Check System Preferences → Security & Privacy for permissions

**Issue: "Cannot connect to Docker daemon"**
- Solution: Make sure Docker Desktop is running (whale icon in menu bar)

### Manual Installation Issues:

**Issue: "command not found: brew"**
- Solution: Install Homebrew first (see Step 1)

**Issue: "Permission denied"**
- Solution: Add `sudo` before the command
- Example: `sudo brew install node@18`

**Issue: "Port already in use"**
- Solution: Change the port or kill the process using it
- Find process: `lsof -i :8000`
- Kill process: `kill -9 <PID>`

---

## ✅ Verification

After installation, verify everything works:

```bash
# Check Docker (if using Docker method)
docker --version
docker-compose --version

# Check Node.js (if using manual method)
node --version
npm --version

# Check Python (if using manual method)
python3 --version

# Check if services are running
curl http://localhost:8000/health
curl http://localhost:3000
```

---

## 🎉 Success!

Once you see the application running at http://localhost:3000, you're ready to:

1. **Register** a new user account
2. **Create** a project
3. **Navigate** to Financial Modeling
4. **Create** assumptions
5. **Add** synergy models
6. **Run** valuations
7. **View** results!

---

**For detailed usage instructions, see: RUN_PROJECT.md**
