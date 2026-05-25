# 🎉 Complete User Guide - Oil & Gas M&A Valuation Platform

## ✅ What's Now Available

### NEW Features Added:
1. ✅ **File Upload UI** - Upload production and financial data through the interface
2. ✅ **Analytics Dashboard** - View charts and visualizations
3. ✅ **Data Quality Tracking** - Monitor uploaded files and data completeness
4. ✅ **Interactive Charts** - Production trends, revenue/costs, file distribution

### Existing Features:
- ✅ User authentication
- ✅ Project management
- ✅ Financial modeling (assumptions, synergies, scenarios)
- ✅ Valuation calculations (NPV, IRR, ROIC, etc.)
- ✅ Results visualization with charts

## 🚀 Complete Workflow Guide

### Step 1: Register & Login

1. Go to **http://localhost:5173**
2. Click **"Register"**
3. Enter your details:
   - Email: your@email.com
   - Password: (min 8 characters)
   - Full Name: Your Name
4. Click **"Register"**
5. Login with your credentials

### Step 2: Create a Project

1. Click **"Create New Project"**
2. Fill in:
   - **Name**: "Permian Basin Acquisition"
   - **Description**: "Acquisition of producing assets"
   - **Project Type**: Select **"Acquisition"** (REQUIRED!)
   - **Target Company**: "Target Energy LLC"
   - **Deal Size**: 75000000
3. Click **"Create Project"**

### Step 3: Upload Data Files

#### Option A: Use the UI (Recommended)

1. Click on your project to open it
2. Click the **"Upload Data"** button
3. Select file type:
   - **Production Data** - Oil, gas, water volumes
   - **Financial Data** - Revenue, OPEX, CAPEX
4. Click **"Upload a file"** or drag and drop
5. Select your CSV or XLSX file
6. Click **"Upload File"**

#### Option B: Use Sample Files

Sample files are provided in the project directory:
- `sample_production_data.csv`
- `sample_financial_data.csv`

**Production Data Format:**
```csv
date,well_name,oil_volume,gas_volume,water_volume
2024-01-01,WELL-001,1000,5000,500
2024-02-01,WELL-001,950,4800,520
```

**Financial Data Format:**
```csv
date,revenue,opex,capex,taxes
2024-01-01,562000,85000,500000,0
2024-02-01,540000,87000,0,0
```

### Step 4: View Analytics

1. From project detail page, click **"Analytics"** button
2. You'll see:
   - **Summary Cards** - Total files, production files, financial files, scenarios
   - **Production Trends Chart** - Line chart showing production over time
   - **Revenue & Costs Chart** - Bar chart with quarterly breakdown
   - **File Distribution Chart** - Pie chart of uploaded files
   - **Data Quality Overview** - Completeness indicators

### Step 5: Create Assumptions

1. Click **"Financial Modeling"** button
2. Go to **"Assumptions"** tab
3. Click **"Create Assumptions"**
4. Fill in all fields:

**Basic Info:**
- Name: "Base Case"
- Version: 1

**Production:**
- Decline Curve Type: "exponential"
- Decline Rate: 0.15

**Oil Prices:**
- Year 1: $75.00
- Year 2: $78.00
- Year 3: $80.00

**Gas Prices:**
- Year 1: $3.50
- Year 2: $3.75
- Year 3: $4.00

**Costs:**
- OPEX Inflation: 0.03
- Transportation Cost: 2.50
- G&A Annual: 500000
- CAPEX Year 1: 5000000

**Deal:**
- Purchase Price: 50000000
- Debt: 30000000
- Equity: 20000000
- Discount Rate: 0.10
- Tax Rate: 0.21
- Exit Multiple: 5.5
- Forecast Years: 10

5. Click **"Create"**

### Step 6: Add Synergies (Optional)

1. Go to **"Synergies"** tab
2. Click **"Add Synergy Model"**
3. Fill in:
   - **Category**: "operational_overhead"
   - **Description**: "Cost savings from consolidation"
   - **Target Value**: 2000000
   - **Realization Schedule**:
     - Year 1: 25% (0.25)
     - Year 2: 50% (0.50)
     - Year 3: 75% (0.75)
     - Year 4: 100% (1.00)
4. Click **"Create"**

### Step 7: Create & Run Scenario

1. Go to **"Scenarios"** tab
2. Click **"Base Case"** button
3. A scenario will be created
4. Click **"Run Valuation"** on the scenario card
5. Wait 2-3 seconds
6. You'll be redirected to **"Results"** tab

### Step 8: View Results

You'll see:

**Metrics Cards:**
- NPV (Net Present Value)
- IRR (Internal Rate of Return)
- Payback Period (years)
- ROIC (Return on Invested Capital)
- ROI (Return on Investment)
- Profitability Index

**Interactive Charts:**
- **Production Decline Chart** - Oil & gas production forecast
- **Cash Flow Analysis Chart** - Revenue, OPEX, CAPEX, FCF
- **EBITDA & Synergies Chart** - Profitability and synergy realization

**Data Table:**
- Annual forecast for 10 years
- Production, revenue, costs, EBITDA, cash flows

**Investment Indicators:**
- NPV Positive? ✓/✗
- IRR > 12%? ✓/✗
- Profitability Index > 1.0? ✓/✗

## 📊 Understanding the Platform

### File Upload

**Supported Formats:**
- CSV (.csv)
- Excel (.xlsx, .xls)
- Max size: 10MB

**Production Data Columns:**
- `date` (required): YYYY-MM-DD format
- `well_name` (optional): Well identifier
- `oil_volume` (required): Barrels
- `gas_volume` (required): MCF
- `water_volume` (optional): Barrels

**Financial Data Columns:**
- `date` (required): YYYY-MM-DD format
- `revenue` (required): USD
- `opex` (required): USD
- `capex` (optional): USD
- `taxes` (optional): USD

### Analytics Dashboard

**Charts Available:**
1. **Production Trends** - Shows how production changes over time
2. **Revenue & Costs** - Quarterly breakdown of financials
3. **File Distribution** - Pie chart of uploaded files by type
4. **Data Quality** - Progress bars showing data completeness

**Data Quality Indicators:**
- Production Data Completeness: 0-100%
- Financial Data Completeness: 0-100%
- Modeling Readiness: 0-100%

### Valuation Calculations

The platform performs:
1. **Production Forecasting** - Using decline curves (exponential, hyperbolic, harmonic)
2. **Revenue Modeling** - Production × Commodity prices
3. **Cost Forecasting** - OPEX with inflation, CAPEX schedule
4. **Synergy Calculations** - Realization over time
5. **Cash Flow Modeling** - Revenue - Costs + Synergies
6. **NPV Calculation** - Discounted cash flows
7. **IRR Calculation** - Internal rate of return
8. **Terminal Value** - Exit value using EBITDA multiple

## 🎯 Best Practices

### Data Upload

1. **Upload historical data first** - This provides baseline for forecasts
2. **Use consistent date formats** - YYYY-MM-DD
3. **Include all required columns** - Check format guide
4. **Upload both production and financial data** - For complete analysis

### Financial Modeling

1. **Start with Base Case** - Use realistic assumptions
2. **Create Bull and Bear cases** - For sensitivity analysis
3. **Add synergies carefully** - Be conservative with estimates
4. **Use appropriate decline curves** - Exponential for most cases
5. **Set realistic commodity prices** - Based on market forecasts

### Interpreting Results

**Positive Investment Indicators:**
- NPV > 0 (value creating)
- IRR > Hurdle Rate (typically 12-15%)
- Payback < 5 years
- Profitability Index > 1.0

**Red Flags:**
- Negative NPV
- IRR < Discount Rate
- Very long payback period
- Declining EBITDA

## 🔧 Advanced Features

### Multiple Scenarios

1. Create different assumption sets
2. Create Bull/Base/Bear scenarios
3. Run valuation for each
4. Compare results side-by-side

### Synergy Modeling

**Categories:**
- `operational_overhead` - Cost savings from consolidation
- `procurement_efficiency` - Better purchasing power
- `workforce_consolidation` - Reduced headcount
- `shared_infrastructure` - Shared facilities

**Realization Schedule:**
- Define how synergies ramp up over time
- Typically 25% → 50% → 75% → 100% over 4 years

### Data Management

- Upload multiple files per project
- Track file status (pending, completed, failed)
- View file upload history
- Monitor data quality

## 📈 Example Workflow

### Complete M&A Analysis

1. **Upload Data**
   - Production history (12 months)
   - Financial statements (12 months)

2. **View Analytics**
   - Check production trends
   - Review revenue/cost patterns
   - Verify data quality

3. **Create Assumptions**
   - Base Case (most likely)
   - Bull Case (optimistic)
   - Bear Case (conservative)

4. **Add Synergies**
   - Identify cost savings
   - Define realization schedule

5. **Run Valuations**
   - Run all three scenarios
   - Compare results

6. **Make Decision**
   - Review NPV, IRR, payback
   - Check investment indicators
   - Analyze sensitivity

## 🆘 Troubleshooting

### File Upload Issues

**Problem**: Upload fails
**Solution**: 
- Check file format (CSV or XLSX)
- Verify column names match expected format
- Ensure file size < 10MB
- Check date format (YYYY-MM-DD)

**Problem**: File uploaded but no data in analytics
**Solution**:
- Refresh the analytics page
- Check file status in project detail
- Verify file has correct columns

### Valuation Issues

**Problem**: Valuation fails
**Solution**:
- Ensure all assumption fields are filled
- Check that oil/gas price forecasts have at least one year
- Verify CAPEX schedule has at least one entry

**Problem**: Negative NPV
**Solution**:
- This may be correct! Check your assumptions
- Increase production or commodity prices
- Reduce costs or purchase price
- Add synergies

### UI Issues

**Problem**: Can't see upload button
**Solution**:
- Make sure you're on the project detail page
- Refresh the page
- Check that you're logged in

**Problem**: Charts not showing
**Solution**:
- Upload data files first
- Refresh the analytics page
- Check browser console for errors

## 🎊 Summary

You now have a complete M&A valuation platform with:

✅ **Data Upload** - UI for uploading production and financial data
✅ **Analytics Dashboard** - Charts and visualizations
✅ **Financial Modeling** - Assumptions, synergies, scenarios
✅ **Valuation Engine** - NPV, IRR, ROIC calculations
✅ **Results Visualization** - Interactive charts and tables
✅ **Data Quality Tracking** - Monitor completeness

### Quick Links

- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/api/v1/docs
- **Sample Files**: 
  - `sample_production_data.csv`
  - `sample_financial_data.csv`

### Next Steps

1. Register a new account
2. Create a project
3. Upload sample data files
4. View analytics dashboard
5. Create assumptions
6. Run valuation
7. View results with charts!

**Enjoy your fully functional M&A valuation platform!** 🚀📈💰
