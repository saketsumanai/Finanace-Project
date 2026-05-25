# Oil & Gas M&A Valuation Platform
## Architecture and Execution Plan

**Version:** 1.0  
**Date:** May 23, 2026  
**Status:** Design Phase

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Business Requirements](#business-requirements)
3. [Financial Modeling Methodology](#financial-modeling-methodology)
4. [Technical Architecture](#technical-architecture)
5. [Database Schema](#database-schema)
6. [API Contracts](#api-contracts)
7. [Frontend Architecture](#frontend-architecture)
8. [Visualization Design](#visualization-design)
9. [Calculation Engine Structure](#calculation-engine-structure)
10. [Security Architecture](#security-architecture)
11. [Performance & Scalability](#performance--scalability)
12. [Testing Strategy](#testing-strategy)
13. [Deployment Strategy](#deployment-strategy)
14. [Implementation Roadmap](#implementation-roadmap)
15. [Risk Considerations](#risk-considerations)
16. [Future Extensibility](#future-extensibility)

---

## Executive Summary

### Platform Vision

The Oil & Gas M&A Valuation Platform is an institutional-grade financial analysis tool designed to replicate the sophisticated valuation methodologies used by top-tier investment banks (Goldman Sachs, Evercore, JPMorgan Energy) and consulting firms (McKinsey Energy Practice). The platform enables energy sector professionals to evaluate upstream oil and gas acquisitions through comprehensive data analysis, financial modeling, and scenario planning.

### Key Capabilities

- **Data Ingestion**: Process historical production, revenue, and cost data from CSV/XLSX files
- **Financial Modeling**: Configure production decline curves, cost assumptions, synergies, and deal structure
- **Valuation Metrics**: Calculate DCF, IRR, NPV, ROIC, payback period, and accretion/dilution
- **Scenario Analysis**: Model Bull/Base/Bear cases with sensitivity tables
- **Visualization**: Executive-grade charts including waterfall, IRR projection, cash flow, and production decline
- **Audit & Compliance**: Complete audit trail with role-based access control

### Target Users

- Investment Banking Analysts & Associates
- Private Equity Investment Professionals
- Corporate Development Teams
- Energy Sector M&A Advisors
- Financial Modeling Specialists

---

## Business Requirements

### Functional Requirements Summary

#### FR-1: Asset Intake & Data Processing
- Upload CSV/XLSX files up to 50MB
- Validate data schemas and quality
- Normalize units (barrels, MCF, USD)
- Convert currencies to USD
- Aggregate by month/quarter/year
- Generate data quality scores

#### FR-2: Financial Modeling Configuration
- Configure production assumptions (decline curves, commodity prices, reserves)
- Configure cost assumptions (OPEX inflation, CAPEX schedules, G&A)
- Configure synergy assumptions (overhead cuts, procurement, workforce, infrastructure)
- Configure deal structure (purchase price, debt, discount rate, exit multiple)

#### FR-3: Valuation Calculations
- Compute EBITDA, EBITDAX, Free Cash Flow
- Calculate NPV using DCF methodology
- Calculate IRR with 0.01% accuracy
- Calculate payback period, ROIC, debt paydown
- Model synergy realization schedules
- Generate 20-year forecasts

#### FR-4: Scenario & Sensitivity Analysis
- Support Bull/Base/Bear scenario configurations
- Execute parallel scenario calculations
- Generate sensitivity tables (2-variable analysis)
- Compare scenarios side-by-side

#### FR-5: Visualization & Reporting
- Waterfall chart (value creation breakdown)
- IRR projection chart (multi-year, multi-scenario)
- Cash flow forecast chart (stacked components)
- Production decline curve chart
- EBITDA trend chart
- Synergy realization timeline
- Debt paydown schedule
- Export to XLSX format

#### FR-6: Project Management
- Create/update/delete projects
- Version control for assumptions
- Multi-user collaboration
- Audit logging

### Non-Functional Requirements

#### NFR-1: Performance
- API response time < 500ms for data retrieval
- Valuation calculations complete within 30 seconds
- Chart rendering < 2 seconds
- Support 50+ concurrent users

#### NFR-2: Security
- JWT-based authentication
- Role-based access control (RBAC)
- File upload sanitization
- Input validation & SQL injection prevention
- Rate limiting (1000 req/hour authenticated, 100 req/hour unauthenticated)
- 7-year audit log retention

#### NFR-3: Usability
- Bloomberg Terminal aesthetic with modern UX
- Dark/light mode support
- Responsive design (desktop, tablet, mobile)
- Accessibility compliance (WCAG 2.1 AA)
- Animated transitions

#### NFR-4: Reliability
- 99.5% uptime SLA
- Automated backups (daily)
- Disaster recovery plan
- Error handling with user-friendly messages

---

## Financial Modeling Methodology

### Production Forecasting

#### Decline Curve Models

The platform supports three industry-standard decline curve models:

**1. Exponential Decline**
```
Q(t) = Q_i * e^(-D * t)
```
- Q(t) = Production rate at time t
- Q_i = Initial production rate
- D = Decline rate (constant)
- t = Time period

**2. Hyperbolic Decline**
```
Q(t) = Q_i / (1 + b * D_i * t)^(1/b)
```
- b = Hyperbolic exponent (0 < b < 1)
- D_i = Initial decline rate

**3. Harmonic Decline**
```
Q(t) = Q_i / (1 + D_i * t)
```
- Special case of hyperbolic where b = 1

#### Application Strategy
- Oil wells: Typically exponential or hyperbolic (b = 0.3-0.5)
- Gas wells: Often hyperbolic (b = 0.5-0.8)
- Mature fields: Exponential decline
- Unconventional (shale): Hyperbolic with high initial decline

### Revenue Modeling

```
Revenue(t) = Oil_Production(t) * Oil_Price(t) + Gas_Production(t) * Gas_Price(t)
```

**Commodity Price Assumptions:**
- Spot prices
- Forward curve pricing
- Hedged positions
- Price deck scenarios (Bull/Base/Bear)

### Cost Modeling

#### Operating Expenses (OPEX)
```
OPEX(t) = Base_OPEX * (1 + Inflation_Rate)^t - Synergies(t)
```

**Components:**
- Lease operating expenses (LOE)
- Transportation costs
- Processing fees
- G&A allocation

#### Capital Expenditures (CAPEX)
```
CAPEX(t) = Maintenance_CAPEX(t) + Growth_CAPEX(t)
```

**Maintenance CAPEX:** Sustain current production levels  
**Growth CAPEX:** Develop new wells/infrastructure

### Synergy Modeling

#### Synergy Categories

**1. Operational Overhead Reduction**
- Eliminate duplicate G&A functions
- Consolidate field offices
- Typical range: 10-20% of combined G&A

**2. Procurement Efficiencies**
- Volume discounts on services
- Renegotiate supplier contracts
- Typical range: 5-10% of procurement spend

**3. Workforce Consolidation**
- Eliminate redundant positions
- Optimize field crew schedules
- Typical range: 15-25% of labor costs

**4. Shared Infrastructure**
- Utilize excess pipeline capacity
- Share processing facilities
- Reduce transportation costs
- Typical range: 10-15% of midstream costs

#### Synergy Realization Schedule

```
Realized_Synergy(t) = Target_Synergy * Realization_Curve(t)
```

**Standard Realization Curve:**
- Year 1: 25% of target
- Year 2: 60% of target
- Year 3: 85% of target
- Year 4+: 100% of target

### Cash Flow Calculation

#### EBITDA Calculation
```
EBITDA(t) = Revenue(t) - OPEX(t) - Transportation(t) + Synergies(t)
```

#### EBITDAX Calculation
```
EBITDAX(t) = EBITDA(t) + Exploration_Expense(t)
```

#### Free Cash Flow Calculation
```
FCF(t) = EBITDA(t) - CAPEX(t) - Taxes(t) + Depreciation(t) - Change_in_NWC(t)
```

**Tax Calculation:**
```
Taxes(t) = (EBITDA(t) - Depreciation(t) - Interest(t)) * Tax_Rate
```

### Valuation Methodologies

#### Discounted Cash Flow (DCF)

```
NPV = Σ[FCF(t) / (1 + WACC)^t] + Terminal_Value / (1 + WACC)^n
```

**Terminal Value Calculation (Exit Multiple Method):**
```
Terminal_Value = EBITDA(n) * Exit_Multiple
```

**Typical Exit Multiples:**
- Upstream oil & gas: 4.0x - 6.0x EBITDA
- Varies by commodity mix, reserve life, decline rates

#### Internal Rate of Return (IRR)

IRR is the discount rate where NPV = 0:

```
0 = -Initial_Investment + Σ[FCF(t) / (1 + IRR)^t] + Terminal_Value / (1 + IRR)^n
```

**Solution Method:** Newton-Raphson iterative algorithm
- Convergence tolerance: 0.01%
- Maximum iterations: 100

#### Return on Invested Capital (ROIC)

```
ROIC = NOPAT / Invested_Capital
```

Where:
- NOPAT = Net Operating Profit After Tax
- Invested_Capital = Total Debt + Total Equity

#### Payback Period

Time required to recover initial investment:

```
Payback_Period = min(t) where Σ[FCF(i) for i=0 to t] ≥ Initial_Investment
```

### Scenario Analysis

#### Bull Case Assumptions
- Commodity prices: +20% vs base
- Production decline: -10% vs base (slower decline)
- OPEX inflation: -1% vs base
- Synergy realization: +15% vs base
- Exit multiple: +0.5x vs base

#### Base Case Assumptions
- Commodity prices: Current forward curve
- Production decline: Historical average
- OPEX inflation: CPI forecast
- Synergy realization: Management plan
- Exit multiple: Industry median

#### Bear Case Assumptions
- Commodity prices: -20% vs base
- Production decline: +15% vs base (faster decline)
- OPEX inflation: +2% vs base
- Synergy realization: -25% vs base
- Exit multiple: -0.5x vs base

### Sensitivity Analysis

Two-variable sensitivity tables analyze NPV/IRR sensitivity to:

**Common Variable Pairs:**
- Oil price vs. Gas price
- Oil price vs. Discount rate
- CAPEX vs. OPEX
- Synergy realization vs. Commodity price
- Exit multiple vs. Discount rate

**Calculation:**
For each combination (Variable1_i, Variable2_j):
- Update assumptions
- Recalculate cash flows
- Compute NPV and IRR
- Store in sensitivity matrix

---


## Technical Architecture

### System Overview

The platform follows a modern three-tier architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  React SPA (Vite)                                     │  │
│  │  - TailwindCSS styling                                │  │
│  │  - Chart.js / Recharts visualizations                 │  │
│  │  - Zustand state management                           │  │
│  │  - React Query data fetching                          │  │
│  │  - Framer Motion animations                           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTPS/REST
┌─────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI Backend                                      │  │
│  │  ┌────────────────┐  ┌────────────────┐             │  │
│  │  │  API Routes    │  │  Auth Service  │             │  │
│  │  └────────────────┘  └────────────────┘             │  │
│  │  ┌────────────────┐  ┌────────────────┐             │  │
│  │  │  ETL Pipeline  │  │  File Service  │             │  │
│  │  └────────────────┘  └────────────────┘             │  │
│  │  ┌──────────────────────────────────────┐           │  │
│  │  │  Financial Calculation Engine        │           │  │
│  │  │  - Valuation Service                 │           │  │
│  │  │  - IRR Engine                        │           │  │
│  │  │  - Synergy Engine                    │           │  │
│  │  │  - Forecasting Engine                │           │  │
│  │  │  - Scenario Engine                   │           │  │
│  │  └──────────────────────────────────────┘           │  │
│  │  ┌────────────────┐  ┌────────────────┐             │  │
│  │  │  Celery Worker │  │  Redis Cache   │             │  │
│  │  └────────────────┘  └────────────────┘             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕ SQL/ORM
┌─────────────────────────────────────────────────────────────┐
│                       DATA LAYER                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  PostgreSQL Database                                  │  │
│  │  - User data                                          │  │
│  │  - Project data                                       │  │
│  │  - Production/Financial data                          │  │
│  │  - Assumptions & Scenarios                            │  │
│  │  - Valuation outputs                                  │  │
│  │  - Audit logs                                         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

#### Backend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Web Framework | FastAPI | 0.110+ | High-performance async API |
| ORM | SQLAlchemy | 2.0+ | Database abstraction |
| Database | PostgreSQL | 15+ | Primary data store |
| Data Processing | Pandas | 2.2+ | Financial calculations |
| Numerical Computing | NumPy | 1.26+ | Array operations |
| Scientific Computing | SciPy | 1.12+ | IRR optimization |
| Validation | Pydantic | 2.6+ | Request/response schemas |
| Migrations | Alembic | 1.13+ | Database versioning |
| File Processing | OpenPyXL | 3.1+ | Excel file handling |
| Task Queue | Celery | 5.3+ | Background jobs |
| Cache | Redis | 7.2+ | Session & data caching |
| Authentication | python-jose | 3.3+ | JWT tokens |
| Password Hashing | passlib | 1.7+ | Bcrypt hashing |

#### Frontend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | React | 18.2+ | UI library |
| Build Tool | Vite | 5.1+ | Fast dev server & bundler |
| Styling | TailwindCSS | 3.4+ | Utility-first CSS |
| Charts | Chart.js | 4.4+ | Primary charting library |
| Charts (Alt) | Recharts | 2.12+ | React-native charts |
| State Management | Zustand | 4.5+ | Lightweight state |
| Data Fetching | React Query | 5.28+ | Server state management |
| HTTP Client | Axios | 1.6+ | API requests |
| Animations | Framer Motion | 11.0+ | UI animations |
| Tables | TanStack Table | 8.13+ | Data grids |
| Forms | React Hook Form | 7.51+ | Form validation |
| Routing | React Router | 6.22+ | Client-side routing |

#### DevOps Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Containerization | Docker | 25+ | Application packaging |
| Orchestration | Docker Compose | 2.24+ | Multi-container apps |
| Reverse Proxy | Nginx | 1.25+ | Load balancing & SSL |
| CI/CD | GitHub Actions | N/A | Automated pipelines |
| Testing (Backend) | Pytest | 8.1+ | Python testing |
| Testing (Frontend) | Vitest | 1.3+ | Vite-native testing |
| Testing (E2E) | Playwright | 1.42+ | End-to-end testing |

### Architecture Patterns

#### Backend Architecture

**Clean Architecture / Hexagonal Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer (Routes)                    │
│  - Request validation                                    │
│  - Response serialization                                │
│  - Error handling                                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   Service Layer                          │
│  - Business logic                                        │
│  - Transaction management                                │
│  - Cross-cutting concerns                                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  Repository Layer                        │
│  - Data access abstraction                               │
│  - Query optimization                                    │
│  - ORM operations                                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    Database Layer                        │
│  - PostgreSQL                                            │
└─────────────────────────────────────────────────────────┘
```

**Folder Structure:**

```
backend/
├── app/
│   ├── main.py                 # FastAPI application entry
│   ├── config.py               # Configuration management
│   ├── dependencies.py         # Dependency injection
│   │
│   ├── api/                    # API Layer
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # Authentication endpoints
│   │   │   ├── projects.py     # Project management
│   │   │   ├── upload.py       # File upload endpoints
│   │   │   ├── modeling.py     # Modeling endpoints
│   │   │   ├── scenarios.py    # Scenario endpoints
│   │   │   └── charts.py       # Visualization endpoints
│   │   └── deps.py             # Route dependencies
│   │
│   ├── core/                   # Core utilities
│   │   ├── security.py         # JWT, password hashing
│   │   ├── config.py           # Settings
│   │   └── exceptions.py       # Custom exceptions
│   │
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── uploaded_file.py
│   │   ├── production_data.py
│   │   ├── financial_data.py
│   │   ├── assumptions.py
│   │   ├── scenario.py
│   │   ├── synergy_model.py
│   │   ├── valuation_output.py
│   │   └── audit_log.py
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── assumptions.py
│   │   ├── scenario.py
│   │   ├── valuation.py
│   │   └── chart.py
│   │
│   ├── repositories/           # Data access layer
│   │   ├── base.py
│   │   ├── user_repository.py
│   │   ├── project_repository.py
│   │   ├── data_repository.py
│   │   └── valuation_repository.py
│   │
│   ├── services/               # Business logic layer
│   │   ├── auth_service.py
│   │   ├── file_service.py
│   │   ├── etl_service.py
│   │   ├── project_service.py
│   │   └── export_service.py
│   │
│   ├── engines/                # Financial calculation engines
│   │   ├── __init__.py
│   │   ├── valuation_service.py    # Main valuation orchestrator
│   │   ├── irr_engine.py           # IRR calculation
│   │   ├── synergy_engine.py       # Synergy modeling
│   │   ├── forecasting_engine.py   # Production & cash flow forecasting
│   │   ├── scenario_engine.py      # Scenario analysis
│   │   ├── sensitivity_engine.py   # Sensitivity analysis
│   │   └── decline_curves.py       # Decline curve models
│   │
│   ├── tasks/                  # Celery tasks
│   │   ├── __init__.py
│   │   ├── etl_tasks.py
│   │   └── calculation_tasks.py
│   │
│   └── utils/                  # Utility functions
│       ├── validators.py
│       ├── formatters.py
│       └── constants.py
│
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
│
├── tests/                      # Test suite
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

#### Frontend Architecture

**Feature-Based Architecture**

```
frontend/
├── public/
│   └── assets/
│
├── src/
│   ├── main.tsx                # Application entry
│   ├── App.tsx                 # Root component
│   ├── router.tsx              # Route configuration
│   │
│   ├── features/               # Feature modules
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── services/
│   │   │   └── types.ts
│   │   │
│   │   ├── projects/
│   │   │   ├── components/
│   │   │   │   ├── ProjectList.tsx
│   │   │   │   ├── ProjectCard.tsx
│   │   │   │   └── CreateProjectModal.tsx
│   │   │   ├── hooks/
│   │   │   │   └── useProjects.ts
│   │   │   ├── services/
│   │   │   │   └── projectService.ts
│   │   │   └── types.ts
│   │   │
│   │   ├── upload/
│   │   │   ├── components/
│   │   │   │   ├── FileUploader.tsx
│   │   │   │   ├── ValidationStatus.tsx
│   │   │   │   └── DataQualityScore.tsx
│   │   │   ├── hooks/
│   │   │   └── services/
│   │   │
│   │   ├── modeling/
│   │   │   ├── components/
│   │   │   │   ├── AssumptionsForm.tsx
│   │   │   │   ├── ProductionAssumptions.tsx
│   │   │   │   ├── CostAssumptions.tsx
│   │   │   │   ├── SynergyAssumptions.tsx
│   │   │   │   └── DealStructure.tsx
│   │   │   ├── hooks/
│   │   │   └── services/
│   │   │
│   │   ├── scenarios/
│   │   │   ├── components/
│   │   │   │   ├── ScenarioManager.tsx
│   │   │   │   ├── ScenarioComparison.tsx
│   │   │   │   └── SensitivityTable.tsx
│   │   │   ├── hooks/
│   │   │   └── services/
│   │   │
│   │   └── visualizations/
│   │       ├── components/
│   │       │   ├── WaterfallChart.tsx
│   │       │   ├── IRRProjectionChart.tsx
│   │       │   ├── CashFlowChart.tsx
│   │       │   ├── ProductionDeclineChart.tsx
│   │       │   ├── EBITDAChart.tsx
│   │       │   ├── SynergyTimelineChart.tsx
│   │       │   └── DebtPaydownChart.tsx
│   │       ├── hooks/
│   │       └── utils/
│   │
│   ├── components/             # Shared components
│   │   ├── ui/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Select.tsx
│   │   │   ├── Table.tsx
│   │   │   └── Spinner.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── DashboardLayout.tsx
│   │   └── charts/
│   │       └── ChartContainer.tsx
│   │
│   ├── hooks/                  # Shared hooks
│   │   ├── useAuth.ts
│   │   ├── useTheme.ts
│   │   └── useDebounce.ts
│   │
│   ├── services/               # API services
│   │   ├── api.ts              # Axios instance
│   │   └── queryClient.ts      # React Query config
│   │
│   ├── store/                  # Zustand stores
│   │   ├── authStore.ts
│   │   ├── themeStore.ts
│   │   └── projectStore.ts
│   │
│   ├── types/                  # TypeScript types
│   │   ├── api.ts
│   │   ├── models.ts
│   │   └── charts.ts
│   │
│   ├── utils/                  # Utility functions
│   │   ├── formatters.ts
│   │   ├── validators.ts
│   │   └── constants.ts
│   │
│   └── styles/                 # Global styles
│       ├── index.css
│       └── tailwind.css
│
├── tests/
│   ├── unit/
│   └── e2e/
│
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
└── Dockerfile
```

### Communication Patterns

#### API Communication

**REST API with JSON**
- All endpoints return JSON responses
- Standard HTTP status codes
- Consistent error format

**Request/Response Flow:**

```
Client                    API Gateway              Service Layer           Database
  │                            │                         │                     │
  │  POST /api/v1/model/run   │                         │                     │
  ├───────────────────────────>│                         │                     │
  │                            │  Validate JWT           │                     │
  │                            │  Check permissions      │                     │
  │                            │  Validate request       │                     │
  │                            ├────────────────────────>│                     │
  │                            │                         │  Load assumptions   │
  │                            │                         ├────────────────────>│
  │                            │                         │<────────────────────┤
  │                            │                         │  Calculate metrics  │
  │                            │                         │  (IRR, NPV, etc.)   │
  │                            │                         │  Store results      │
  │                            │                         ├────────────────────>│
  │                            │<────────────────────────┤                     │
  │<───────────────────────────┤                         │                     │
  │  200 OK + results          │                         │                     │
```

#### Async Task Processing

For long-running calculations:

```
Client              API              Celery Worker         Database
  │                  │                      │                  │
  │  POST /model/run │                      │                  │
  ├─────────────────>│                      │                  │
  │                  │  Queue task          │                  │
  │                  ├─────────────────────>│                  │
  │  202 Accepted    │                      │                  │
  │  task_id: xyz    │                      │                  │
  │<─────────────────┤                      │                  │
  │                  │                      │  Process         │
  │                  │                      │  calculations    │
  │                  │                      ├─────────────────>│
  │                  │                      │  Store results   │
  │                  │                      │<─────────────────┤
  │                  │                      │                  │
  │  GET /tasks/xyz  │                      │                  │
  ├─────────────────>│                      │                  │
  │  200 OK          │                      │                  │
  │  status: complete│                      │                  │
  │<─────────────────┤                      │                  │
```

---


## Database Schema

### Entity Relationship Diagram

```
┌──────────────┐         ┌──────────────┐         ┌──────────────────┐
│    users     │         │   projects   │         │  uploaded_files  │
├──────────────┤         ├──────────────┤         ├──────────────────┤
│ id (PK)      │────┐    │ id (PK)      │────┐    │ id (PK)          │
│ email        │    │    │ user_id (FK) │    │    │ project_id (FK)  │
│ hashed_pwd   │    └───<│ name         │    └───<│ filename         │
│ full_name    │         │ description  │         │ file_type        │
│ role         │         │ created_at   │         │ file_size        │
│ is_active    │         │ updated_at   │         │ upload_date      │
│ created_at   │         └──────────────┘         │ validation_status│
└──────────────┘                │                 │ quality_score    │
                                │                 └──────────────────┘
                                │
                ┌───────────────┼───────────────┬──────────────────┐
                │               │               │                  │
                ▼               ▼               ▼                  ▼
    ┌──────────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ production_data  │ │   financial  │ │ assumptions  │ │  scenarios   │
    ├──────────────────┤ │     _data    │ ├──────────────┤ ├──────────────┤
    │ id (PK)          │ ├──────────────┤ │ id (PK)      │ │ id (PK)      │
    │ project_id (FK)  │ │ id (PK)      │ │ project_id   │ │ project_id   │
    │ date             │ │ project_id   │ │   (FK)       │ │   (FK)       │
    │ oil_production   │ │   (FK)       │ │ version      │ │ name         │
    │ gas_production   │ │ date         │ │ decline_type │ │ type         │
    │ oil_price        │ │ revenue      │ │ decline_rate │ │ assumptions  │
    │ gas_price        │ │ opex         │ │ oil_price    │ │   _id (FK)   │
    │ created_at       │ │ capex        │ │ gas_price    │ │ created_at   │
    └──────────────────┘ │ ebitda       │ │ opex_infl    │ └──────────────┘
                         │ created_at   │ │ capex_sched  │         │
                         └──────────────┘ │ discount_rate│         │
                                          │ tax_rate     │         │
                                          │ created_at   │         │
                                          └──────────────┘         │
                                                  │                │
                                                  │                │
                                          ┌───────┴────────┐       │
                                          │                │       │
                                          ▼                ▼       ▼
                                  ┌──────────────┐ ┌──────────────────┐
                                  │synergy_models│ │valuation_outputs │
                                  ├──────────────┤ ├──────────────────┤
                                  │ id (PK)      │ │ id (PK)          │
                                  │ assumptions  │ │ scenario_id (FK) │
                                  │   _id (FK)   │ │ year             │
                                  │ category     │ │ production       │
                                  │ target_value │ │ revenue          │
                                  │ ramp_schedule│ │ opex             │
                                  │ created_at   │ │ capex            │
                                  └──────────────┘ │ ebitda           │
                                                   │ fcf              │
                                                   │ npv              │
                                                   │ irr              │
                                                   │ created_at       │
                                                   └──────────────────┘

┌──────────────┐
│  audit_logs  │
├──────────────┤
│ id (PK)      │
│ user_id (FK) │
│ action       │
│ resource_type│
│ resource_id  │
│ details      │
│ ip_address   │
│ timestamp    │
└──────────────┘
```

### Table Definitions

#### users

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'analyst',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_role CHECK (role IN ('admin', 'analyst', 'viewer'))
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

**Roles:**
- `admin`: Full system access, user management
- `analyst`: Create/edit projects, run models
- `viewer`: Read-only access

#### projects

```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_status CHECK (status IN ('draft', 'active', 'archived'))
);

CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_created_at ON projects(created_at DESC);
```

#### uploaded_files

```sql
CREATE TABLE uploaded_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size INTEGER NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validation_status VARCHAR(50) DEFAULT 'pending',
    quality_score DECIMAL(5,2),
    validation_errors JSONB,
    
    CONSTRAINT chk_file_type CHECK (file_type IN ('production', 'financial', 'other')),
    CONSTRAINT chk_validation_status CHECK (validation_status IN ('pending', 'valid', 'invalid'))
);

CREATE INDEX idx_uploaded_files_project_id ON uploaded_files(project_id);
CREATE INDEX idx_uploaded_files_upload_date ON uploaded_files(upload_date DESC);
```

#### production_data

```sql
CREATE TABLE production_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    oil_production DECIMAL(15,2),  -- barrels
    gas_production DECIMAL(15,2),  -- MCF
    oil_price DECIMAL(10,2),       -- USD per barrel
    gas_price DECIMAL(10,2),       -- USD per MCF
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(project_id, date)
);

CREATE INDEX idx_production_data_project_id ON production_data(project_id);
CREATE INDEX idx_production_data_date ON production_data(date);
CREATE INDEX idx_production_data_project_date ON production_data(project_id, date);
```

#### financial_data

```sql
CREATE TABLE financial_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    revenue DECIMAL(15,2),
    opex DECIMAL(15,2),
    capex DECIMAL(15,2),
    loe DECIMAL(15,2),              -- Lease Operating Expenses
    transportation_cost DECIMAL(15,2),
    ga_expense DECIMAL(15,2),       -- G&A
    ebitda DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(project_id, date)
);

CREATE INDEX idx_financial_data_project_id ON financial_data(project_id);
CREATE INDEX idx_financial_data_date ON financial_data(date);
```

#### assumptions

```sql
CREATE TABLE assumptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    version INTEGER NOT NULL DEFAULT 1,
    name VARCHAR(255) NOT NULL,
    
    -- Production assumptions
    decline_curve_type VARCHAR(50) NOT NULL,
    decline_rate DECIMAL(5,4),
    hyperbolic_b DECIMAL(3,2),
    oil_price_forecast JSONB,      -- Array of {year, price}
    gas_price_forecast JSONB,
    
    -- Cost assumptions
    opex_inflation_rate DECIMAL(5,4),
    capex_schedule JSONB,          -- Array of {year, amount}
    transportation_cost_per_unit DECIMAL(10,2),
    ga_annual DECIMAL(15,2),
    
    -- Deal assumptions
    purchase_price DECIMAL(15,2),
    debt_amount DECIMAL(15,2),
    equity_amount DECIMAL(15,2),
    discount_rate DECIMAL(5,4),
    tax_rate DECIMAL(5,4),
    exit_multiple DECIMAL(4,2),
    forecast_years INTEGER DEFAULT 20,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_decline_curve CHECK (decline_curve_type IN ('exponential', 'hyperbolic', 'harmonic')),
    UNIQUE(project_id, version)
);

CREATE INDEX idx_assumptions_project_id ON assumptions(project_id);
CREATE INDEX idx_assumptions_version ON assumptions(project_id, version DESC);
```

#### synergy_models

```sql
CREATE TABLE synergy_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assumptions_id UUID NOT NULL REFERENCES assumptions(id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL,
    description TEXT,
    target_value DECIMAL(15,2) NOT NULL,
    realization_schedule JSONB NOT NULL,  -- Array of {year, percentage}
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_category CHECK (category IN (
        'operational_overhead',
        'procurement_efficiency',
        'workforce_consolidation',
        'shared_infrastructure'
    ))
);

CREATE INDEX idx_synergy_models_assumptions_id ON synergy_models(assumptions_id);
```

#### scenarios

```sql
CREATE TABLE scenarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    assumptions_id UUID NOT NULL REFERENCES assumptions(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    scenario_type VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_scenario_type CHECK (scenario_type IN ('bull', 'base', 'bear', 'custom')),
    UNIQUE(project_id, name)
);

CREATE INDEX idx_scenarios_project_id ON scenarios(project_id);
CREATE INDEX idx_scenarios_type ON scenarios(scenario_type);
```

#### valuation_outputs

```sql
CREATE TABLE valuation_outputs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scenario_id UUID NOT NULL REFERENCES scenarios(id) ON DELETE CASCADE,
    year INTEGER NOT NULL,
    
    -- Production forecasts
    oil_production DECIMAL(15,2),
    gas_production DECIMAL(15,2),
    
    -- Financial forecasts
    revenue DECIMAL(15,2),
    opex DECIMAL(15,2),
    capex DECIMAL(15,2),
    ebitda DECIMAL(15,2),
    ebitdax DECIMAL(15,2),
    depreciation DECIMAL(15,2),
    interest_expense DECIMAL(15,2),
    taxes DECIMAL(15,2),
    free_cash_flow DECIMAL(15,2),
    
    -- Synergies
    synergy_value DECIMAL(15,2),
    
    -- Debt
    debt_balance DECIMAL(15,2),
    debt_service DECIMAL(15,2),
    
    -- Valuation metrics (stored in year 0 or final year)
    npv DECIMAL(15,2),
    irr DECIMAL(7,4),
    payback_period DECIMAL(5,2),
    roic DECIMAL(7,4),
    terminal_value DECIMAL(15,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(scenario_id, year)
);

CREATE INDEX idx_valuation_outputs_scenario_id ON valuation_outputs(scenario_id);
CREATE INDEX idx_valuation_outputs_year ON valuation_outputs(scenario_id, year);
```

#### audit_logs

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id UUID,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_action CHECK (action IN (
        'login', 'logout', 'create', 'update', 'delete', 
        'upload', 'download', 'calculate', 'export'
    ))
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
```

### Data Retention Policy

| Table | Retention Period | Archive Strategy |
|-------|-----------------|------------------|
| users | Indefinite | Soft delete (is_active = false) |
| projects | 5 years after archive | Move to cold storage |
| uploaded_files | Same as project | Delete with project |
| production_data | Same as project | Delete with project |
| financial_data | Same as project | Delete with project |
| assumptions | Same as project | Delete with project |
| scenarios | Same as project | Delete with project |
| synergy_models | Same as project | Delete with project |
| valuation_outputs | Same as project | Delete with project |
| audit_logs | 7 years | Move to archive table |

### Backup Strategy

- **Full backups**: Daily at 2:00 AM UTC
- **Incremental backups**: Every 6 hours
- **Point-in-time recovery**: 30-day window
- **Backup retention**: 90 days
- **Backup location**: AWS S3 / Azure Blob Storage (encrypted)

---


## API Contracts

### API Design Principles

- RESTful architecture
- JSON request/response format
- Versioned endpoints (`/api/v1/`)
- Consistent error responses
- Pagination for list endpoints
- Rate limiting headers
- CORS enabled for frontend domain

### Authentication

#### POST /api/v1/auth/register

Register a new user account.

**Request:**
```json
{
  "email": "analyst@example.com",
  "password": "SecurePass123!",
  "full_name": "John Analyst"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "email": "analyst@example.com",
  "full_name": "John Analyst",
  "role": "analyst",
  "created_at": "2026-05-23T10:00:00Z"
}
```

#### POST /api/v1/auth/login

Authenticate and receive JWT token.

**Request:**
```json
{
  "email": "analyst@example.com",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": "uuid",
    "email": "analyst@example.com",
    "full_name": "John Analyst",
    "role": "analyst"
  }
}
```

### Project Management

#### GET /api/v1/projects

List all projects for authenticated user.

**Query Parameters:**
- `page` (integer, default: 1)
- `page_size` (integer, default: 20, max: 100)
- `status` (string, optional: draft|active|archived)
- `sort_by` (string, default: created_at)
- `sort_order` (string, default: desc)

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "Permian Basin Acquisition",
      "description": "Evaluation of 50 wells in Midland Basin",
      "status": "active",
      "created_at": "2026-05-20T10:00:00Z",
      "updated_at": "2026-05-23T10:00:00Z"
    }
  ],
  "total": 15,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

#### POST /api/v1/projects

Create a new project.

**Request:**
```json
{
  "name": "Eagle Ford Acquisition",
  "description": "Evaluation of 30 horizontal wells"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "name": "Eagle Ford Acquisition",
  "description": "Evaluation of 30 horizontal wells",
  "status": "draft",
  "created_at": "2026-05-23T10:00:00Z",
  "updated_at": "2026-05-23T10:00:00Z"
}
```

#### GET /api/v1/projects/{project_id}

Get project details.

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "name": "Permian Basin Acquisition",
  "description": "Evaluation of 50 wells in Midland Basin",
  "status": "active",
  "created_at": "2026-05-20T10:00:00Z",
  "updated_at": "2026-05-23T10:00:00Z",
  "files_count": 3,
  "scenarios_count": 3
}
```

#### PUT /api/v1/projects/{project_id}

Update project details.

**Request:**
```json
{
  "name": "Updated Project Name",
  "description": "Updated description",
  "status": "active"
}
```

**Response:** `200 OK`

#### DELETE /api/v1/projects/{project_id}

Delete a project and all associated data.

**Response:** `204 No Content`

### File Upload

#### POST /api/v1/upload/production

Upload production data file.

**Request:** `multipart/form-data`
- `file`: CSV or XLSX file
- `project_id`: UUID

**Response:** `202 Accepted`
```json
{
  "file_id": "uuid",
  "filename": "production_data.xlsx",
  "file_size": 1048576,
  "status": "processing",
  "message": "File uploaded successfully. Processing in background."
}
```

#### POST /api/v1/upload/financials

Upload financial data file.

**Request:** `multipart/form-data`
- `file`: CSV or XLSX file
- `project_id`: UUID

**Response:** `202 Accepted`

#### GET /api/v1/upload/{file_id}/status

Check file processing status.

**Response:** `200 OK`
```json
{
  "file_id": "uuid",
  "filename": "production_data.xlsx",
  "validation_status": "valid",
  "quality_score": 95.5,
  "rows_processed": 1200,
  "validation_errors": [],
  "completed_at": "2026-05-23T10:05:00Z"
}
```

### Modeling

#### POST /api/v1/assumptions

Create or update modeling assumptions.

**Request:**
```json
{
  "project_id": "uuid",
  "name": "Base Case Assumptions",
  "decline_curve_type": "hyperbolic",
  "decline_rate": 0.15,
  "hyperbolic_b": 0.5,
  "oil_price_forecast": [
    {"year": 2026, "price": 75.00},
    {"year": 2027, "price": 77.50}
  ],
  "gas_price_forecast": [
    {"year": 2026, "price": 3.50},
    {"year": 2027, "price": 3.75}
  ],
  "opex_inflation_rate": 0.03,
  "capex_schedule": [
    {"year": 2026, "amount": 5000000},
    {"year": 2027, "amount": 3000000}
  ],
  "transportation_cost_per_unit": 2.50,
  "ga_annual": 1000000,
  "purchase_price": 50000000,
  "debt_amount": 30000000,
  "equity_amount": 20000000,
  "discount_rate": 0.12,
  "tax_rate": 0.25,
  "exit_multiple": 5.0,
  "forecast_years": 20
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "project_id": "uuid",
  "version": 1,
  "name": "Base Case Assumptions",
  "created_at": "2026-05-23T10:00:00Z"
}
```

#### POST /api/v1/synergies

Add synergy assumptions.

**Request:**
```json
{
  "assumptions_id": "uuid",
  "synergies": [
    {
      "category": "operational_overhead",
      "description": "Eliminate duplicate G&A functions",
      "target_value": 2000000,
      "realization_schedule": [
        {"year": 1, "percentage": 0.25},
        {"year": 2, "percentage": 0.60},
        {"year": 3, "percentage": 0.85},
        {"year": 4, "percentage": 1.00}
      ]
    },
    {
      "category": "procurement_efficiency",
      "description": "Volume discounts on services",
      "target_value": 1500000,
      "realization_schedule": [
        {"year": 1, "percentage": 0.30},
        {"year": 2, "percentage": 0.70},
        {"year": 3, "percentage": 1.00}
      ]
    }
  ]
}
```

**Response:** `201 Created`

#### POST /api/v1/model/run

Execute valuation model.

**Request:**
```json
{
  "project_id": "uuid",
  "assumptions_id": "uuid",
  "scenarios": ["bull", "base", "bear"]
}
```

**Response:** `202 Accepted`
```json
{
  "task_id": "uuid",
  "status": "processing",
  "message": "Valuation calculation started. Check status at /api/v1/tasks/{task_id}"
}
```

#### GET /api/v1/tasks/{task_id}

Check calculation task status.

**Response:** `200 OK`
```json
{
  "task_id": "uuid",
  "status": "completed",
  "progress": 100,
  "result": {
    "scenarios_calculated": 3,
    "scenario_ids": ["uuid1", "uuid2", "uuid3"]
  },
  "completed_at": "2026-05-23T10:10:00Z"
}
```

#### GET /api/v1/model/results/{project_id}

Get valuation results for a project.

**Query Parameters:**
- `scenario_id` (UUID, optional): Filter by specific scenario

**Response:** `200 OK`
```json
{
  "project_id": "uuid",
  "scenarios": [
    {
      "scenario_id": "uuid",
      "name": "Base Case",
      "type": "base",
      "metrics": {
        "npv": 15234567.89,
        "irr": 0.1845,
        "payback_period": 4.2,
        "roic": 0.2156
      },
      "cash_flows": [
        {
          "year": 0,
          "oil_production": 0,
          "gas_production": 0,
          "revenue": 0,
          "opex": 0,
          "capex": 50000000,
          "ebitda": 0,
          "free_cash_flow": -50000000
        },
        {
          "year": 1,
          "oil_production": 365000,
          "gas_production": 1825000,
          "revenue": 33743750,
          "opex": 7300000,
          "capex": 5000000,
          "ebitda": 26443750,
          "free_cash_flow": 18082812.50
        }
      ]
    }
  ]
}
```

### Scenarios

#### POST /api/v1/scenarios

Create a new scenario.

**Request:**
```json
{
  "project_id": "uuid",
  "assumptions_id": "uuid",
  "name": "Optimistic Case",
  "scenario_type": "bull",
  "description": "High commodity prices, low decline rates"
}
```

**Response:** `201 Created`

#### GET /api/v1/scenarios/{scenario_id}

Get scenario details and results.

**Response:** `200 OK`

#### PUT /api/v1/scenarios/{scenario_id}

Update scenario configuration.

**Response:** `200 OK`

#### DELETE /api/v1/scenarios/{scenario_id}

Delete a scenario.

**Response:** `204 No Content`

#### GET /api/v1/scenarios/compare

Compare multiple scenarios.

**Query Parameters:**
- `scenario_ids`: Comma-separated list of UUIDs

**Response:** `200 OK`
```json
{
  "comparison": [
    {
      "scenario_id": "uuid1",
      "name": "Bull Case",
      "npv": 25000000,
      "irr": 0.22,
      "payback_period": 3.5
    },
    {
      "scenario_id": "uuid2",
      "name": "Base Case",
      "npv": 15000000,
      "irr": 0.18,
      "payback_period": 4.2
    },
    {
      "scenario_id": "uuid3",
      "name": "Bear Case",
      "npv": 8000000,
      "irr": 0.14,
      "payback_period": 5.8
    }
  ]
}
```

### Sensitivity Analysis

#### POST /api/v1/sensitivity

Run sensitivity analysis.

**Request:**
```json
{
  "scenario_id": "uuid",
  "variable1": {
    "name": "oil_price",
    "values": [60, 70, 80, 90, 100]
  },
  "variable2": {
    "name": "discount_rate",
    "values": [0.08, 0.10, 0.12, 0.14, 0.16]
  },
  "output_metric": "npv"
}
```

**Response:** `200 OK`
```json
{
  "sensitivity_table": {
    "variable1": "oil_price",
    "variable2": "discount_rate",
    "output_metric": "npv",
    "results": [
      [12000000, 10500000, 9200000, 8100000, 7200000],
      [15000000, 13200000, 11600000, 10200000, 9000000],
      [18000000, 15900000, 14000000, 12300000, 10800000],
      [21000000, 18600000, 16400000, 14400000, 12600000],
      [24000000, 21300000, 18800000, 16500000, 14400000]
    ]
  }
}
```

### Visualization

#### GET /api/v1/charts/waterfall/{scenario_id}

Get waterfall chart data.

**Response:** `200 OK`
```json
{
  "scenario_id": "uuid",
  "chart_data": {
    "categories": [
      "Base EBITDA",
      "Revenue Synergies",
      "Cost Synergies",
      "Operational Efficiencies",
      "Financing Impact",
      "Final EBITDA"
    ],
    "values": [20000000, 1500000, 2000000, 1000000, -500000, 24000000],
    "cumulative": [20000000, 21500000, 23500000, 24500000, 24000000, 24000000]
  }
}
```

#### GET /api/v1/charts/irr/{project_id}

Get IRR projection chart data.

**Query Parameters:**
- `scenario_ids`: Comma-separated list of UUIDs

**Response:** `200 OK`
```json
{
  "project_id": "uuid",
  "scenarios": [
    {
      "scenario_id": "uuid",
      "name": "Base Case",
      "data": [
        {"year": 1, "irr": 0.05},
        {"year": 2, "irr": 0.10},
        {"year": 3, "irr": 0.15},
        {"year": 4, "irr": 0.18},
        {"year": 5, "irr": 0.18}
      ]
    }
  ]
}
```

#### GET /api/v1/charts/cashflow/{scenario_id}

Get cash flow chart data.

**Response:** `200 OK`
```json
{
  "scenario_id": "uuid",
  "years": [2026, 2027, 2028, 2029, 2030],
  "revenue": [33743750, 31256437, 28970205, 26871690, 24948366],
  "opex": [7300000, 7519000, 7744570, 7976907, 8216414],
  "capex": [5000000, 3000000, 2000000, 2000000, 2000000],
  "free_cash_flow": [18082812, 17737437, 16225635, 14894783, 12731952]
}
```

### Data Export

#### GET /api/v1/export/project/{project_id}

Export complete project data to Excel.

**Query Parameters:**
- `include_scenarios`: boolean (default: true)
- `include_charts`: boolean (default: false)

**Response:** `200 OK`
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Content-Disposition: `attachment; filename="project_export.xlsx"`

#### GET /api/v1/export/scenario/{scenario_id}

Export scenario results to Excel.

**Response:** `200 OK`
- Excel file with multiple sheets (Summary, Cash Flows, Assumptions, Charts)

### Error Responses

All error responses follow this format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "discount_rate",
        "message": "Must be between 0 and 1"
      }
    ],
    "timestamp": "2026-05-23T10:00:00Z",
    "request_id": "uuid"
  }
}
```

**Error Codes:**
- `AUTHENTICATION_ERROR` (401)
- `AUTHORIZATION_ERROR` (403)
- `NOT_FOUND` (404)
- `VALIDATION_ERROR` (400)
- `RATE_LIMIT_EXCEEDED` (429)
- `INTERNAL_SERVER_ERROR` (500)
- `SERVICE_UNAVAILABLE` (503)

### Rate Limiting

Response headers include:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 995
X-RateLimit-Reset: 1716465600
```

---


## Frontend Architecture

### Component Hierarchy

```
App
├── Router
│   ├── PublicRoutes
│   │   ├── LoginPage
│   │   └── RegisterPage
│   │
│   └── ProtectedRoutes
│       ├── DashboardLayout
│       │   ├── Header
│       │   ├── Sidebar
│       │   └── MainContent
│       │
│       ├── ProjectsPage
│       │   ├── ProjectList
│       │   ├── ProjectCard
│       │   └── CreateProjectModal
│       │
│       ├── ProjectDetailPage
│       │   ├── ProjectHeader
│       │   ├── TabNavigation
│       │   ├── DataTab
│       │   │   ├── FileUploader
│       │   │   ├── ValidationStatus
│       │   │   └── DataQualityScore
│       │   ├── ModelingTab
│       │   │   ├── AssumptionsForm
│       │   │   ├── ProductionAssumptions
│       │   │   ├── CostAssumptions
│       │   │   ├── SynergyAssumptions
│       │   │   └── DealStructure
│       │   ├── ScenariosTab
│       │   │   ├── ScenarioManager
│       │   │   ├── ScenarioComparison
│       │   │   └── SensitivityTable
│       │   └── VisualizationsTab
│       │       ├── WaterfallChart
│       │       ├── IRRProjectionChart
│       │       ├── CashFlowChart
│       │       ├── ProductionDeclineChart
│       │       ├── EBITDAChart
│       │       ├── SynergyTimelineChart
│       │       └── DebtPaydownChart
│       │
│       └── SettingsPage
│           ├── ProfileSettings
│           └── ThemeSettings
```

### State Management Strategy

#### Zustand Stores

**authStore.ts**
```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}
```

**projectStore.ts**
```typescript
interface ProjectState {
  currentProject: Project | null;
  projects: Project[];
  setCurrentProject: (project: Project) => void;
  updateProject: (id: string, data: Partial<Project>) => void;
}
```

**themeStore.ts**
```typescript
interface ThemeState {
  mode: 'light' | 'dark';
  toggleTheme: () => void;
  setTheme: (mode: 'light' | 'dark') => void;
}
```

#### React Query for Server State

```typescript
// Custom hooks for data fetching
export const useProjects = () => {
  return useQuery({
    queryKey: ['projects'],
    queryFn: fetchProjects,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useProjectDetails = (projectId: string) => {
  return useQuery({
    queryKey: ['project', projectId],
    queryFn: () => fetchProjectDetails(projectId),
    enabled: !!projectId,
  });
};

export const useValuationResults = (projectId: string) => {
  return useQuery({
    queryKey: ['valuation', projectId],
    queryFn: () => fetchValuationResults(projectId),
    refetchInterval: 5000, // Poll every 5 seconds if calculating
  });
};

// Mutations
export const useCreateProject = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: createProject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
    },
  });
};
```

### Design System

#### Color Palette

**Light Mode:**
```css
--primary: #1e40af;        /* Blue 800 */
--primary-hover: #1e3a8a;  /* Blue 900 */
--secondary: #059669;      /* Emerald 600 */
--accent: #f59e0b;         /* Amber 500 */
--background: #ffffff;
--surface: #f9fafb;        /* Gray 50 */
--text-primary: #111827;   /* Gray 900 */
--text-secondary: #6b7280; /* Gray 500 */
--border: #e5e7eb;         /* Gray 200 */
--error: #dc2626;          /* Red 600 */
--success: #10b981;        /* Emerald 500 */
--warning: #f59e0b;        /* Amber 500 */
```

**Dark Mode:**
```css
--primary: #3b82f6;        /* Blue 500 */
--primary-hover: #2563eb;  /* Blue 600 */
--secondary: #10b981;      /* Emerald 500 */
--accent: #fbbf24;         /* Amber 400 */
--background: #0f172a;     /* Slate 900 */
--surface: #1e293b;        /* Slate 800 */
--text-primary: #f1f5f9;   /* Slate 100 */
--text-secondary: #94a3b8; /* Slate 400 */
--border: #334155;         /* Slate 700 */
--error: #ef4444;          /* Red 500 */
--success: #10b981;        /* Emerald 500 */
--warning: #fbbf24;        /* Amber 400 */
```

#### Typography

```css
/* Headings */
.heading-1 { font-size: 2.25rem; font-weight: 700; line-height: 2.5rem; }
.heading-2 { font-size: 1.875rem; font-weight: 600; line-height: 2.25rem; }
.heading-3 { font-size: 1.5rem; font-weight: 600; line-height: 2rem; }
.heading-4 { font-size: 1.25rem; font-weight: 600; line-height: 1.75rem; }

/* Body */
.body-large { font-size: 1.125rem; line-height: 1.75rem; }
.body-normal { font-size: 1rem; line-height: 1.5rem; }
.body-small { font-size: 0.875rem; line-height: 1.25rem; }

/* Labels */
.label { font-size: 0.875rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
```

#### Spacing System

```css
--spacing-xs: 0.25rem;   /* 4px */
--spacing-sm: 0.5rem;    /* 8px */
--spacing-md: 1rem;      /* 16px */
--spacing-lg: 1.5rem;    /* 24px */
--spacing-xl: 2rem;      /* 32px */
--spacing-2xl: 3rem;     /* 48px */
--spacing-3xl: 4rem;     /* 64px */
```

### Key UI Components

#### Card Component

```tsx
interface CardProps {
  title?: string;
  subtitle?: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
  className?: string;
}

export const Card: React.FC<CardProps> = ({
  title,
  subtitle,
  children,
  actions,
  className
}) => {
  return (
    <div className={`bg-surface rounded-lg shadow-md border border-border ${className}`}>
      {(title || actions) && (
        <div className="px-6 py-4 border-b border-border flex justify-between items-center">
          <div>
            {title && <h3 className="heading-4 text-text-primary">{title}</h3>}
            {subtitle && <p className="body-small text-text-secondary mt-1">{subtitle}</p>}
          </div>
          {actions && <div>{actions}</div>}
        </div>
      )}
      <div className="p-6">{children}</div>
    </div>
  );
};
```

#### Button Component

```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  children,
  onClick
}) => {
  const baseClasses = 'rounded-md font-medium transition-colors focus:outline-none focus:ring-2';
  
  const variantClasses = {
    primary: 'bg-primary text-white hover:bg-primary-hover',
    secondary: 'bg-secondary text-white hover:bg-secondary/90',
    outline: 'border-2 border-primary text-primary hover:bg-primary hover:text-white',
    ghost: 'text-primary hover:bg-primary/10'
  };
  
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };
  
  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}
      disabled={disabled || loading}
      onClick={onClick}
    >
      {loading ? <Spinner size="sm" /> : children}
    </button>
  );
};
```

### Chart Components

#### Waterfall Chart

```tsx
import { Bar } from 'react-chartjs-2';

interface WaterfallChartProps {
  data: {
    categories: string[];
    values: number[];
    cumulative: number[];
  };
}

export const WaterfallChart: React.FC<WaterfallChartProps> = ({ data }) => {
  const chartData = {
    labels: data.categories,
    datasets: [
      {
        label: 'Value',
        data: data.values,
        backgroundColor: data.values.map(v => v >= 0 ? '#10b981' : '#ef4444'),
      }
    ]
  };
  
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            return `$${(context.parsed.y / 1000000).toFixed(2)}M`;
          }
        }
      }
    },
    scales: {
      y: {
        ticks: {
          callback: (value: number) => `$${(value / 1000000).toFixed(0)}M`
        }
      }
    }
  };
  
  return (
    <div className="h-96">
      <Bar data={chartData} options={options} />
    </div>
  );
};
```

#### IRR Projection Chart

```tsx
import { Line } from 'react-chartjs-2';

interface IRRProjectionChartProps {
  scenarios: Array<{
    name: string;
    data: Array<{ year: number; irr: number }>;
  }>;
}

export const IRRProjectionChart: React.FC<IRRProjectionChartProps> = ({ scenarios }) => {
  const chartData = {
    labels: scenarios[0].data.map(d => d.year),
    datasets: scenarios.map((scenario, index) => ({
      label: scenario.name,
      data: scenario.data.map(d => d.irr * 100),
      borderColor: ['#3b82f6', '#10b981', '#ef4444'][index],
      backgroundColor: ['#3b82f6', '#10b981', '#ef4444'][index] + '20',
      tension: 0.4,
    }))
  };
  
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' as const },
      tooltip: {
        callbacks: {
          label: (context: any) => `${context.dataset.label}: ${context.parsed.y.toFixed(2)}%`
        }
      }
    },
    scales: {
      y: {
        ticks: {
          callback: (value: number) => `${value}%`
        }
      }
    }
  };
  
  return (
    <div className="h-96">
      <Line data={chartData} options={options} />
    </div>
  );
};
```

### Responsive Design

**Breakpoints:**
```css
/* Mobile: < 640px */
/* Tablet: 640px - 1024px */
/* Desktop: > 1024px */

@media (max-width: 640px) {
  /* Stack charts vertically */
  /* Hide sidebar, show hamburger menu */
  /* Simplify data tables */
}

@media (min-width: 641px) and (max-width: 1024px) {
  /* 2-column grid for charts */
  /* Collapsible sidebar */
}

@media (min-width: 1025px) {
  /* 3-column grid for charts */
  /* Full sidebar visible */
  /* Multi-panel layouts */
}
```

### Accessibility

- Semantic HTML elements
- ARIA labels for interactive elements
- Keyboard navigation support (Tab, Enter, Escape)
- Focus indicators
- Screen reader announcements for dynamic content
- Color contrast ratios meeting WCAG 2.1 AA standards
- Alt text for images and icons

### Performance Optimization

- Code splitting by route
- Lazy loading for charts
- Virtual scrolling for large data tables
- Debounced search inputs
- Memoized expensive calculations
- Image optimization
- Bundle size monitoring

---


## Visualization Design

### Chart Specifications

#### 1. Waterfall Chart - Value Creation Breakdown

**Purpose:** Visualize sequential value contributions from base EBITDA to final projected margin.

**Data Structure:**
```typescript
interface WaterfallData {
  categories: string[];
  values: number[];        // Incremental values
  cumulative: number[];    // Running totals
}
```

**Visual Design:**
- Positive contributions: Green bars
- Negative contributions: Red bars
- Connecting lines between bars showing cumulative flow
- Final bar highlighted with distinct color
- Y-axis: Dollar values (millions)
- Hover tooltips: Show exact value and percentage of total

**Implementation:** Chart.js with custom waterfall plugin or Recharts ComposedChart

---

#### 2. IRR Projection Chart - Multi-Year Return Profile

**Purpose:** Display IRR evolution over time across multiple scenarios.

**Data Structure:**
```typescript
interface IRRProjectionData {
  scenarios: Array<{
    name: string;
    type: 'bull' | 'base' | 'bear';
    data: Array<{ year: number; irr: number }>;
  }>;
  targetIRR?: number;  // Reference line
}
```

**Visual Design:**
- Line chart with 3 series (Bull/Base/Bear)
- Color coding: Blue (Bull), Green (Base), Red (Bear)
- Dashed horizontal line for target IRR threshold
- Shaded confidence intervals (optional)
- X-axis: Years
- Y-axis: IRR percentage
- Interactive legend to toggle scenarios
- Zoom and pan capabilities

---

#### 3. Cash Flow Forecast Chart - Component Breakdown

**Purpose:** Show annual cash flow components in stacked format.

**Data Structure:**
```typescript
interface CashFlowData {
  years: number[];
  revenue: number[];
  opex: number[];
  capex: number[];
  freeCashFlow: number[];
  synergies?: number[];
}
```

**Visual Design:**
- Stacked bar chart for components
- Line overlay for free cash flow
- Color scheme:
  - Revenue: Blue
  - OPEX: Orange (negative)
  - CAPEX: Red (negative)
  - Synergies: Green
  - FCF line: Purple
- Toggle visibility of individual components
- Dual Y-axis if needed

---

#### 4. Production Decline Curve - Historical vs. Forecast

**Purpose:** Validate production forecasts against historical data.

**Data Structure:**
```typescript
interface ProductionDeclineData {
  historical: Array<{ date: Date; oil: number; gas: number }>;
  forecast: Array<{ date: Date; oil: number; gas: number }>;
  declineModel: {
    type: 'exponential' | 'hyperbolic' | 'harmonic';
    parameters: Record<string, number>;
  };
}
```

**Visual Design:**
- Dual-axis line chart (oil on left, gas on right)
- Solid lines for historical data
- Dashed lines for forecasted data
- Vertical line marking transition point
- Shaded area showing forecast uncertainty range
- Annotation showing decline model parameters

---

#### 5. EBITDA Trend Chart - Profitability Over Time

**Purpose:** Track EBITDA evolution with synergy contributions.

**Data Structure:**
```typescript
interface EBITDATrendData {
  periods: string[];  // Monthly, quarterly, or annual
  baseEBITDA: number[];
  synergies: number[];
  totalEBITDA: number[];
  ebitdax?: number[];
}
```

**Visual Design:**
- Stacked area chart
- Base EBITDA: Light blue area
- Synergies: Green area on top
- EBITDAX line (if applicable): Dashed line
- Gradient fills for visual appeal
- Hover shows breakdown

---

#### 6. Synergy Realization Timeline - Value Capture Schedule

**Purpose:** Display synergy realization by category over time.

**Data Structure:**
```typescript
interface SynergyTimelineData {
  years: number[];
  categories: Array<{
    name: string;
    values: number[];  // Realized value per year
    target: number;    // Total target value
  }>;
}
```

**Visual Design:**
- Stacked area chart
- Each category: Different color
- Categories:
  - Operational Overhead: Blue
  - Procurement: Green
  - Workforce: Orange
  - Infrastructure: Purple
- Cumulative line overlay
- Target achievement markers

---

#### 7. Debt Paydown Chart - Leverage Reduction

**Purpose:** Show debt balance reduction and coverage ratios.

**Data Structure:**
```typescript
interface DebtPaydownData {
  years: number[];
  debtBalance: number[];
  principalPayment: number[];
  interestPayment: number[];
  debtServiceCoverage: number[];
}
```

**Visual Design:**
- Combination chart
- Area chart for debt balance (declining)
- Stacked bars for principal + interest payments
- Line chart for debt service coverage ratio (secondary axis)
- Horizontal reference line at 1.2x DSCR threshold
- Red zone highlighting when DSCR < 1.2x

---

### Chart Interaction Patterns

**Common Interactions:**
- **Hover:** Display detailed tooltip with exact values
- **Click:** Drill down to underlying data
- **Legend Toggle:** Show/hide data series
- **Zoom:** Mouse wheel or pinch gesture
- **Pan:** Click and drag
- **Export:** Download as PNG, SVG, or data as CSV

**Responsive Behavior:**
- Desktop: Full-featured charts with all interactions
- Tablet: Simplified tooltips, touch-optimized
- Mobile: Essential data only, vertical scrolling

---

## Calculation Engine Structure

### Engine Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Valuation Service                          │
│  (Orchestrates all calculation engines)                      │
└─────────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┬─────────────────┐
        │                 │                 │                 │
        ▼                 ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Forecasting  │  │   Synergy    │  │     IRR      │  │   Scenario   │
│   Engine     │  │   Engine     │  │   Engine     │  │   Engine     │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │                 │
        └─────────────────┴─────────────────┴─────────────────┘
                          │
                          ▼
                ┌──────────────────┐
                │  Decline Curves  │
                │     Module       │
                └──────────────────┘
```

### Module Specifications

#### 1. Decline Curves Module (`decline_curves.py`)

```python
from enum import Enum
from typing import List
import numpy as np

class DeclineType(Enum):
    EXPONENTIAL = "exponential"
    HYPERBOLIC = "hyperbolic"
    HARMONIC = "harmonic"

class DeclineCurve:
    """Base class for production decline curves."""
    
    def __init__(self, initial_rate: float, decline_rate: float):
        self.initial_rate = initial_rate
        self.decline_rate = decline_rate
    
    def forecast(self, periods: int) -> np.ndarray:
        """Generate production forecast for specified periods."""
        raise NotImplementedError

class ExponentialDecline(DeclineCurve):
    """Exponential decline: Q(t) = Q_i * e^(-D * t)"""
    
    def forecast(self, periods: int) -> np.ndarray:
        t = np.arange(0, periods)
        return self.initial_rate * np.exp(-self.decline_rate * t)

class HyperbolicDecline(DeclineCurve):
    """Hyperbolic decline: Q(t) = Q_i / (1 + b * D_i * t)^(1/b)"""
    
    def __init__(self, initial_rate: float, decline_rate: float, b_factor: float):
        super().__init__(initial_rate, decline_rate)
        self.b_factor = b_factor
    
    def forecast(self, periods: int) -> np.ndarray:
        t = np.arange(0, periods)
        return self.initial_rate / np.power(
            1 + self.b_factor * self.decline_rate * t,
            1 / self.b_factor
        )

class HarmonicDecline(DeclineCurve):
    """Harmonic decline: Q(t) = Q_i / (1 + D_i * t)"""
    
    def forecast(self, periods: int) -> np.ndarray:
        t = np.arange(0, periods)
        return self.initial_rate / (1 + self.decline_rate * t)
```

---

#### 2. Forecasting Engine (`forecasting_engine.py`)

```python
import pandas as pd
import numpy as np
from typing import Dict, List
from .decline_curves import DeclineCurve

class ForecastingEngine:
    """Generates production and financial forecasts."""
    
    def __init__(self, assumptions: Dict):
        self.assumptions = assumptions
        self.forecast_years = assumptions.get('forecast_years', 20)
    
    def forecast_production(
        self,
        historical_data: pd.DataFrame,
        decline_curve: DeclineCurve
    ) -> pd.DataFrame:
        """
        Forecast oil and gas production using decline curves.
        
        Args:
            historical_data: DataFrame with historical production
            decline_curve: Decline curve model instance
        
        Returns:
            DataFrame with forecasted production by year
        """
        # Get last historical production rate
        last_oil_rate = historical_data['oil_production'].iloc[-1]
        last_gas_rate = historical_data['gas_production'].iloc[-1]
        
        # Generate forecasts
        oil_forecast = decline_curve.forecast(self.forecast_years)
        gas_forecast = decline_curve.forecast(self.forecast_years)
        
        # Scale to match last historical rate
        oil_forecast = oil_forecast * (last_oil_rate / oil_forecast[0])
        gas_forecast = gas_forecast * (last_gas_rate / gas_forecast[0])
        
        # Create forecast DataFrame
        years = np.arange(1, self.forecast_years + 1)
        forecast_df = pd.DataFrame({
            'year': years,
            'oil_production': oil_forecast,
            'gas_production': gas_forecast
        })
        
        return forecast_df
    
    def forecast_revenue(
        self,
        production_forecast: pd.DataFrame,
        price_forecast: Dict[str, List[Dict]]
    ) -> pd.DataFrame:
        """
        Calculate revenue forecast from production and prices.
        
        Args:
            production_forecast: DataFrame with production forecasts
            price_forecast: Dict with oil_price and gas_price arrays
        
        Returns:
            DataFrame with revenue by year
        """
        df = production_forecast.copy()
        
        # Map price forecasts to years
        oil_prices = self._map_prices_to_years(price_forecast['oil_price'])
        gas_prices = self._map_prices_to_years(price_forecast['gas_price'])
        
        # Calculate revenue
        df['oil_revenue'] = df['oil_production'] * oil_prices
        df['gas_revenue'] = df['gas_production'] * gas_prices
        df['total_revenue'] = df['oil_revenue'] + df['gas_revenue']
        
        return df
    
    def forecast_opex(
        self,
        production_forecast: pd.DataFrame,
        base_opex: float,
        inflation_rate: float
    ) -> pd.DataFrame:
        """
        Forecast operating expenses with inflation.
        
        Args:
            production_forecast: DataFrame with production forecasts
            base_opex: Base year OPEX
            inflation_rate: Annual inflation rate
        
        Returns:
            DataFrame with OPEX by year
        """
        df = production_forecast[['year']].copy()
        
        # Apply inflation
        df['opex'] = base_opex * np.power(1 + inflation_rate, df['year'])
        
        return df
    
    def forecast_capex(
        self,
        capex_schedule: List[Dict]
    ) -> pd.DataFrame:
        """
        Map CAPEX schedule to forecast years.
        
        Args:
            capex_schedule: List of {year, amount} dicts
        
        Returns:
            DataFrame with CAPEX by year
        """
        years = np.arange(1, self.forecast_years + 1)
        capex_map = {item['year']: item['amount'] for item in capex_schedule}
        
        df = pd.DataFrame({
            'year': years,
            'capex': [capex_map.get(year, 0) for year in years]
        })
        
        return df
    
    def _map_prices_to_years(self, price_forecast: List[Dict]) -> np.ndarray:
        """Helper to map price forecast to all years."""
        price_map = {item['year']: item['price'] for item in price_forecast}
        years = np.arange(1, self.forecast_years + 1)
        
        # Use last known price for years beyond forecast
        last_price = price_forecast[-1]['price']
        prices = np.array([price_map.get(year, last_price) for year in years])
        
        return prices
```

---

#### 3. Synergy Engine (`synergy_engine.py`)

```python
import pandas as pd
import numpy as np
from typing import List, Dict

class SynergyEngine:
    """Models operational synergies and realization schedules."""
    
    def calculate_synergies(
        self,
        synergy_models: List[Dict],
        forecast_years: int
    ) -> pd.DataFrame:
        """
        Calculate realized synergies by year and category.
        
        Args:
            synergy_models: List of synergy model dicts
            forecast_years: Number of years to forecast
        
        Returns:
            DataFrame with synergy values by year and category
        """
        years = np.arange(1, forecast_years + 1)
        synergy_df = pd.DataFrame({'year': years})
        
        for model in synergy_models:
            category = model['category']
            target_value = model['target_value']
            schedule = model['realization_schedule']
            
            # Map realization percentages to years
            realization_map = {item['year']: item['percentage'] for item in schedule}
            
            # Assume 100% realization after last scheduled year
            max_scheduled_year = max(item['year'] for item in schedule)
            
            realized_values = []
            for year in years:
                if year <= max_scheduled_year:
                    percentage = realization_map.get(year, 0)
                else:
                    percentage = 1.0
                
                realized_values.append(target_value * percentage)
            
            synergy_df[category] = realized_values
        
        # Calculate total synergies
        category_columns = [col for col in synergy_df.columns if col != 'year']
        synergy_df['total_synergies'] = synergy_df[category_columns].sum(axis=1)
        
        return synergy_df
```

---

#### 4. IRR Engine (`irr_engine.py`)

```python
import numpy as np
from scipy.optimize import newton
from typing import List

class IRREngine:
    """Calculates Internal Rate of Return using Newton-Raphson method."""
    
    def __init__(self, tolerance: float = 0.0001, max_iterations: int = 100):
        self.tolerance = tolerance
        self.max_iterations = max_iterations
    
    def calculate_irr(self, cash_flows: List[float]) -> float:
        """
        Calculate IRR for a series of cash flows.
        
        Args:
            cash_flows: List of cash flows (initial investment should be negative)
        
        Returns:
            IRR as a decimal (e.g., 0.15 for 15%)
        
        Raises:
            ValueError: If IRR cannot be calculated
        """
        # Initial guess: 10%
        initial_guess = 0.10
        
        try:
            irr = newton(
                func=self._npv_function,
                x0=initial_guess,
                fprime=self._npv_derivative,
                args=(cash_flows,),
                tol=self.tolerance,
                maxiter=self.max_iterations
            )
            return irr
        except RuntimeError:
            raise ValueError("IRR calculation did not converge")
    
    def _npv_function(self, rate: float, cash_flows: List[float]) -> float:
        """NPV function for root finding."""
        return sum(cf / (1 + rate) ** t for t, cf in enumerate(cash_flows))
    
    def _npv_derivative(self, rate: float, cash_flows: List[float]) -> float:
        """Derivative of NPV function for Newton-Raphson."""
        return sum(-t * cf / (1 + rate) ** (t + 1) for t, cf in enumerate(cash_flows))
    
    def calculate_npv(self, cash_flows: List[float], discount_rate: float) -> float:
        """
        Calculate Net Present Value.
        
        Args:
            cash_flows: List of cash flows
            discount_rate: Discount rate as decimal
        
        Returns:
            NPV value
        """
        return sum(cf / (1 + discount_rate) ** t for t, cf in enumerate(cash_flows))
```

---

#### 5. Valuation Service (`valuation_service.py`)

```python
import pandas as pd
from typing import Dict, List
from .forecasting_engine import ForecastingEngine
from .synergy_engine import SynergyEngine
from .irr_engine import IRREngine
from .decline_curves import ExponentialDecline, HyperbolicDecline, HarmonicDecline

class ValuationService:
    """Main orchestrator for valuation calculations."""
    
    def __init__(self):
        self.forecasting_engine = ForecastingEngine({})
        self.synergy_engine = SynergyEngine()
        self.irr_engine = IRREngine()
    
    def run_valuation(
        self,
        historical_data: pd.DataFrame,
        assumptions: Dict,
        synergy_models: List[Dict]
    ) -> Dict:
        """
        Execute complete valuation workflow.
        
        Args:
            historical_data: Historical production and financial data
            assumptions: Modeling assumptions
            synergy_models: Synergy model configurations
        
        Returns:
            Dict containing all valuation outputs
        """
        # 1. Initialize forecasting engine with assumptions
        self.forecasting_engine = ForecastingEngine(assumptions)
        forecast_years = assumptions.get('forecast_years', 20)
        
        # 2. Create decline curve model
        decline_curve = self._create_decline_curve(assumptions)
        
        # 3. Forecast production
        production_forecast = self.forecasting_engine.forecast_production(
            historical_data, decline_curve
        )
        
        # 4. Forecast revenue
        revenue_forecast = self.forecasting_engine.forecast_revenue(
            production_forecast,
            {
                'oil_price': assumptions['oil_price_forecast'],
                'gas_price': assumptions['gas_price_forecast']
            }
        )
        
        # 5. Forecast OPEX
        base_opex = historical_data['opex'].mean()
        opex_forecast = self.forecasting_engine.forecast_opex(
            production_forecast,
            base_opex,
            assumptions['opex_inflation_rate']
        )
        
        # 6. Forecast CAPEX
        capex_forecast = self.forecasting_engine.forecast_capex(
            assumptions['capex_schedule']
        )
        
        # 7. Calculate synergies
        synergy_forecast = self.synergy_engine.calculate_synergies(
            synergy_models, forecast_years
        )
        
        # 8. Combine into cash flow forecast
        cash_flow_df = self._build_cash_flow_model(
            revenue_forecast,
            opex_forecast,
            capex_forecast,
            synergy_forecast,
            assumptions
        )
        
        # 9. Calculate valuation metrics
        metrics = self._calculate_metrics(cash_flow_df, assumptions)
        
        return {
            'production_forecast': production_forecast,
            'cash_flow_forecast': cash_flow_df,
            'synergy_forecast': synergy_forecast,
            'metrics': metrics
        }
    
    def _create_decline_curve(self, assumptions: Dict):
        """Create appropriate decline curve model."""
        decline_type = assumptions['decline_curve_type']
        decline_rate = assumptions['decline_rate']
        initial_rate = 1.0  # Will be scaled to match historical
        
        if decline_type == 'exponential':
            return ExponentialDecline(initial_rate, decline_rate)
        elif decline_type == 'hyperbolic':
            b_factor = assumptions.get('hyperbolic_b', 0.5)
            return HyperbolicDecline(initial_rate, decline_rate, b_factor)
        elif decline_type == 'harmonic':
            return HarmonicDecline(initial_rate, decline_rate)
        else:
            raise ValueError(f"Unknown decline type: {decline_type}")
    
    def _build_cash_flow_model(
        self,
        revenue_df: pd.DataFrame,
        opex_df: pd.DataFrame,
        capex_df: pd.DataFrame,
        synergy_df: pd.DataFrame,
        assumptions: Dict
    ) -> pd.DataFrame:
        """Combine forecasts into complete cash flow model."""
        df = revenue_df[['year', 'total_revenue']].copy()
        df = df.merge(opex_df, on='year')
        df = df.merge(capex_df, on='year')
        df = df.merge(synergy_df[['year', 'total_synergies']], on='year')
        
        # Calculate EBITDA
        df['ebitda'] = df['total_revenue'] - df['opex'] + df['total_synergies']
        
        # Calculate taxes (simplified)
        tax_rate = assumptions['tax_rate']
        df['taxes'] = df['ebitda'] * tax_rate
        
        # Calculate free cash flow
        df['free_cash_flow'] = df['ebitda'] - df['capex'] - df['taxes']
        
        # Add initial investment as year 0
        initial_investment = -assumptions['purchase_price']
        year_zero = pd.DataFrame({
            'year': [0],
            'total_revenue': [0],
            'opex': [0],
            'capex': [assumptions['purchase_price']],
            'total_synergies': [0],
            'ebitda': [0],
            'taxes': [0],
            'free_cash_flow': [initial_investment]
        })
        
        df = pd.concat([year_zero, df], ignore_index=True)
        
        return df
    
    def _calculate_metrics(self, cash_flow_df: pd.DataFrame, assumptions: Dict) -> Dict:
        """Calculate valuation metrics."""
        cash_flows = cash_flow_df['free_cash_flow'].tolist()
        discount_rate = assumptions['discount_rate']
        
        # Calculate NPV
        npv = self.irr_engine.calculate_npv(cash_flows, discount_rate)
        
        # Calculate IRR
        try:
            irr = self.irr_engine.calculate_irr(cash_flows)
        except ValueError:
            irr = None
        
        # Calculate payback period
        cumulative_cf = cash_flow_df['free_cash_flow'].cumsum()
        payback_years = (cumulative_cf >= 0).idxmax() if (cumulative_cf >= 0).any() else None
        
        # Calculate terminal value
        final_ebitda = cash_flow_df['ebitda'].iloc[-1]
        exit_multiple = assumptions['exit_multiple']
        terminal_value = final_ebitda * exit_multiple
        
        return {
            'npv': npv,
            'irr': irr,
            'payback_period': payback_years,
            'terminal_value': terminal_value
        }
```

---


## Security Architecture

### Authentication & Authorization

#### JWT Token Structure

```json
{
  "sub": "user_id_uuid",
  "email": "analyst@example.com",
  "role": "analyst",
  "exp": 1716551400,
  "iat": 1716465000
}
```

**Token Lifecycle:**
- Access token expiration: 24 hours
- Refresh token expiration: 30 days
- Token storage: HTTP-only cookies (preferred) or localStorage
- Token refresh: Automatic before expiration

#### Role-Based Access Control (RBAC)

| Role | Permissions |
|------|-------------|
| **Admin** | Full system access, user management, all CRUD operations |
| **Analyst** | Create/edit/delete own projects, run models, export data |
| **Viewer** | Read-only access to shared projects, view results |

**Permission Matrix:**

| Resource | Admin | Analyst | Viewer |
|----------|-------|---------|--------|
| Create Project | ✓ | ✓ | ✗ |
| Edit Own Project | ✓ | ✓ | ✗ |
| Edit Others' Project | ✓ | ✗ | ✗ |
| Delete Project | ✓ | Own only | ✗ |
| Upload Files | ✓ | ✓ | ✗ |
| Run Models | ✓ | ✓ | ✗ |
| View Results | ✓ | ✓ | ✓ |
| Export Data | ✓ | ✓ | ✗ |
| Manage Users | ✓ | ✗ | ✗ |
| View Audit Logs | ✓ | ✗ | ✗ |

### Input Validation & Sanitization

#### File Upload Security

```python
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def validate_file_upload(file):
    """Validate uploaded file for security."""
    # Check file extension
    if not allowed_file(file.filename):
        raise ValidationError("Invalid file type")
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size > MAX_FILE_SIZE:
        raise ValidationError("File too large")
    
    # Scan for malicious content
    if not scan_file_content(file):
        raise ValidationError("File contains malicious content")
    
    # Generate safe filename
    safe_filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{safe_filename}"
    
    return unique_filename
```

#### API Input Validation

```python
from pydantic import BaseModel, Field, validator

class AssumptionsSchema(BaseModel):
    """Pydantic schema for assumptions validation."""
    
    decline_rate: float = Field(ge=0, le=1, description="Decline rate between 0 and 1")
    discount_rate: float = Field(ge=0, le=0.5, description="Discount rate between 0 and 50%")
    tax_rate: float = Field(ge=0, le=1, description="Tax rate between 0 and 100%")
    purchase_price: float = Field(gt=0, description="Purchase price must be positive")
    forecast_years: int = Field(ge=1, le=50, description="Forecast years between 1 and 50")
    
    @validator('oil_price_forecast')
    def validate_price_forecast(cls, v):
        """Validate price forecast structure."""
        if not isinstance(v, list):
            raise ValueError("Price forecast must be a list")
        for item in v:
            if 'year' not in item or 'price' not in item:
                raise ValueError("Each price forecast must have year and price")
            if item['price'] < 0:
                raise ValueError("Price cannot be negative")
        return v
```

### SQL Injection Prevention

- Use SQLAlchemy ORM for all database queries
- Parameterized queries for raw SQL
- Input validation before database operations
- Principle of least privilege for database users

```python
# GOOD: Using ORM
project = db.query(Project).filter(Project.id == project_id).first()

# GOOD: Parameterized query
result = db.execute(
    text("SELECT * FROM projects WHERE user_id = :user_id"),
    {"user_id": user_id}
)

# BAD: String interpolation (NEVER DO THIS)
# query = f"SELECT * FROM projects WHERE user_id = '{user_id}'"
```

### XSS Prevention

- Sanitize all user inputs
- Escape output in templates
- Content Security Policy (CSP) headers
- HTTP-only cookies for tokens

```python
# FastAPI response headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/auth/login")
@limiter.limit("5/minute")  # 5 attempts per minute
async def login(request: Request, credentials: LoginSchema):
    # Login logic
    pass

@app.post("/api/v1/model/run")
@limiter.limit("10/hour")  # 10 model runs per hour
async def run_model(request: Request, data: ModelRunSchema):
    # Model execution logic
    pass
```

### Data Encryption

#### At Rest
- Database: PostgreSQL with encryption enabled
- File storage: AES-256 encryption
- Backups: Encrypted before storage

#### In Transit
- HTTPS/TLS 1.3 for all API communication
- Certificate pinning for mobile apps
- Secure WebSocket connections for real-time updates

### Audit Logging

```python
async def log_audit_event(
    user_id: str,
    action: str,
    resource_type: str,
    resource_id: str,
    details: dict,
    request: Request
):
    """Log audit event to database."""
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        timestamp=datetime.utcnow()
    )
    db.add(audit_log)
    await db.commit()
```

---

## Performance & Scalability

### Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Response Time (GET) | < 500ms | p95 |
| API Response Time (POST) | < 1s | p95 |
| Valuation Calculation | < 30s | 20-year forecast |
| Chart Rendering | < 2s | Client-side |
| File Upload Processing | < 10s | 50MB file |
| Concurrent Users | 50+ | No degradation |
| Database Query Time | < 100ms | p95 |

### Caching Strategy

#### Redis Cache Layers

```python
# Cache configuration
CACHE_TTL = {
    'project_list': 300,      # 5 minutes
    'project_detail': 600,    # 10 minutes
    'valuation_results': 3600, # 1 hour
    'chart_data': 1800,       # 30 minutes
}

# Cache decorator
from functools import wraps
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(key_prefix: str, ttl: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{args}:{kwargs}"
            
            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            redis_client.setex(
                cache_key,
                ttl,
                json.dumps(result)
            )
            
            return result
        return wrapper
    return decorator

# Usage
@cache_result('valuation_results', CACHE_TTL['valuation_results'])
async def get_valuation_results(project_id: str):
    # Expensive calculation
    return results
```

### Database Optimization

#### Indexing Strategy

```sql
-- Composite indexes for common queries
CREATE INDEX idx_production_data_project_date 
ON production_data(project_id, date DESC);

CREATE INDEX idx_valuation_outputs_scenario_year 
ON valuation_outputs(scenario_id, year);

CREATE INDEX idx_audit_logs_user_timestamp 
ON audit_logs(user_id, timestamp DESC);

-- Partial indexes for filtered queries
CREATE INDEX idx_projects_active 
ON projects(user_id, updated_at DESC) 
WHERE status = 'active';
```

#### Query Optimization

```python
# Use select_related for foreign keys
projects = db.query(Project)\
    .options(selectinload(Project.user))\
    .filter(Project.status == 'active')\
    .all()

# Pagination for large result sets
def get_projects_paginated(page: int, page_size: int):
    offset = (page - 1) * page_size
    projects = db.query(Project)\
        .offset(offset)\
        .limit(page_size)\
        .all()
    total = db.query(Project).count()
    return projects, total

# Batch inserts for bulk data
def bulk_insert_production_data(data_list: List[Dict]):
    db.bulk_insert_mappings(ProductionData, data_list)
    db.commit()
```

### Async Processing

#### Celery Task Queue

```python
from celery import Celery

celery_app = Celery('valuation_platform', broker='redis://localhost:6379/0')

@celery_app.task(bind=True)
def run_valuation_task(self, project_id: str, assumptions_id: str):
    """Background task for valuation calculation."""
    try:
        # Update task status
        self.update_state(state='PROCESSING', meta={'progress': 0})
        
        # Load data
        historical_data = load_historical_data(project_id)
        assumptions = load_assumptions(assumptions_id)
        synergy_models = load_synergy_models(assumptions_id)
        
        self.update_state(state='PROCESSING', meta={'progress': 25})
        
        # Run valuation
        valuation_service = ValuationService()
        results = valuation_service.run_valuation(
            historical_data, assumptions, synergy_models
        )
        
        self.update_state(state='PROCESSING', meta={'progress': 75})
        
        # Store results
        store_valuation_results(project_id, results)
        
        self.update_state(state='PROCESSING', meta={'progress': 100})
        
        return {'status': 'completed', 'results': results}
    
    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise
```

### Horizontal Scaling

#### Load Balancing

```nginx
# Nginx configuration
upstream backend {
    least_conn;
    server backend1:8000 weight=1;
    server backend2:8000 weight=1;
    server backend3:8000 weight=1;
}

server {
    listen 80;
    server_name api.valuation-platform.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

#### Database Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,          # Number of connections to maintain
    max_overflow=10,       # Additional connections when pool is full
    pool_timeout=30,       # Timeout for getting connection
    pool_recycle=3600,     # Recycle connections after 1 hour
)
```

---

## Testing Strategy

### Test Pyramid

```
                    ┌─────────────┐
                    │   E2E Tests │  (10%)
                    │   Playwright│
                    └─────────────┘
                  ┌───────────────────┐
                  │ Integration Tests │  (30%)
                  │   API Tests       │
                  └───────────────────┘
              ┌─────────────────────────────┐
              │      Unit Tests             │  (60%)
              │  Backend + Frontend         │
              └─────────────────────────────┘
```

### Backend Testing

#### Unit Tests (Pytest)

```python
# tests/unit/test_irr_engine.py
import pytest
from app.engines.irr_engine import IRREngine

class TestIRREngine:
    def setup_method(self):
        self.irr_engine = IRREngine()
    
    def test_calculate_irr_positive_returns(self):
        """Test IRR calculation with positive returns."""
        cash_flows = [-100000, 30000, 40000, 50000, 40000]
        irr = self.irr_engine.calculate_irr(cash_flows)
        
        assert irr > 0
        assert 0.15 < irr < 0.25  # Expected range
    
    def test_calculate_irr_negative_returns(self):
        """Test IRR calculation with negative returns."""
        cash_flows = [-100000, 10000, 10000, 10000, 10000]
        irr = self.irr_engine.calculate_irr(cash_flows)
        
        assert irr < 0.10  # Below 10%
    
    def test_calculate_npv(self):
        """Test NPV calculation."""
        cash_flows = [-100000, 30000, 40000, 50000, 40000]
        discount_rate = 0.12
        npv = self.irr_engine.calculate_npv(cash_flows, discount_rate)
        
        assert npv > 0
        assert isinstance(npv, float)
    
    def test_irr_convergence_failure(self):
        """Test IRR calculation with non-converging cash flows."""
        cash_flows = [100000, 100000, 100000]  # All positive
        
        with pytest.raises(ValueError, match="did not converge"):
            self.irr_engine.calculate_irr(cash_flows)

# tests/unit/test_decline_curves.py
import pytest
import numpy as np
from app.engines.decline_curves import ExponentialDecline, HyperbolicDecline

class TestDeclineCurves:
    def test_exponential_decline(self):
        """Test exponential decline curve."""
        curve = ExponentialDecline(initial_rate=1000, decline_rate=0.15)
        forecast = curve.forecast(periods=10)
        
        assert len(forecast) == 10
        assert forecast[0] == 1000  # Initial rate
        assert forecast[-1] < forecast[0]  # Declining
        assert all(forecast[i] > forecast[i+1] for i in range(len(forecast)-1))
    
    def test_hyperbolic_decline(self):
        """Test hyperbolic decline curve."""
        curve = HyperbolicDecline(
            initial_rate=1000,
            decline_rate=0.15,
            b_factor=0.5
        )
        forecast = curve.forecast(periods=10)
        
        assert len(forecast) == 10
        assert forecast[0] == 1000
        assert forecast[-1] < forecast[0]
```

#### Integration Tests

```python
# tests/integration/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestProjectAPI:
    def test_create_project(self, auth_headers):
        """Test project creation endpoint."""
        response = client.post(
            "/api/v1/projects",
            json={
                "name": "Test Project",
                "description": "Integration test project"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Project"
        assert "id" in data
    
    def test_get_projects(self, auth_headers):
        """Test project list endpoint."""
        response = client.get(
            "/api/v1/projects",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)
    
    def test_unauthorized_access(self):
        """Test that endpoints require authentication."""
        response = client.get("/api/v1/projects")
        assert response.status_code == 401

# Fixtures
@pytest.fixture
def auth_headers(test_user):
    """Generate auth headers for testing."""
    token = create_access_token(test_user.id)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_user(db_session):
    """Create test user."""
    user = User(
        email="test@example.com",
        hashed_password=hash_password("testpass"),
        full_name="Test User",
        role="analyst"
    )
    db_session.add(user)
    db_session.commit()
    return user
```

### Frontend Testing

#### Component Tests (Vitest + React Testing Library)

```typescript
// tests/components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Button } from '@/components/ui/Button';

describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click Me</Button>);
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });
  
  it('calls onClick handler when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click Me</Button>);
    
    fireEvent.click(screen.getByText('Click Me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
  
  it('is disabled when loading', () => {
    render(<Button loading>Click Me</Button>);
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
  });
});

// tests/components/WaterfallChart.test.tsx
import { render } from '@testing-library/react';
import { WaterfallChart } from '@/features/visualizations/components/WaterfallChart';

describe('WaterfallChart Component', () => {
  const mockData = {
    categories: ['Base', 'Synergy 1', 'Synergy 2', 'Final'],
    values: [10000000, 2000000, 1500000, 13500000],
    cumulative: [10000000, 12000000, 13500000, 13500000]
  };
  
  it('renders without crashing', () => {
    const { container } = render(<WaterfallChart data={mockData} />);
    expect(container.querySelector('canvas')).toBeInTheDocument();
  });
  
  it('displays correct number of bars', () => {
    const { container } = render(<WaterfallChart data={mockData} />);
    // Chart.js creates canvas element
    expect(container.querySelector('canvas')).toBeTruthy();
  });
});
```

#### E2E Tests (Playwright)

```typescript
// tests/e2e/project-workflow.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Project Workflow', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'testpass');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/projects');
  });
  
  test('create new project', async ({ page }) => {
    // Click create project button
    await page.click('button:has-text("New Project")');
    
    // Fill form
    await page.fill('input[name="name"]', 'E2E Test Project');
    await page.fill('textarea[name="description"]', 'Created by E2E test');
    await page.click('button:has-text("Create")');
    
    // Verify project created
    await expect(page.locator('text=E2E Test Project')).toBeVisible();
  });
  
  test('upload production data', async ({ page }) => {
    // Navigate to project
    await page.click('text=E2E Test Project');
    await page.click('text=Data');
    
    // Upload file
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles('tests/fixtures/production_data.csv');
    
    // Wait for processing
    await expect(page.locator('text=Processing')).toBeVisible();
    await expect(page.locator('text=Valid')).toBeVisible({ timeout: 10000 });
  });
  
  test('run valuation model', async ({ page }) => {
    // Navigate to modeling tab
    await page.click('text=E2E Test Project');
    await page.click('text=Modeling');
    
    // Fill assumptions
    await page.fill('input[name="decline_rate"]', '0.15');
    await page.fill('input[name="discount_rate"]', '0.12');
    await page.click('button:has-text("Run Model")');
    
    // Wait for results
    await expect(page.locator('text=Calculating')).toBeVisible();
    await expect(page.locator('text=NPV')).toBeVisible({ timeout: 30000 });
  });
});
```

### Test Coverage Goals

| Component | Target Coverage |
|-----------|----------------|
| Backend Services | 90% |
| Financial Engines | 95% |
| API Endpoints | 85% |
| Frontend Components | 80% |
| Overall | 85% |

---


## Deployment Strategy

### Container Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Compose Stack                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Nginx     │  │   Frontend   │  │   Backend    │      │
│  │  (Reverse    │  │   (React)    │  │  (FastAPI)   │      │
│  │   Proxy)     │  │              │  │              │      │
│  │  Port: 80    │  │  Port: 3000  │  │  Port: 8000  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                                     │              │
│         └─────────────────┬─────────────────┘              │
│                           │                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  PostgreSQL  │  │    Redis     │  │    Celery    │      │
│  │  (Database)  │  │   (Cache)    │  │   Worker     │      │
│  │  Port: 5432  │  │  Port: 6379  │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Docker Configuration

#### docker-compose.yml

```yaml
version: '3.8'

services:
  # Nginx Reverse Proxy
  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
      - frontend
    networks:
      - app-network
    restart: unless-stopped

  # Frontend Service
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      - VITE_API_URL=http://backend:8000
    networks:
      - app-network
    restart: unless-stopped

  # Backend Service
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/valuation_db
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
    depends_on:
      - postgres
      - redis
    networks:
      - app-network
    restart: unless-stopped
    volumes:
      - ./uploads:/app/uploads

  # Celery Worker
  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.tasks worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/valuation_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    networks:
      - app-network
    restart: unless-stopped

  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=valuation_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

#### Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p /app/uploads

# Run database migrations
CMD alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM nginx:1.25-alpine

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Environment Configuration

#### .env.example

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/valuation_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# File Upload
MAX_UPLOAD_SIZE=52428800  # 50MB
UPLOAD_DIR=/app/uploads

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Monitoring (optional)
SENTRY_DSN=your-sentry-dsn
```

### CI/CD Pipeline

#### GitHub Actions Workflow

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # Backend Tests
  backend-test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
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
          pip install pytest pytest-cov
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml

  # Frontend Tests
  frontend-test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run tests
        run: |
          cd frontend
          npm run test:coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./frontend/coverage/coverage-final.json

  # Build and Deploy
  deploy:
    needs: [backend-test, frontend-test]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push backend
        uses: docker/build-push-action@v4
        with:
          context: ./backend
          push: true
          tags: yourusername/valuation-backend:latest
      
      - name: Build and push frontend
        uses: docker/build-push-action@v4
        with:
          context: ./frontend
          push: true
          tags: yourusername/valuation-frontend:latest
      
      - name: Deploy to production
        run: |
          # Add deployment commands here
          # e.g., SSH to server and pull new images
          echo "Deploying to production..."
```

### Deployment Environments

#### Development
- Local Docker Compose
- Hot reload enabled
- Debug logging
- Mock data seeding

#### Staging
- Cloud-hosted (AWS/Azure/GCP)
- Production-like configuration
- Integration testing
- Performance testing

#### Production
- High availability setup
- Load balancing
- Auto-scaling
- Monitoring and alerting
- Automated backups

---

## Implementation Roadmap

### Phase 1: Project Scaffolding (Week 1)

**Backend Setup:**
- [ ] Initialize FastAPI project structure
- [ ] Configure PostgreSQL database
- [ ] Set up Alembic migrations
- [ ] Configure Redis
- [ ] Set up Celery
- [ ] Create base models (User, Project)
- [ ] Implement authentication (JWT)
- [ ] Create API documentation (Swagger)

**Frontend Setup:**
- [ ] Initialize React + Vite project
- [ ] Configure TailwindCSS
- [ ] Set up React Router
- [ ] Configure Zustand stores
- [ ] Set up React Query
- [ ] Create base layout components
- [ ] Implement authentication flow

**DevOps:**
- [ ] Create Dockerfiles
- [ ] Create docker-compose.yml
- [ ] Set up GitHub repository
- [ ] Configure CI/CD pipeline

**Deliverables:**
- Working authentication system
- Basic project CRUD operations
- Containerized development environment

---

### Phase 2: Data Ingestion & ETL (Week 2)

**Backend:**
- [ ] Implement file upload endpoints
- [ ] Create ETL service for CSV/XLSX parsing
- [ ] Implement data validation logic
- [ ] Create production_data and financial_data models
- [ ] Implement data quality scoring
- [ ] Create background tasks for file processing

**Frontend:**
- [ ] Build file upload component (drag & drop)
- [ ] Create validation status display
- [ ] Build data quality dashboard
- [ ] Implement historical KPI cards
- [ ] Create data preview tables

**Testing:**
- [ ] Unit tests for ETL pipeline
- [ ] Integration tests for upload endpoints
- [ ] Test with sample CSV/XLSX files

**Deliverables:**
- Functional file upload system
- Data validation and quality scoring
- Historical data visualization

---

### Phase 3: Financial Calculation Engine (Week 3-4)

**Backend:**
- [ ] Implement decline curve models (exponential, hyperbolic, harmonic)
- [ ] Create forecasting engine
- [ ] Implement synergy engine
- [ ] Create IRR calculation engine
- [ ] Implement NPV calculation
- [ ] Create valuation service orchestrator
- [ ] Implement scenario engine
- [ ] Create sensitivity analysis engine

**Testing:**
- [ ] Unit tests for all calculation engines
- [ ] Validate financial formulas against benchmarks
- [ ] Test edge cases (negative cash flows, etc.)
- [ ] Performance testing for large datasets

**Deliverables:**
- Complete financial calculation engine
- Validated against industry standards
- Performance benchmarks met

---

### Phase 4: Modeling Interface (Week 5)

**Backend:**
- [ ] Create assumptions model and endpoints
- [ ] Create synergy_models endpoints
- [ ] Implement model run endpoint
- [ ] Create task status endpoints

**Frontend:**
- [ ] Build assumptions form (production, cost, synergy, deal)
- [ ] Create synergy configuration interface
- [ ] Implement model run trigger
- [ ] Build calculation progress indicator
- [ ] Create results summary display

**Testing:**
- [ ] Integration tests for modeling workflow
- [ ] E2E tests for complete modeling flow

**Deliverables:**
- Complete modeling interface
- Ability to configure and run valuations

---

### Phase 5: Scenario Analysis (Week 6)

**Backend:**
- [ ] Create scenarios model and endpoints
- [ ] Implement scenario comparison logic
- [ ] Create sensitivity analysis endpoints
- [ ] Optimize parallel scenario calculations

**Frontend:**
- [ ] Build scenario manager component
- [ ] Create scenario comparison table
- [ ] Implement sensitivity table component
- [ ] Build scenario toggle controls

**Testing:**
- [ ] Test multi-scenario calculations
- [ ] Validate sensitivity analysis accuracy

**Deliverables:**
- Bull/Base/Bear scenario analysis
- Sensitivity tables
- Scenario comparison views

---

### Phase 6: Visualization Suite (Week 7-8)

**Frontend:**
- [ ] Implement waterfall chart
- [ ] Create IRR projection chart
- [ ] Build cash flow forecast chart
- [ ] Implement production decline chart
- [ ] Create EBITDA trend chart
- [ ] Build synergy realization timeline
- [ ] Implement debt paydown chart
- [ ] Add chart export functionality

**Backend:**
- [ ] Create chart data endpoints
- [ ] Optimize data aggregation for charts
- [ ] Implement caching for chart data

**Testing:**
- [ ] Visual regression testing
- [ ] Performance testing for chart rendering
- [ ] Test chart interactions

**Deliverables:**
- Complete visualization suite
- Interactive, professional-grade charts
- Export functionality

---

### Phase 7: Data Export & Reporting (Week 9)

**Backend:**
- [ ] Implement Excel export service
- [ ] Create PDF report generator (optional)
- [ ] Implement export endpoints
- [ ] Add export to audit logs

**Frontend:**
- [ ] Build export configuration interface
- [ ] Add export buttons to relevant pages
- [ ] Implement download progress indicators

**Testing:**
- [ ] Test Excel file generation
- [ ] Validate exported data accuracy

**Deliverables:**
- Excel export functionality
- Comprehensive project reports

---

### Phase 8: Polish & Optimization (Week 10)

**Backend:**
- [ ] Implement caching strategy
- [ ] Optimize database queries
- [ ] Add database indexes
- [ ] Implement rate limiting
- [ ] Add comprehensive error handling

**Frontend:**
- [ ] Implement dark/light mode
- [ ] Add loading states and skeletons
- [ ] Implement error boundaries
- [ ] Add animations and transitions
- [ ] Optimize bundle size
- [ ] Implement responsive design

**Testing:**
- [ ] Performance testing
- [ ] Load testing
- [ ] Accessibility testing

**Deliverables:**
- Optimized performance
- Polished user experience
- Accessibility compliance

---

### Phase 9: Testing & Quality Assurance (Week 11)

**Backend:**
- [ ] Achieve 90% test coverage
- [ ] Fix all critical bugs
- [ ] Security audit
- [ ] Performance benchmarking

**Frontend:**
- [ ] Achieve 80% test coverage
- [ ] Cross-browser testing
- [ ] Mobile responsiveness testing
- [ ] E2E test suite completion

**Documentation:**
- [ ] API documentation
- [ ] User guide
- [ ] Developer documentation
- [ ] Deployment guide

**Deliverables:**
- Production-ready application
- Comprehensive test coverage
- Complete documentation

---

### Phase 10: Deployment & Launch (Week 12)

**Infrastructure:**
- [ ] Set up production environment
- [ ] Configure SSL certificates
- [ ] Set up monitoring (Sentry, DataDog, etc.)
- [ ] Configure automated backups
- [ ] Set up log aggregation

**Deployment:**
- [ ] Deploy to production
- [ ] Run smoke tests
- [ ] Monitor performance
- [ ] Set up alerts

**Launch:**
- [ ] User training
- [ ] Soft launch with beta users
- [ ] Gather feedback
- [ ] Full launch

**Deliverables:**
- Live production system
- Monitoring and alerting
- User documentation

---

## Risk Considerations

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| IRR calculation convergence failures | High | Medium | Implement multiple algorithms, fallback methods |
| Large file processing timeouts | Medium | High | Async processing, chunking, progress indicators |
| Database performance degradation | High | Medium | Indexing, query optimization, caching |
| Chart rendering performance | Medium | Medium | Data aggregation, lazy loading, virtualization |
| Security vulnerabilities | High | Low | Security audit, penetration testing, regular updates |

### Business Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Inaccurate financial calculations | Critical | Low | Extensive testing, validation against benchmarks |
| Data loss | Critical | Low | Automated backups, redundancy, disaster recovery |
| Regulatory compliance issues | High | Low | Audit logging, data encryption, compliance review |
| User adoption challenges | Medium | Medium | User training, intuitive UX, documentation |
| Scalability limitations | Medium | Low | Horizontal scaling, load testing, optimization |

---

## Future Extensibility

### Phase 2 Features (Post-Launch)

**Advanced Analytics:**
- Monte Carlo simulation for risk analysis
- Machine learning for production forecasting
- Automated decline curve fitting
- Real-time commodity price integration

**Collaboration Features:**
- Multi-user project collaboration
- Comments and annotations
- Version control for assumptions
- Approval workflows

**Integration Capabilities:**
- API for third-party integrations
- Excel add-in for direct data import
- Integration with accounting systems
- Integration with reservoir engineering software

**Enhanced Reporting:**
- Custom report templates
- Automated report scheduling
- Interactive dashboards
- Executive summary generation

**Mobile Application:**
- iOS and Android apps
- Offline mode
- Push notifications
- Mobile-optimized charts

### Architectural Extensibility

**Microservices Migration:**
- Split calculation engine into separate service
- Separate file processing service
- Independent scaling of components

**Multi-Tenancy:**
- Organization-level accounts
- Team management
- Resource quotas
- Usage analytics

**Advanced Security:**
- Two-factor authentication
- Single sign-on (SSO)
- Advanced audit logging
- Data encryption at rest

---

## Conclusion

This architecture document provides a comprehensive blueprint for building an institutional-grade Oil & Gas M&A valuation platform. The design emphasizes:

- **Scalability**: Horizontal scaling, caching, async processing
- **Security**: JWT authentication, RBAC, input validation, audit logging
- **Performance**: Optimized queries, caching, parallel processing
- **Maintainability**: Clean architecture, modular design, comprehensive testing
- **Extensibility**: Plugin architecture, API-first design, microservices-ready

The phased implementation approach ensures steady progress with regular deliverables, allowing for iterative feedback and adjustments. The platform will provide energy sector professionals with powerful tools for evaluating M&A opportunities with institutional-grade rigor.

---

**Document Version:** 1.0  
**Last Updated:** May 23, 2026  
**Next Review:** June 23, 2026
