# 🤖 AI CHAT USER GUIDE - HOW TO USE

## ⚠️ IMPORTANT: YOU MUST BE LOGGED IN!

The AI chat requires authentication. If you're getting "Failed to get AI response", it's because you're not logged in.

---

## 🔐 STEP-BY-STEP GUIDE

### Step 1: Login First! ✅
```
1. Go to: http://localhost:5173/login
2. Choose login method:
   - Click "Sign in with Google" (recommended)
   - Or use email/password
3. Complete login process
4. You'll be redirected to dashboard
```

### Step 2: Verify You're Logged In ✅
```
Look for these signs:
- Your name/email in the header
- "Logout" button visible
- Dashboard accessible
- Projects page accessible
```

### Step 3: Go to AI Chat ✅
```
1. Click "AI Chat" in navigation
2. Or go to: http://localhost:5173/ai-chat
3. You should see the chat interface
```

### Step 4: Start Chatting! ✅
```
Ask anything:
- "What are current oil prices?"
- "What assumptions should I use?"
- "Analyze https://www.exxonmobil.com"
- "Research oil and gas M&A trends"
```

---

## 🚫 COMMON ERRORS & FIXES

### Error: "Failed to get AI response"

**Cause:** Not logged in or token expired

**Fix:**
1. Check if you're logged in (see your name in header)
2. If not logged in:
   - Go to http://localhost:5173/login
   - Login with Google or email/password
   - Return to AI chat
3. If already logged in:
   - Logout and login again
   - Refresh the page
   - Try again

### Error: "401 Unauthorized"

**Cause:** Authentication token missing or invalid

**Fix:**
1. Logout completely
2. Clear browser cookies (optional)
3. Login again
4. Go to AI chat
5. Try your question again

### Error: "Network Error"

**Cause:** Backend not running or connection issue

**Fix:**
1. Check backend is running:
   ```bash
   docker-compose ps
   ```
2. If not running:
   ```bash
   docker-compose up -d
   ```
3. Wait 10 seconds
4. Refresh page
5. Try again

---

## ✅ VERIFICATION STEPS

### 1. Check You're Logged In:
```
✓ Can you see your name in the header?
✓ Can you see "Logout" button?
✓ Can you access Dashboard?
✓ Can you access Projects?

If YES to all → You're logged in ✅
If NO to any → Login first!
```

### 2. Check Backend is Running:
```bash
# Run this command:
curl http://localhost:8000/health

# Should return:
{"status":"healthy","version":"1.0.0"}

If you get this → Backend is working ✅
If error → Start backend with: docker-compose up -d
```

### 3. Test AI Chat:
```
1. Login ✅
2. Go to AI Chat ✅
3. Type: "Hello"
4. Click Send
5. Wait for response

If you get response → Everything working! ✅
If error → Follow troubleshooting below
```

---

## 🔧 TROUBLESHOOTING

### Problem: Still getting "Failed to get AI response" after login

**Solution 1: Hard Refresh**
```
1. Press Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
2. This clears cache and reloads
3. Login again
4. Try AI chat
```

**Solution 2: Clear Browser Data**
```
1. Open browser settings
2. Clear browsing data
3. Select "Cookies" and "Cached images"
4. Clear data
5. Go to http://localhost:5173
6. Login again
7. Try AI chat
```

**Solution 3: Try Different Browser**
```
1. Open Chrome/Firefox/Safari
2. Go to http://localhost:5173
3. Login
4. Try AI chat
```

**Solution 4: Restart Services**
```bash
# Stop services
docker-compose down

# Start services
docker-compose up -d

# Wait 30 seconds
sleep 30

# Open browser
# Go to http://localhost:5173
# Login and try AI chat
```

---

## 💬 EXAMPLE CONVERSATIONS

### Example 1: Market Data
```
You: "What are current oil prices?"

AI: [Fetches real-time data]

**CURRENT MARKET DATA:**
- WTI Crude Oil: $100.32/bbl
- Brent Crude: $105.20/bbl
- Natural Gas: $3.45/MMBtu

Based on current prices, here's my analysis...
[Detailed 2000+ word response]
```

### Example 2: Company Analysis
```
You: "Analyze https://www.exxonmobil.com"

AI: [Scrapes website and analyzes]

## COMPANY INTELLIGENCE

**Company Overview:**
ExxonMobil is a global integrated oil and gas company...

**Current Market Data:**
- Stock Price: $154.92
- Market Cap: $450B

**M&A Assessment:**
[Comprehensive analysis]
```

### Example 3: Research
```
You: "Research oil and gas M&A trends"

AI: [Searches and analyzes multiple sources]

## RESEARCH REPORT

**Executive Summary:**
Based on analysis of 5 sources...

**Key Findings:**
- Deal volume up 15% YoY
- Average deal size: $2.5B

[Professional research report]
```

---

## 🎯 TIPS FOR BEST RESULTS

### 1. Be Specific:
```
❌ Bad: "Tell me about oil"
✅ Good: "What are current WTI oil prices and how do they affect M&A valuations?"
```

### 2. Ask Follow-up Questions:
```
First: "What assumptions should I use?"
Then: "What decline rate for a mature field?"
Then: "How do I calculate that?"
```

### 3. Use Context:
```
"I'm valuing a $50M acquisition in the Permian Basin. 
What assumptions should I use given current market conditions?"
```

### 4. Upload Files:
```
- Click 📎 icon
- Upload CSV file
- AI will analyze automatically
```

### 5. Use Quick Actions:
```
When on a project:
- "Analyze Project"
- "Suggest Assumptions"
- "Identify Synergies"
- "Assess Risks"
```

---

## 📊 WHAT AI CAN DO

### 1. Market Intelligence:
- ✅ Real-time oil & gas prices
- ✅ Stock market data
- ✅ Economic indicators
- ✅ Market trends

### 2. Company Analysis:
- ✅ Scrape company websites
- ✅ Analyze financials
- ✅ Compare competitors
- ✅ M&A intelligence

### 3. Research:
- ✅ Research any topic
- ✅ Multi-source analysis
- ✅ Professional reports
- ✅ Credibility assessment

### 4. Valuation Support:
- ✅ Recommend assumptions
- ✅ Analyze results
- ✅ Suggest synergies
- ✅ Generate reports

### 5. Data Analysis:
- ✅ Analyze CSV files
- ✅ Extract insights
- ✅ Identify patterns
- ✅ Quality assessment

---

## 🎉 SUCCESS CHECKLIST

Before using AI chat, make sure:

- [ ] Backend is running (`docker-compose ps`)
- [ ] Frontend is accessible (http://localhost:5173)
- [ ] You are logged in (see your name in header)
- [ ] You can access Dashboard
- [ ] You can access Projects
- [ ] AI Chat page loads
- [ ] You can type messages
- [ ] Send button is clickable

If ALL checked ✅ → You're ready to use AI chat!

---

## 📞 QUICK HELP

### Still Not Working?

1. **Check this first:**
   ```bash
   # Are services running?
   docker-compose ps
   
   # Is backend healthy?
   curl http://localhost:8000/health
   ```

2. **Restart everything:**
   ```bash
   docker-compose restart
   ```

3. **Try this sequence:**
   - Logout
   - Close browser
   - Open browser
   - Go to http://localhost:5173/login
   - Login
   - Go to AI chat
   - Try again

4. **Last resort:**
   ```bash
   docker-compose down
   docker-compose up --build -d
   # Wait 1 minute
   # Then try again
   ```

---

## 🎊 YOU'RE READY!

**Follow these steps:**
1. ✅ Login at http://localhost:5173/login
2. ✅ Go to AI Chat
3. ✅ Ask your question
4. ✅ Get comprehensive AI response

**Your AI can:**
- Provide detailed analysis (5,000-20,000 characters)
- Access real-time market data
- Scrape and analyze websites
- Research any topic
- Analyze any content
- Support M&A decisions

**Start chatting now!** 🚀
