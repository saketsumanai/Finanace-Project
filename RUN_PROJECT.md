# 🚀 How to Run the Oil & Gas M&A Valuation Platform

## Complete Step-by-Step Guide

This guide will help you run the complete application on your MacBook.

---

## 📋 Prerequisites Check

Before starting, ensure you have these installed:

```bash
# Check Node.js (need v18+)
node --version

# Check npm
npm --version

# Check Python (need 3.11+)
python3 --version

# Check Docker
docker --version

# Check Docker Compose
docker-compose --version
```

If any are missing, install them first:
- **Node.js**: https://nodejs.org/ (download LTS version)
- **Python**: https://www.python.org/downloads/
- **Docker Desktop**: https://www.docker.com/products/docker-desktop/

---

## 🎯 Quick Start (Recommended)

### Option 1: Run with Docker Compose (Easiest)

```bash
# 1. Navigate to project directory
cd "/Users/saketsmac/Desktop/Finanace Project"

# 2. Start all services (PostgreSQL, Redis, Backend, Frontend, Celery)
docker-compose up

# Wait for all services to start (2-3 minutes)
# You'll see logs from all services

# When you see:
# - "Application startup complete" (Backend)
# - "ready in X ms" (Frontend)
# The application is ready!
```

**Access the application:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs

**To stop:**
```bash
# Press Ctrl+C in the terminal
# Then run:
docker-compose down
```

---

## 🔧 Option 2: Run Manually (For Development)

### Step 1: Start Database Services

```bash
# Terminal 1: Start PostgreSQL and Redis
cd "/Users/saketsmac/Desktop/Finanace Project"
docker-compose up postgres redis

# Keep this terminal running
```

### Step 2: Setup and Run Backend

```bash
# Terminal 2: Backend setup
cd "/Users/saketsmac/Desktop/Finanace Project/backend"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/oilgas_valuation
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["http://localhost:3000"]
EOF

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Backend will be available at http://localhost:8000
```

### Step 3: Start Celery Worker (Optional, for background tasks)

```bash
# Terminal 3: Celery worker
cd "/Users/saketsmac/Desktop/Finanace Project/backend"
source venv/bin/activate

celery -A app.tasks.celery_app worker --loglevel=info

# Keep this terminal running
```

### Step 4: Setup and Run Frontend

```bash
# Terminal 4: Frontend setup
cd "/Users/saketsmac/Desktop/Finanace Project/frontend"

# Install dependencies (first time only)
npm install

# Create .env file
cat > .env << EOF
VITE_API_URL=http://localhost:8000
EOF

# Start frontend development server
npm run dev

# Frontend will be available at http://localhost:3000
```

---

## 🧪 Testing the Application

### 1. Create a User Account

```bash
# Open your browser
open http://localhost:3000

# Click "Register"
# Fill in:
# - Email: test@example.com
# - Password: Test123!
# - Full Name: Test User
# Click "Register"
```

### 2. Login

```bash
# Use the credentials you just created
# Email: test@example.com
# Password: Test123!
# Click "Login"
```

### 3. Create a Project

```bash
# Click "Create Project"
# Fill in:
# - Name: "Permian Basin Acquisition"
# - Description: "M&A analysis for Permian Basin assets"
# Click "Create"
```

### 4. Test Financial Modeling

```bash
# Click on your project
# Click "Financial Modeling" button
# Follow the workflow:
# 1. Create Assumptions
# 2. Add Synergy Models
# 3. Create Scenario
# 4. Run Valuation
# 5. View Results
```

---

## 📊 Sample Data for Testing

### Create Assumptions

Use these values for quick testing:

**Basic Information:**
- Name: `Base Case Assumptions`
- Version: `1`

**Production Assumptions:**
- Decline Curve: `Hyperbolic`
- Decline Rate: `0.15` (15%)
- Hyperbolic b: `0.5`
- Oil Prices:
  - Year 1: `70`
  - Year 5: `75`
  - Year 10: `80`
- Gas Prices:
  - Year 1: `3.5`
  - Year 5: `3.8`
  - Year 10: `4.0`

**Cost Assumptions:**
- OPEX Inflation: `0.03` (3%)
- Transportation Cost: `2.5`
- Annual G&A: `1000000`
- CAPEX:
  - Year 1: `5000000`
  - Year 3: `2000000`

**Deal Assumptions:**
- Purchase Price: `50000000`
- Debt Amount: `30000000`
- Equity Amount: `20000000`
- Discount Rate: `0.12` (12%)
- Tax Rate: `0.21` (21%)
- Exit Multiple: `5.5`
- Forecast Years: `20`

### Add Synergy Model

**Synergy 1:**
- Category: `Operational Overhead`
- Description: `Consolidate field offices and eliminate duplicate G&A`
- Target Value: `2000000`
- Click "Standard" template

**Synergy 2:**
- Category: `Procurement Efficiency`
- Description: `Volume discounts and supplier consolidation`
- Target Value: `1500000`
- Click "Standard" template

### Create Scenarios

- Click "Base Case" button
- Click "Bull Case" button
- Click "Bear Case" button

### Run Valuation

- Select a scenario
- Click "Run Valuation"
- Wait for completion (5-10 seconds)
- View results in Results tab

---

## 🔍 Troubleshooting

### Issue: Port Already in Use

```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --reload --port 8001
```

### Issue: Database Connection Error

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Restart PostgreSQL
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

### Issue: Frontend Not Loading

```bash
# Clear npm cache
cd frontend
rm -rf node_modules package-lock.json
npm install

# Restart dev server
npm run dev
```

### Issue: Module Not Found (Backend)

```bash
# Reinstall dependencies
cd backend
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Issue: CORS Error

```bash
# Check backend .env file has correct CORS_ORIGINS
# Should be: CORS_ORIGINS=["http://localhost:3000"]

# Restart backend after changing
```

---

## 📱 Accessing the Application

### Main URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main web application |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/api/v1/docs | Interactive API documentation |
| ReDoc | http://localhost:8000/api/v1/redoc | Alternative API docs |

### API Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","version":"1.0.0"}
```

---

## 🛑 Stopping the Application

### If using Docker Compose:

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

### If running manually:

```bash
# Press Ctrl+C in each terminal:
# - Terminal 1: PostgreSQL/Redis
# - Terminal 2: Backend
# - Terminal 3: Celery (if running)
# - Terminal 4: Frontend
```

---

## 🔄 Restarting the Application

### Quick Restart (Docker Compose):

```bash
cd "/Users/saketsmac/Desktop/Finanace Project"
docker-compose restart
```

### Full Restart (Docker Compose):

```bash
cd "/Users/saketsmac/Desktop/Finanace Project"
docker-compose down
docker-compose up
```

---

## 📝 Useful Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Database Commands

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d oilgas_valuation

# List tables
\dt

# Query data
SELECT * FROM users;
SELECT * FROM projects;
SELECT * FROM assumptions;

# Exit
\q
```

### Backend Commands

```bash
cd backend
source venv/bin/activate

# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Run tests (when available)
pytest

# Check code style
flake8 app/
```

### Frontend Commands

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint

# Run tests (when available)
npm run test
```

---

## 🎯 Quick Reference

### Start Everything (Recommended)

```bash
cd "/Users/saketsmac/Desktop/Finanace Project"
docker-compose up
```

### Access Application

```bash
# Open in browser
open http://localhost:3000
```

### View API Documentation

```bash
# Open in browser
open http://localhost:8000/api/v1/docs
```

### Stop Everything

```bash
# Press Ctrl+C, then:
docker-compose down
```

---

## 🎓 Next Steps

1. **Register** a new user account
2. **Create** a project
3. **Navigate** to Financial Modeling
4. **Create** assumptions with the sample data above
5. **Add** synergy models
6. **Create** Bull/Base/Bear scenarios
7. **Run** valuations
8. **View** results with NPV, IRR, and other metrics

---

## 📞 Need Help?

### Check Status

```bash
# Check if services are running
docker-compose ps

# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000
```

### Common Issues

1. **Port conflicts**: Change ports in docker-compose.yml
2. **Database errors**: Run `docker-compose down -v` then `docker-compose up`
3. **Frontend errors**: Delete node_modules and reinstall
4. **Backend errors**: Check .env file and reinstall requirements

---

## ✅ Success Checklist

- [ ] Docker Desktop is running
- [ ] All services started successfully
- [ ] Frontend accessible at http://localhost:3000
- [ ] Backend accessible at http://localhost:8000
- [ ] Can register a new user
- [ ] Can create a project
- [ ] Can access Financial Modeling page
- [ ] Can create assumptions
- [ ] Can add synergy models
- [ ] Can create scenarios
- [ ] Can run valuations
- [ ] Can view results

---

**You're all set! Enjoy using the Oil & Gas M&A Valuation Platform! 🚀**
