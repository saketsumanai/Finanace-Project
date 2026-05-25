# Design Document

## Overview

This document provides the technical design for the Oil & Gas M&A Valuation Platform based on the requirements specified in requirements.md. The design follows clean architecture principles with clear separation between presentation, business logic, and data layers.

## System Architecture

### High-Level Architecture

The system follows a three-tier architecture:

```
┌─────────────────────────────────────────┐
│      Presentation Layer (React)          │
│  - UI Components                         │
│  - State Management (Zustand)            │
│  - API Client (Axios + React Query)      │
└─────────────────────────────────────────┘
                  ↕ REST API
┌─────────────────────────────────────────┐
│    Application Layer (FastAPI)           │
│  - API Routes                            │
│  - Business Services                     │
│  - Financial Calculation Engines         │
│  - Background Workers (Celery)           │
└─────────────────────────────────────────┘
                  ↕ ORM
┌─────────────────────────────────────────┐
│      Data Layer (PostgreSQL)             │
│  - Relational Database                   │
│  - Redis Cache                           │
└─────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- FastAPI 0.110+ (Web framework)
- SQLAlchemy 2.0+ (ORM)
- PostgreSQL 15+ (Database)
- Pandas 2.2+ (Data processing)
- NumPy 1.26+ (Numerical computing)
- SciPy 1.12+ (Scientific computing)
- Celery 5.3+ (Task queue)
- Redis 7.2+ (Cache & message broker)

**Frontend:**
- React 18.2+ (UI library)
- Vite 5.1+ (Build tool)
- TailwindCSS 3.4+ (Styling)
- Chart.js 4.4+ (Charting)
- Zustand 4.5+ (State management)
- React Query 5.28+ (Server state)
- Axios 1.6+ (HTTP client)

**DevOps:**
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Nginx (Reverse proxy)

## Component Design

### Backend Components

#### 1. API Layer

**Purpose:** Handle HTTP requests, validate inputs, serialize responses

**Structure:**
```
app/api/v1/
├── auth.py          # Authentication endpoints
├── projects.py      # Project management
├── upload.py        # File upload
├── modeling.py      # Modeling configuration
├── scenarios.py     # Scenario management
└── charts.py        # Visualization data
```

**Key Endpoints:**
- `POST /api/v1/auth/login` - User authentication
- `GET /api/v1/projects` - List projects
- `POST /api/v1/upload/production` - Upload production data
- `POST /api/v1/model/run` - Execute valuation
- `GET /api/v1/charts/waterfall/{scenario_id}` - Get chart data

#### 2. Service Layer

**Purpose:** Implement business logic, orchestrate operations

**Components:**
- `AuthService`: User authentication and authorization
- `FileService`: File upload and storage management
- `ETLService`: Data extraction, transformation, loading
- `ProjectService`: Project lifecycle management
- `ExportService`: Data export to Excel/PDF

#### 3. Financial Calculation Engines

**Purpose:** Perform valuation calculations

**Modules:**

**decline_curves.py**
```python
class DeclineCurve(ABC):
    @abstractmethod
    def forecast(self, periods: int) -> np.ndarray:
        pass

class ExponentialDecline(DeclineCurve):
    # Q(t) = Q_i * e^(-D * t)
    pass

class HyperbolicDecline(DeclineCurve):
    # Q(t) = Q_i / (1 + b * D_i * t)^(1/b)
    pass
```

**forecasting_engine.py**
```python
class ForecastingEngine:
    def forecast_production(self, historical_data, decline_curve)
    def forecast_revenue(self, production_forecast, price_forecast)
    def forecast_opex(self, production_forecast, base_opex, inflation_rate)
    def forecast_capex(self, capex_schedule)
```

**synergy_engine.py**
```python
class SynergyEngine:
    def calculate_synergies(self, synergy_models, forecast_years)
    def apply_realization_schedule(self, target_value, schedule)
```

**irr_engine.py**
```python
class IRREngine:
    def calculate_irr(self, cash_flows) -> float
    def calculate_npv(self, cash_flows, discount_rate) -> float
    def _npv_function(self, rate, cash_flows)
    def _npv_derivative(self, rate, cash_flows)
```

**valuation_service.py**
```python
class ValuationService:
    def run_valuation(self, historical_data, assumptions, synergy_models)
    def _create_decline_curve(self, assumptions)
    def _build_cash_flow_model(self, revenue, opex, capex, synergies, assumptions)
    def _calculate_metrics(self, cash_flow_df, assumptions)
```

#### 4. Repository Layer

**Purpose:** Abstract database operations

**Pattern:**
```python
class BaseRepository:
    def __init__(self, db_session):
        self.db = db_session
    
    def get_by_id(self, id)
    def get_all(self, filters)
    def create(self, data)
    def update(self, id, data)
    def delete(self, id)

class ProjectRepository(BaseRepository):
    def get_by_user(self, user_id)
    def get_with_scenarios(self, project_id)
```

### Frontend Components

#### 1. Feature Modules

**Structure:**
```
src/features/
├── auth/
│   ├── components/
│   ├── hooks/
│   └── services/
├── projects/
│   ├── components/
│   ├── hooks/
│   └── services/
├── upload/
├── modeling/
├── scenarios/
└── visualizations/
```

#### 2. Shared Components

**UI Components:**
- `Button` - Reusable button with variants
- `Card` - Container component
- `Modal` - Dialog component
- `Input` - Form input with validation
- `Table` - Data table with sorting/filtering
- `Spinner` - Loading indicator

**Chart Components:**
- `WaterfallChart` - Value creation waterfall
- `IRRProjectionChart` - Multi-scenario IRR
- `CashFlowChart` - Stacked cash flow components
- `ProductionDeclineChart` - Production forecast
- `EBITDAChart` - EBITDA trend
- `SynergyTimelineChart` - Synergy realization
- `DebtPaydownChart` - Debt schedule

#### 3. State Management

**Zustand Stores:**

```typescript
// authStore.ts
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

// projectStore.ts
interface ProjectState {
  currentProject: Project | null;
  projects: Project[];
  setCurrentProject: (project: Project) => void;
}

// themeStore.ts
interface ThemeState {
  mode: 'light' | 'dark';
  toggleTheme: () => void;
}
```

**React Query Hooks:**

```typescript
// useProjects.ts
export const useProjects = () => {
  return useQuery({
    queryKey: ['projects'],
    queryFn: fetchProjects,
  });
};

// useValuationResults.ts
export const useValuationResults = (projectId: string) => {
  return useQuery({
    queryKey: ['valuation', projectId],
    queryFn: () => fetchValuationResults(projectId),
  });
};
```

## Data Models

### Database Schema

**users**
- id (UUID, PK)
- email (VARCHAR, UNIQUE)
- hashed_password (VARCHAR)
- full_name (VARCHAR)
- role (VARCHAR)
- is_active (BOOLEAN)
- created_at (TIMESTAMP)

**projects**
- id (UUID, PK)
- user_id (UUID, FK → users)
- name (VARCHAR)
- description (TEXT)
- status (VARCHAR)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

**uploaded_files**
- id (UUID, PK)
- project_id (UUID, FK → projects)
- filename (VARCHAR)
- file_type (VARCHAR)
- file_size (INTEGER)
- file_path (VARCHAR)
- validation_status (VARCHAR)
- quality_score (DECIMAL)
- upload_date (TIMESTAMP)

**production_data**
- id (UUID, PK)
- project_id (UUID, FK → projects)
- date (DATE)
- oil_production (DECIMAL)
- gas_production (DECIMAL)
- oil_price (DECIMAL)
- gas_price (DECIMAL)

**financial_data**
- id (UUID, PK)
- project_id (UUID, FK → projects)
- date (DATE)
- revenue (DECIMAL)
- opex (DECIMAL)
- capex (DECIMAL)
- ebitda (DECIMAL)

**assumptions**
- id (UUID, PK)
- project_id (UUID, FK → projects)
- version (INTEGER)
- name (VARCHAR)
- decline_curve_type (VARCHAR)
- decline_rate (DECIMAL)
- hyperbolic_b (DECIMAL)
- oil_price_forecast (JSONB)
- gas_price_forecast (JSONB)
- opex_inflation_rate (DECIMAL)
- capex_schedule (JSONB)
- purchase_price (DECIMAL)
- discount_rate (DECIMAL)
- tax_rate (DECIMAL)
- exit_multiple (DECIMAL)
- forecast_years (INTEGER)

**synergy_models**
- id (UUID, PK)
- assumptions_id (UUID, FK → assumptions)
- category (VARCHAR)
- description (TEXT)
- target_value (DECIMAL)
- realization_schedule (JSONB)

**scenarios**
- id (UUID, PK)
- project_id (UUID, FK → projects)
- assumptions_id (UUID, FK → assumptions)
- name (VARCHAR)
- scenario_type (VARCHAR)
- description (TEXT)

**valuation_outputs**
- id (UUID, PK)
- scenario_id (UUID, FK → scenarios)
- year (INTEGER)
- oil_production (DECIMAL)
- gas_production (DECIMAL)
- revenue (DECIMAL)
- opex (DECIMAL)
- capex (DECIMAL)
- ebitda (DECIMAL)
- free_cash_flow (DECIMAL)
- synergy_value (DECIMAL)
- debt_balance (DECIMAL)
- npv (DECIMAL)
- irr (DECIMAL)
- payback_period (DECIMAL)
- roic (DECIMAL)

**audit_logs**
- id (UUID, PK)
- user_id (UUID, FK → users)
- action (VARCHAR)
- resource_type (VARCHAR)
- resource_id (UUID)
- details (JSONB)
- ip_address (INET)
- timestamp (TIMESTAMP)

## API Design

### Request/Response Schemas

**Authentication:**
```json
POST /api/v1/auth/login
Request: {
  "email": "string",
  "password": "string"
}
Response: {
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "string",
    "full_name": "string",
    "role": "string"
  }
}
```

**Project Creation:**
```json
POST /api/v1/projects
Request: {
  "name": "string",
  "description": "string"
}
Response: {
  "id": "uuid",
  "name": "string",
  "description": "string",
  "status": "draft",
  "created_at": "timestamp"
}
```

**Model Execution:**
```json
POST /api/v1/model/run
Request: {
  "project_id": "uuid",
  "assumptions_id": "uuid",
  "scenarios": ["bull", "base", "bear"]
}
Response: {
  "task_id": "uuid",
  "status": "processing"
}
```

## Security Design

### Authentication Flow

1. User submits credentials
2. Backend validates credentials
3. Generate JWT token with user claims
4. Return token to client
5. Client stores token (HTTP-only cookie or localStorage)
6. Client includes token in Authorization header for subsequent requests
7. Backend validates token on each request

### Authorization

**Role-Based Access Control:**
- Admin: Full access
- Analyst: Create/edit own projects
- Viewer: Read-only access

**Implementation:**
```python
def require_role(required_role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = get_current_user()
            if current_user.role != required_role:
                raise HTTPException(status_code=403)
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

### Input Validation

- Pydantic schemas for all API inputs
- File upload validation (type, size, content)
- SQL injection prevention (ORM, parameterized queries)
- XSS prevention (output escaping)

## Performance Design

### Caching Strategy

**Redis Cache Layers:**
- Project list: 5 minutes TTL
- Project details: 10 minutes TTL
- Valuation results: 1 hour TTL
- Chart data: 30 minutes TTL

**Cache Invalidation:**
- On data update: Invalidate related caches
- On model run: Invalidate valuation and chart caches

### Database Optimization

**Indexes:**
```sql
CREATE INDEX idx_production_data_project_date ON production_data(project_id, date);
CREATE INDEX idx_valuation_outputs_scenario_year ON valuation_outputs(scenario_id, year);
CREATE INDEX idx_projects_user_status ON projects(user_id, status);
```

**Query Optimization:**
- Use select_related for foreign keys
- Implement pagination for large result sets
- Batch inserts for bulk data

### Async Processing

**Celery Tasks:**
- File processing (ETL)
- Valuation calculations
- Report generation
- Email notifications

**Task Flow:**
1. API receives request
2. Create Celery task
3. Return task ID immediately (202 Accepted)
4. Client polls task status
5. Task completes, results stored in database
6. Client retrieves results

## Testing Design

### Test Strategy

**Unit Tests (60%):**
- Financial calculation engines
- Business logic services
- Utility functions

**Integration Tests (30%):**
- API endpoints
- Database operations
- External service integrations

**E2E Tests (10%):**
- Complete user workflows
- Critical business paths

### Test Coverage Goals

- Backend services: 90%
- Financial engines: 95%
- API endpoints: 85%
- Frontend components: 80%

## Deployment Design

### Container Architecture

**Services:**
- Nginx (reverse proxy)
- Frontend (React app)
- Backend (FastAPI)
- Celery Worker
- PostgreSQL
- Redis

**Docker Compose:**
- Development: Hot reload, debug logging
- Production: Optimized builds, health checks

### CI/CD Pipeline

**Stages:**
1. Lint & Format Check
2. Unit Tests
3. Integration Tests
4. Build Docker Images
5. Push to Registry
6. Deploy to Environment
7. Smoke Tests

## Monitoring & Observability

### Logging

**Log Levels:**
- ERROR: Application errors
- WARNING: Potential issues
- INFO: Important events
- DEBUG: Detailed information

**Log Aggregation:**
- Centralized logging (ELK stack or similar)
- Structured JSON logs
- Request ID tracking

### Metrics

**Application Metrics:**
- Request rate
- Response time (p50, p95, p99)
- Error rate
- Active users

**Business Metrics:**
- Projects created
- Models run
- Files uploaded
- Export requests

### Alerting

**Critical Alerts:**
- Service down
- Database connection failures
- High error rate (>5%)
- Slow response times (>2s p95)

**Warning Alerts:**
- High memory usage (>80%)
- High CPU usage (>80%)
- Disk space low (<20%)
- Cache hit rate low (<70%)

## Conclusion

This design provides a solid foundation for building a scalable, maintainable, and performant Oil & Gas M&A valuation platform. The architecture follows industry best practices with clear separation of concerns, comprehensive testing, and robust security measures.
