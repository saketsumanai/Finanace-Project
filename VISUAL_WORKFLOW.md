# 🎨 Visual Workflow Guide

## 🚀 Complete User Journey

```
┌─────────────────────────────────────────────────────────────────────┐
│                         START HERE                                  │
│                   http://localhost:5173                             │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 1: REGISTER / LOGIN                                           │
├─────────────────────────────────────────────────────────────────────┤
│  → Click "Register" button                                          │
│  → Enter: Email, Password, Full Name                                │
│  → Click "Create Account"                                           │
│  → Automatically logged in with JWT token                           │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 2: CREATE PROJECT                                             │
├─────────────────────────────────────────────────────────────────────┤
│  → Click "New Project" button                                       │
│  → Fill in form:                                                    │
│     • Name: "Eagle Ford Acquisition"                                │
│     • Description: "Mature oil & gas assets"                        │
│     • Type: "Acquisition"                                           │
│     • Deal Size: 50000000 ($50M)                                    │
│     • Status: "Active"                                              │
│  → Click "Create Project"                                           │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 3: GENERATE AI DATA ✨                                        │
├─────────────────────────────────────────────────────────────────────┤
│  → Click on project card to open                                    │
│  → Click "Modeling" tab                                             │
│  → Click purple "✨ Generate Smart Data with AI" button            │
│  → Wait 2-3 seconds                                                 │
│  → Success! "AI generated 12 production + 12 financial records"     │
│                                                                      │
│  What happened behind the scenes:                                   │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ AI Data Generator                                            │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │ 1. Analyzed deal size ($50M)                                 │  │
│  │ 2. Scaled initial rates (1000 bbl/day, 5000 MCF/day)        │  │
│  │ 3. Applied 15% decline curve (acquisition type)             │  │
│  │ 4. Generated 12 months production data                       │  │
│  │ 5. Applied market pricing ($70-85 oil, $3-4.5 gas)          │  │
│  │ 6. Calculated costs ($2.50/bbl OPEX)                        │  │
│  │ 7. Generated 12 months financial data                        │  │
│  │ 8. Stored in PostgreSQL database                            │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 4: CREATE ASSUMPTIONS                                         │
├─────────────────────────────────────────────────────────────────────┤
│  → Stay on "Assumptions" tab                                        │
│  → Click "Create Assumptions"                                       │
│  → Fill in form:                                                    │
│                                                                      │
│  Basic Info:                                                        │
│  • Name: "Base Case Assumptions"                                    │
│  • Version: "1.0"                                                   │
│  • Forecast Years: 20                                               │
│                                                                      │
│  Production:                                                        │
│  • Decline Curve: "Exponential"                                     │
│  • Decline Rate: 0.15 (15% annual)                                  │
│                                                                      │
│  Pricing (5-year forecast):                                         │
│  • Oil: [75, 78, 80, 82, 85]                                        │
│  • Gas: [3.5, 3.7, 3.9, 4.0, 4.2]                                   │
│                                                                      │
│  Financial:                                                         │
│  • Discount Rate: 0.12 (12%)                                        │
│  • Tax Rate: 0.21 (21%)                                             │
│  • Purchase Price: 50000000                                         │
│  • Exit Multiple: 5.0                                               │
│  • OPEX Inflation: 0.03 (3%)                                        │
│  • CAPEX: [5000000, 1000000, 500000]                                │
│                                                                      │
│  → Click "Create Assumptions"                                       │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 4.5: ADD SYNERGIES (Optional)                                 │
├─────────────────────────────────────────────────────────────────────┤
│  → Click "Synergies" tab                                            │
│  → Click "Add Synergy Model"                                        │
│  → Choose category: "Cost Synergies"                                │
│  → Target Value: 2000000 ($2M/year)                                 │
│  → Realization: [0.3, 0.6, 1.0] (30%, 60%, 100% over 3 years)      │
│  → Description: "Operational efficiencies"                          │
│  → Click "Create"                                                   │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 5: CREATE SCENARIO & RUN VALUATION                            │
├─────────────────────────────────────────────────────────────────────┤
│  → Click "Scenarios" tab                                            │
│  → Click "Base Case" button                                         │
│  → Scenario created automatically                                   │
│  → Click "Run Valuation" button                                     │
│  → Wait 3-5 seconds for calculations                                │
│                                                                      │
│  What's happening:                                                  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Valuation Engine                                             │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │ 1. Load historical data (AI-generated)                       │  │
│  │ 2. Calculate initial rates                                   │  │
│  │ 3. Generate 20-year production forecast                      │  │
│  │ 4. Apply decline curves                                      │  │
│  │ 5. Calculate revenue (production × prices)                   │  │
│  │ 6. Forecast OPEX with inflation                             │  │
│  │ 7. Apply CAPEX schedule                                      │  │
│  │ 8. Calculate synergies                                       │  │
│  │ 9. Build cash flow model                                     │  │
│  │ 10. Calculate NPV, IRR, Payback, ROIC                       │  │
│  │ 11. Calculate terminal value                                │  │
│  │ 12. Store results in database                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  → Success! "Valuation completed successfully"                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 6: VIEW RESULTS                                               │
├─────────────────────────────────────────────────────────────────────┤
│  → Click "View Results" or go to "Results" tab                      │
│  → See comprehensive valuation output                               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  RESULTS DASHBOARD                                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  KEY METRICS                                               │    │
│  ├────────────────────────────────────────────────────────────┤    │
│  │  NPV (12%)           $8,234,567                            │    │
│  │  IRR                 14.3%                                 │    │
│  │  Payback Period      4.2 years                             │    │
│  │  ROIC                16.8%                                 │    │
│  │  Terminal Value      $45,000,000                           │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  CHART 1: PRODUCTION DECLINE                               │    │
│  │                                                            │    │
│  │   1200 ┤                                                   │    │
│  │        │ ●                                                 │    │
│  │   1000 ┤   ●                                               │    │
│  │        │     ●                                             │    │
│  │    800 ┤       ●                                           │    │
│  │        │         ●                                         │    │
│  │    600 ┤           ●                                       │    │
│  │        │             ●                                     │    │
│  │    400 ┤               ●                                   │    │
│  │        │                 ●                                 │    │
│  │    200 ┤                   ●                               │    │
│  │        └─────────────────────────────────────────          │    │
│  │         Y1  Y3  Y5  Y7  Y9  Y11 Y13 Y15 Y17 Y19           │    │
│  │                                                            │    │
│  │  Legend: ● Oil (bbl/day)  ■ Gas (MCF/day)                 │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  CHART 2: CASH FLOW ANALYSIS                               │    │
│  │                                                            │    │
│  │   $20M ┤                                                   │    │
│  │        │  ███                                              │    │
│  │   $15M ┤  ███  ███                                         │    │
│  │        │  ███  ███  ███                                    │    │
│  │   $10M ┤  ███  ███  ███  ███                               │    │
│  │        │  ███  ███  ███  ███  ███                          │    │
│  │    $5M ┤  ███  ███  ███  ███  ███  ███                     │    │
│  │        │  ███  ███  ███  ███  ███  ███  ███                │    │
│  │     $0 ┼──────────────────────────────────────             │    │
│  │        └─────────────────────────────────────              │    │
│  │         Y1   Y3   Y5   Y7   Y9   Y11  Y13                 │    │
│  │                                                            │    │
│  │  Legend: ■ Revenue  ■ OPEX  ■ CAPEX  ■ FCF                │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  CHART 3: EBITDA & SYNERGIES                               │    │
│  │                                                            │    │
│  │   $12M ┤                                                   │    │
│  │        │  ●───●───●───●───●───●───●───●───●               │    │
│  │   $10M ┤                                                   │    │
│  │        │                                                   │    │
│  │    $8M ┤                                                   │    │
│  │        │  ▲───▲───▲───▲───▲───▲───▲───▲───▲               │    │
│  │    $6M ┤                                                   │    │
│  │        │                                                   │    │
│  │    $4M ┤                                                   │    │
│  │        └─────────────────────────────────────              │    │
│  │         Y1   Y3   Y5   Y7   Y9   Y11  Y13                 │    │
│  │                                                            │    │
│  │  Legend: ● EBITDA  ▲ Synergies                            │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  FINANCIAL SUMMARY (20 years)                              │    │
│  ├────────────────────────────────────────────────────────────┤    │
│  │  Total Revenue              $180,456,789                   │    │
│  │  Total OPEX                 $45,234,567                    │    │
│  │  Total CAPEX                $12,500,000                    │    │
│  │  Total Synergies            $24,000,000                    │    │
│  │  Total EBITDA               $122,789,456                   │    │
│  │  Total Free Cash Flow       $98,345,678                    │    │
│  │                                                            │    │
│  │  Average Annual EBITDA      $6,139,473                     │    │
│  │  Year 1 EBITDA              $8,234,567                     │    │
│  │  Final Year EBITDA          $4,567,890                     │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  PRODUCTION SUMMARY                                        │    │
│  ├────────────────────────────────────────────────────────────┤    │
│  │  Initial Oil Rate           1,000 bbl/day                  │    │
│  │  Initial Gas Rate           5,000 MCF/day                  │    │
│  │  Total Oil Production       5.2 MMbbl                      │    │
│  │  Total Gas Production       26.1 BCF                       │    │
│  │  Decline Curve Type         Exponential                    │    │
│  │  Decline Rate               15% annual                     │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  INVESTMENT DECISION                                       │    │
│  ├────────────────────────────────────────────────────────────┤    │
│  │  ✅ POSITIVE NPV - Value creating investment               │    │
│  │  ✅ IRR > Hurdle Rate (14.3% > 12%)                        │    │
│  │  ✅ Payback < 5 years                                      │    │
│  │  ✅ ROIC > 15% (strong returns)                            │    │
│  │                                                            │    │
│  │  RECOMMENDATION: PROCEED WITH ACQUISITION                  │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## 🎯 Alternative Workflows

### Workflow A: Multiple Scenarios
```
Create Assumptions
       │
       ├─→ Create Bull Scenario → Run Valuation → View Results
       │
       ├─→ Create Base Scenario → Run Valuation → View Results
       │
       └─→ Create Bear Scenario → Run Valuation → View Results
                                                         │
                                                         ▼
                                              Compare All Scenarios
```

### Workflow B: With Synergies
```
Create Assumptions
       │
       ├─→ Add Cost Synergies ($2M/year)
       │
       ├─→ Add Revenue Synergies ($1M/year)
       │
       └─→ Add Tax Synergies ($500K/year)
                    │
                    ▼
           Create Scenario → Run Valuation
                                   │
                                   ▼
                    See Synergy Impact in Results
```

### Workflow C: Sensitivity Analysis
```
Base Assumptions (15% decline, $75 oil)
       │
       ├─→ Scenario 1: 10% decline → NPV = $15M
       │
       ├─→ Scenario 2: 15% decline → NPV = $8M
       │
       ├─→ Scenario 3: 20% decline → NPV = $2M
       │
       └─→ Compare to find break-even decline rate
```

## 🔄 Data Flow Architecture

```
┌─────────────┐
│   Browser   │
│  (React UI) │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────────────────────────────────────┐
│         Backend API (FastAPI)               │
├─────────────────────────────────────────────┤
│  /auth/register    → Create user            │
│  /auth/login       → Get JWT token          │
│  /projects         → CRUD projects          │
│  /upload/generate  → AI data generation     │
│  /modeling/...     → Assumptions, scenarios │
│  /modeling/valuate → Run valuation          │
└──────┬──────────────────────┬───────────────┘
       │                      │
       ▼                      ▼
┌─────────────┐      ┌──────────────────┐
│ PostgreSQL  │      │  Calculation     │
│  Database   │      │    Engines       │
├─────────────┤      ├──────────────────┤
│ • Users     │      │ • Decline Curves │
│ • Projects  │      │ • Forecasting    │
│ • Prod Data │      │ • Synergies      │
│ • Fin Data  │      │ • IRR/NPV        │
│ • Scenarios │      │ • Valuation      │
│ • Results   │      └──────────────────┘
└─────────────┘
```

## 🎨 UI Component Tree

```
App
├── AuthPage
│   ├── LoginForm
│   └── RegisterForm
│
├── DashboardLayout
│   ├── Sidebar
│   ├── Header
│   └── Content
│       ├── DashboardPage
│       │   └── ProjectCards
│       │
│       ├── ProjectsPage
│       │   ├── ProjectList
│       │   └── CreateProjectModal
│       │
│       ├── ProjectDetailPage
│       │   ├── ProjectInfo
│       │   ├── FileUploadModal
│       │   └── ActionButtons
│       │
│       ├── ModelingPage
│       │   ├── AssumptionsTab
│       │   │   └── AssumptionsForm
│       │   │
│       │   ├── SynergiesTab
│       │   │   └── SynergyModelForm
│       │   │
│       │   ├── ScenariosTab
│       │   │   └── ScenarioCards
│       │   │
│       │   └── ResultsTab
│       │       └── ValuationResults
│       │           ├── MetricsCards
│       │           ├── ProductionChart
│       │           ├── CashFlowChart
│       │           └── EBITDAChart
│       │
│       └── AnalyticsPage
│           ├── ProductionTrendsChart
│           ├── RevenueCostsChart
│           ├── FileDistributionChart
│           └── DataQualityChart
│
└── Shared Components
    ├── Button
    ├── Card
    ├── Input
    ├── Select
    └── Modal
```

## 🔧 Backend Service Architecture

```
FastAPI App
├── API Routes
│   ├── /auth
│   │   ├── POST /register
│   │   ├── POST /login
│   │   └── GET /me
│   │
│   ├── /projects
│   │   ├── GET /
│   │   ├── POST /
│   │   ├── GET /{id}
│   │   ├── PUT /{id}
│   │   └── DELETE /{id}
│   │
│   ├── /upload
│   │   ├── POST /generate-smart-data  ← NEW!
│   │   ├── POST /production
│   │   ├── POST /financials
│   │   └── GET /project/{id}
│   │
│   └── /modeling
│       ├── POST /assumptions
│       ├── GET /assumptions/{project_id}
│       ├── POST /synergies
│       ├── POST /scenarios
│       ├── POST /valuate/{scenario_id}
│       └── GET /results/{scenario_id}
│
├── Services
│   ├── DataGenerator  ← NEW!
│   │   ├── generate_production_data()
│   │   ├── generate_financial_data()
│   │   └── generate_smart_data()
│   │
│   ├── FileService
│   │   ├── validate_file()
│   │   ├── save_file()
│   │   └── get_file_size()
│   │
│   └── ETLService
│       ├── process_production_file()
│       └── process_financial_file()
│
├── Engines
│   ├── DeclineCurves
│   │   ├── exponential_decline()
│   │   ├── hyperbolic_decline()
│   │   └── harmonic_decline()
│   │
│   ├── ForecastingEngine
│   │   ├── forecast_production()
│   │   ├── forecast_revenue()
│   │   ├── forecast_opex()
│   │   ├── forecast_capex()
│   │   └── create_cash_flow_forecast()
│   │
│   ├── SynergyEngine
│   │   ├── calculate_synergies()
│   │   └── apply_realization_schedule()
│   │
│   ├── IRREngine
│   │   ├── calculate_irr()
│   │   ├── calculate_npv()
│   │   ├── calculate_payback_period()
│   │   └── calculate_roi()
│   │
│   └── ValuationService
│       ├── run_valuation()
│       ├── get_valuation_results()
│       └── compare_scenarios()
│
└── Models (Database)
    ├── User
    ├── Project
    ├── ProductionData
    ├── FinancialData
    ├── Assumptions
    ├── SynergyModel
    ├── Scenario
    └── ValuationOutput
```

## 🎓 Key Concepts Explained

### What is Decline Curve Analysis?
```
Production over time follows a decline curve:

Exponential:  Q(t) = Q₀ × e^(-D×t)
Hyperbolic:   Q(t) = Q₀ / (1 + b×D×t)^(1/b)
Harmonic:     Q(t) = Q₀ / (1 + D×t)

Where:
Q(t) = Production at time t
Q₀   = Initial production rate
D    = Decline rate
b    = Hyperbolic exponent
```

### What is NPV?
```
NPV = Σ [CFₜ / (1 + r)ᵗ] - Initial Investment

Where:
CFₜ = Cash flow in year t
r   = Discount rate
t   = Year number

Example:
Year 0: -$50M (purchase)
Year 1: +$8M
Year 2: +$7M
Year 3: +$6M
...
Year 20: +$2M + $45M (terminal value)

NPV @ 12% = $8.2M
```

### What is IRR?
```
IRR is the discount rate where NPV = 0

If IRR > Hurdle Rate → Good investment
If IRR < Hurdle Rate → Bad investment

Example:
IRR = 14.3%
Hurdle Rate = 12%
Decision: PROCEED (14.3% > 12%)
```

---

**Ready to start?** Open http://localhost:5173 and follow the workflow above!
