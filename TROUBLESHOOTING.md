# 🔧 Troubleshooting Guide

## ✅ Quick Health Check

Run these commands to verify everything is working:

```bash
# Check Docker containers
docker ps

# Expected output: 5 containers running
# - valuation_frontend
# - valuation_backend
# - valuation_postgres
# - valuation_redis
# - valuation_celery

# Test backend API
curl http://localhost:8000/health

# Expected: {"status":"healthy","version":"1.0.0"}

# Test frontend
curl -I http://localhost:5173

# Expected: HTTP/1.1 200 OK
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "Cannot connect to backend"

**Symptoms:**
- Frontend shows "Network Error"
- API calls fail
- Login doesn't work

**Solution:**
```bash
# Check if backend is running
docker ps | grep valuation_backend

# If not running, restart it
docker-compose restart backend

# Check backend logs
docker logs valuation_backend --tail 50

# If you see errors, restart all services
docker-compose down
docker-compose up -d
```

---

### Issue 2: "Generate Smart Data button doesn't work"

**Symptoms:**
- Button click does nothing
- No success message
- No data generated

**Solution:**
```bash
# Check backend logs for errors
docker logs valuation_backend --tail 100 | grep -i error

# Verify the endpoint exists
curl -X POST http://localhost:8000/api/v1/upload/generate-smart-data \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "project_id=1"

# If 404 error, restart backend
docker-compose restart backend

# If 401 error, you need to login again
# Go to frontend and login to get new token
```

**Frontend Check:**
```bash
# Check frontend logs
docker logs valuation_frontend --tail 50

# Look for any JavaScript errors
# Open browser console (F12) and check for errors
```

---

### Issue 3: "Valuation fails to run"

**Symptoms:**
- "Run Valuation" button shows error
- No results appear
- Error message in toast

**Solution:**

**Step 1: Verify data exists**
```bash
# Connect to database
docker exec -it valuation_postgres psql -U postgres -d valuation_db

# Check if production data exists
SELECT COUNT(*) FROM production_data WHERE project_id = YOUR_PROJECT_ID;

# Check if financial data exists
SELECT COUNT(*) FROM financial_data WHERE project_id = YOUR_PROJECT_ID;

# Exit
\q
```

**Step 2: Check assumptions**
```bash
# In database
SELECT * FROM assumptions WHERE project_id = YOUR_PROJECT_ID;

# Verify all required fields are set:
# - decline_rate
# - discount_rate
# - tax_rate
# - purchase_price
```

**Step 3: Check backend logs**
```bash
docker logs valuation_backend --tail 100 | grep -i "valuation\|error"
```

**Step 4: If still failing, regenerate data**
1. Go to Modeling page
2. Click "Generate Smart Data with AI" again
3. Wait for success message
4. Try running valuation again

---

### Issue 4: "Charts not displaying"

**Symptoms:**
- Results page shows metrics but no charts
- Blank spaces where charts should be
- Console errors about Chart.js

**Solution:**

**Check browser console:**
```
1. Press F12 to open developer tools
2. Go to Console tab
3. Look for errors related to "Chart" or "canvas"
```

**Common fixes:**
```bash
# Restart frontend
docker-compose restart frontend

# Clear browser cache
# Chrome: Ctrl+Shift+Delete
# Firefox: Ctrl+Shift+Delete
# Safari: Cmd+Option+E

# Try different browser
# Recommended: Chrome or Firefox
```

---

### Issue 5: "Database connection error"

**Symptoms:**
- Backend logs show "could not connect to database"
- API returns 500 errors
- Cannot create projects

**Solution:**
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check PostgreSQL logs
docker logs valuation_postgres --tail 50

# Restart PostgreSQL
docker-compose restart postgres

# Wait 10 seconds for it to be healthy
docker ps | grep postgres
# Should show "healthy" in STATUS

# Restart backend to reconnect
docker-compose restart backend
```

---

### Issue 6: "Old password doesn't work"

**Symptoms:**
- Cannot login with old credentials
- "Invalid credentials" error

**Explanation:**
Password hashing was changed from passlib to bcrypt. Old passwords won't work.

**Solution:**
```
1. Click "Register" to create a new account
2. Use a new email or different email
3. Login with new credentials
```

**Alternative: Reset database (WARNING: Deletes all data)**
```bash
docker-compose down -v
docker-compose up -d
# Wait 30 seconds for services to start
# Then register a new account
```

---

### Issue 7: "Port already in use"

**Symptoms:**
- Docker fails to start
- Error: "port 8000 is already allocated"
- Error: "port 5173 is already allocated"

**Solution:**
```bash
# Find what's using the port
lsof -i :8000
lsof -i :5173

# Kill the process
kill -9 <PID>

# Or change ports in docker-compose.yml
# Edit docker-compose.yml:
# ports:
#   - "8001:8000"  # Change 8000 to 8001
#   - "5174:5173"  # Change 5173 to 5174

# Restart
docker-compose down
docker-compose up -d
```

---

### Issue 8: "Frontend shows blank page"

**Symptoms:**
- http://localhost:5173 shows white screen
- No content loads
- Browser console shows errors

**Solution:**
```bash
# Check frontend logs
docker logs valuation_frontend --tail 100

# Look for build errors or missing dependencies

# Rebuild frontend
docker-compose down
docker-compose build frontend
docker-compose up -d

# If still failing, check browser console (F12)
# Look for JavaScript errors
```

---

### Issue 9: "Assumptions form validation errors"

**Symptoms:**
- Cannot submit assumptions form
- Red error messages
- Form fields highlighted in red

**Solution:**

**Check required fields:**
- Name: Must not be empty
- Version: Must not be empty
- Forecast Years: Must be > 0
- Decline Rate: Must be between 0 and 1 (e.g., 0.15 for 15%)
- Discount Rate: Must be between 0 and 1 (e.g., 0.12 for 12%)
- Tax Rate: Must be between 0 and 1 (e.g., 0.21 for 21%)
- Purchase Price: Must be > 0

**Array fields format:**
- Oil Price Forecast: [75, 78, 80, 82, 85]
- Gas Price Forecast: [3.5, 3.7, 3.9, 4.0, 4.2]
- CAPEX Schedule: [5000000, 1000000, 500000]

**Common mistakes:**
- Using percentages instead of decimals (15% → 0.15)
- Missing commas in arrays
- Using strings instead of numbers
- Negative values where positive required

---

### Issue 10: "Docker containers keep restarting"

**Symptoms:**
- `docker ps` shows containers restarting
- Services not accessible
- Logs show crash errors

**Solution:**
```bash
# Check which container is failing
docker ps -a

# Check logs of failing container
docker logs <container_name> --tail 100

# Common causes:

# 1. Database not ready
# Solution: Wait 30 seconds after starting

# 2. Missing environment variables
# Solution: Check .env file exists in backend/

# 3. Port conflicts
# Solution: Change ports in docker-compose.yml

# 4. Out of memory
# Solution: Increase Docker memory limit
# Docker Desktop → Settings → Resources → Memory

# 5. Corrupted volumes
# Solution: Remove volumes and restart
docker-compose down -v
docker-compose up -d
```

---

## 🔍 Debugging Commands

### Check all container status
```bash
docker-compose ps
```

### View logs for all services
```bash
docker-compose logs -f
```

### View logs for specific service
```bash
docker logs valuation_backend -f
docker logs valuation_frontend -f
docker logs valuation_postgres -f
```

### Restart specific service
```bash
docker-compose restart backend
docker-compose restart frontend
```

### Restart all services
```bash
docker-compose restart
```

### Stop all services
```bash
docker-compose down
```

### Start all services
```bash
docker-compose up -d
```

### Rebuild and restart
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

### Check database
```bash
# Connect to PostgreSQL
docker exec -it valuation_postgres psql -U postgres -d valuation_db

# List tables
\dt

# Check users
SELECT id, email, full_name FROM users;

# Check projects
SELECT id, name, owner_id, deal_size FROM projects;

# Check production data
SELECT COUNT(*) FROM production_data;

# Check financial data
SELECT COUNT(*) FROM financial_data;

# Exit
\q
```

### Check Redis
```bash
# Connect to Redis
docker exec -it valuation_redis redis-cli

# Check keys
KEYS *

# Exit
exit
```

---

## 📊 Performance Issues

### Issue: "Valuation takes too long"

**Normal times:**
- Data generation: 2-3 seconds
- Valuation calculation: 3-5 seconds
- Chart rendering: <1 second

**If slower:**
```bash
# Check CPU usage
docker stats

# If high CPU:
# 1. Close other applications
# 2. Reduce forecast years (20 → 10)
# 3. Increase Docker CPU limit

# Check memory usage
docker stats

# If high memory:
# 1. Restart services
# 2. Increase Docker memory limit
```

---

## 🔐 Security Issues

### Issue: "JWT token expired"

**Symptoms:**
- Suddenly logged out
- API returns 401 errors
- "Unauthorized" messages

**Solution:**
```
1. Simply login again
2. Token expires after 24 hours (normal behavior)
3. Your data is safe, just need to re-authenticate
```

---

## 🆘 Nuclear Option (Last Resort)

If nothing else works, completely reset everything:

```bash
# WARNING: This deletes ALL data!

# Stop and remove everything
docker-compose down -v

# Remove all images
docker-compose rm -f

# Rebuild from scratch
docker-compose build --no-cache

# Start fresh
docker-compose up -d

# Wait 30 seconds for services to start

# Check status
docker ps

# All containers should show "Up" and "healthy"

# Open frontend
open http://localhost:5173

# Register a new account and start fresh
```

---

## 📞 Getting Help

### Check these files first:
1. `SYSTEM_STATUS.md` - Current system status
2. `COMPLETE_SYSTEM_GUIDE.md` - Full user guide
3. `VISUAL_WORKFLOW.md` - Step-by-step workflow

### Collect this information:
```bash
# System info
docker --version
docker-compose --version

# Container status
docker ps -a

# Recent logs
docker logs valuation_backend --tail 100 > backend.log
docker logs valuation_frontend --tail 100 > frontend.log

# Browser console errors (F12 → Console → Copy all errors)
```

---

## ✅ Verification Checklist

After fixing issues, verify everything works:

- [ ] All 5 Docker containers running
- [ ] Backend health check returns 200
- [ ] Frontend loads at http://localhost:5173
- [ ] Can register new account
- [ ] Can login successfully
- [ ] Can create project
- [ ] Can generate AI data
- [ ] Can create assumptions
- [ ] Can create scenario
- [ ] Can run valuation
- [ ] Can view results with charts

---

## 🎯 Prevention Tips

### To avoid issues:

1. **Always wait for services to be healthy**
   ```bash
   docker ps
   # Wait until STATUS shows "healthy" for postgres and redis
   ```

2. **Don't modify database directly**
   - Use the API/UI instead
   - Direct database changes can break things

3. **Keep Docker updated**
   ```bash
   docker --version
   # Should be 20.10+ or newer
   ```

4. **Give Docker enough resources**
   - Memory: At least 4GB
   - CPU: At least 2 cores
   - Disk: At least 10GB free

5. **Use Chrome or Firefox**
   - Best compatibility
   - Better developer tools

6. **Clear browser cache regularly**
   - Prevents stale JavaScript
   - Fixes weird UI issues

---

**Still having issues?** Check the logs and error messages carefully. Most issues are clearly indicated in the logs.

**System working?** Great! Check out `COMPLETE_SYSTEM_GUIDE.md` to learn all the features.
