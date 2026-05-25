# How to Use the Oil & Gas M&A Valuation Platform

## ✅ What's Working (Backend APIs)

All backend APIs are fully functional:
- ✅ User registration & login
- ✅ Project creation
- ✅ File upload (production & financial data)
- ✅ Assumptions creation
- ✅ Synergy models
- ✅ Scenarios
- ✅ Valuation calculations

## ✅ What's Working (Frontend UI)

The frontend has these pages:
- ✅ Login/Register pages
- ✅ Projects list page
- ✅ Project detail page
- ✅ **Modeling page** (Assumptions, Synergies, Scenarios, Results)

## 🎯 How to Access Everything

### Step 1: Register a New Account

**IMPORTANT**: Your old password won't work because we fixed the password hashing. You need to register a new account.

1. Go to: http://localhost:5173
2. Click "Register"
3. Enter:
   - Email: anything@example.com
   - Password: TestPass123! (or any password)
   - Full Name: Your Name
4. Click "Register"

### Step 2: Login

1. Use the email and password you just registered
2. Click "Login"
3. You'll be redirected to the Projects page

### Step 3: Create a Project

1. Click "Create New Project" button
2. Fill in:
   - **Name**: e.g., "Permian Basin Acquisition"
   - **Description**: e.g., "Acquisition of producing assets"
   - **Project Type**: Select "Acquisition" (REQUIRED!)
   - **Target Company**: e.g., "Target Energy LLC"
   - **Deal Size**: e.g., 75000000
3. Click "Create Project"

### Step 4: Go to Financial Modeling

1. Click on your project to open it
2. Click the "Financial Modeling" button
3. You'll see 4 tabs:
   - **Assumptions** - Create modeling parameters
   - **Synergies** - Add synergy models
   - **Scenarios** - Create Bull/Base/Bear cases
   - **Results** - View valuation results

### Step 5: Create Assumptions

1. On the **Assumptions** tab, click "Create Assumptions"
2. Fill in the form:
   - **Name**: e.g., "Base Case Assumptions"
   - **Version**: 1
   - **Decline Curve Type**: exponential, hyperbolic, or harmonic
   - **Decline Rate**: e.g., 0.15 (15%)
   - **Oil Price Forecast**: Add years and prices
   - **Gas Price Forecast**: Add years and prices
   - **OPEX Inflation Rate**: e.g., 0.03 (3%)
   - **CAPEX Schedule**: Add years and amounts
   - **Transportation Cost**: e.g., 2.50
   - **G&A Annual**: e.g., 500000
   - **Purchase Price**: e.g., 50000000
   - **Debt Amount**: e.g., 30000000
   - **Equity Amount**: e.g., 20000000
   - **Discount Rate**: e.g., 0.10 (10%)
   - **Tax Rate**: e.g., 0.21 (21%)
   - **Exit Multiple**: e.g., 5.5
   - **Forecast Years**: e.g., 20
3. Click "Create"

### Step 6: Add Synergies (Optional)

1. Go to the **Synergies** tab
2. Click "Add Synergy Model"
3. Fill in:
   - **Category**: operational_overhead, procurement_efficiency, workforce_consolidation, or shared_infrastructure
   - **Description**: What the synergy is
   - **Target Value**: Annual synergy at full realization
   - **Realization Schedule**: Add years and percentages
4. Click "Create"

### Step 7: Create Scenarios

1. Go to the **Scenarios** tab
2. Click one of:
   - "Bull Case" - Optimistic scenario
   - "Base Case" - Most likely scenario
   - "Bear Case" - Conservative scenario
3. A scenario will be created automatically

### Step 8: Run Valuation

1. On the **Scenarios** tab, find your scenario
2. Click "Run Valuation" button
3. Wait for the calculation to complete
4. You'll be redirected to the **Results** tab

### Step 9: View Results

On the **Results** tab, you'll see:
- **NPV** (Net Present Value)
- **IRR** (Internal Rate of Return)
- **Payback Period**
- **ROIC** (Return on Invested Capital)
- **ROI** (Return on Investment)
- **Profitability Index**
- **Terminal Value**
- **Annual Forecast Data** (table with production, revenue, costs, cash flows)
- **Investment Decision Indicators** (Yes/No recommendations)

## 📊 What's Currently Missing

### Missing Visualizations:
- ❌ Charts/graphs for production decline
- ❌ Charts for cash flow waterfall
- ❌ Charts for scenario comparison
- ❌ Charts for sensitivity analysis

### Missing Features:
- ❌ File upload UI (API works, but no UI button)
- ❌ Dashboard analytics
- ❌ Export to Excel/PDF
- ❌ Sensitivity analysis
- ❌ Monte Carlo simulation

## 🔧 What Needs to Be Built

### 1. Add Charts to Results Page
Need to add:
- Production decline curve chart
- Cash flow waterfall chart
- Revenue vs costs chart
- Scenario comparison chart

### 2. Add File Upload UI
Need to add upload buttons to:
- Project detail page
- Modeling page

### 3. Add Dashboard Analytics
Need to create:
- Portfolio overview
- Project comparison
- Key metrics summary

### 4. Add Data Visualization Page
Need to create:
- Interactive charts
- Drill-down capabilities
- Export functionality

## 🎯 Quick Test (Command Line)

If you want to test without the UI:

```bash
# 1. Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "Test123!", "full_name": "Test User"}'

# 2. Login (save the token)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "Test123!"}'

# 3. Create project (use token from step 2)
TOKEN="your_token_here"
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "description": "Test", "project_type": "Acquisition"}'

# 4. Create assumptions (use project_id from step 3)
curl -X POST http://localhost:8000/api/v1/modeling/assumptions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "version": 1,
    "name": "Base Case",
    "decline_curve_type": "exponential",
    "decline_rate": 0.15,
    "oil_price_forecast": [{"year": 1, "price": 75.00}],
    "gas_price_forecast": [{"year": 1, "price": 3.50}],
    "opex_inflation_rate": 0.03,
    "capex_schedule": [{"year": 1, "amount": 5000000}],
    "transportation_cost_per_unit": 2.50,
    "ga_annual": 500000,
    "purchase_price": 50000000,
    "debt_amount": 30000000,
    "equity_amount": 20000000,
    "discount_rate": 0.10,
    "tax_rate": 0.21,
    "exit_multiple": 5.5,
    "forecast_years": 20
  }'
```

## 📝 Summary

**What works:**
- ✅ Complete backend API
- ✅ User authentication
- ✅ Project management
- ✅ Financial modeling (assumptions, synergies, scenarios)
- ✅ Valuation calculations
- ✅ Results display (metrics + table)

**What's missing:**
- ❌ Charts/graphs
- ❌ File upload UI
- ❌ Dashboard analytics
- ❌ Advanced visualizations

**To use the platform:**
1. Register a new account (old passwords won't work)
2. Create a project
3. Go to Financial Modeling
4. Create assumptions
5. Create scenarios
6. Run valuation
7. View results

The core functionality is there, but the visual analytics and charts need to be added!
