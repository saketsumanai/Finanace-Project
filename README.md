# 🛢️ Oil & Gas M&A Valuation Platform

A comprehensive, AI-powered platform for valuing oil and gas mergers & acquisitions. Built with FastAPI, React, and advanced financial modeling engines.

![Platform Status](https://img.shields.io/badge/status-production--ready-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![React](https://img.shields.io/badge/react-18.2-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.110-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🌟 Features

### 💼 Core Valuation Features
- **Project Management** - Create and manage multiple M&A projects
- **Data Upload** - Import production and financial data (CSV/XLSX)
- **Financial Modeling** - Configure assumptions, decline curves, and forecasts
- **Valuation Engine** - Calculate NPV, IRR, payback period, and ROIC
- **Scenario Analysis** - Bull/Base/Bear scenarios with sensitivity analysis
- **Synergy Modeling** - Track operational, procurement, and workforce synergies

### 🤖 AI-Powered Intelligence
- **AI Chat Assistant** - Powered by Google Gemini 2.5 Flash
- **Real-Time Market Data** - Live oil/gas prices via Alpha Vantage API
- **Web Scraping** - Analyze company websites and gather intelligence
- **Research Assistant** - Multi-source research and analysis
- **Company Analysis** - Comprehensive M&A target evaluation
- **Market Intelligence** - Economic indicators and commodity trends

### 📊 Analytics & Visualization
- **Production Trends** - Interactive line charts with decline curves
- **Revenue & Cost Analysis** - Bar charts with OPEX/CAPEX breakdown
- **File Distribution** - Pie charts for data quality metrics
- **Data Quality Indicators** - Real-time completeness scoring
- **Custom Dashboards** - Project-specific analytics

### 🔐 Security & Authentication
- **Firebase Google OAuth** - Secure social login
- **Email/Password Auth** - Traditional authentication
- **JWT Tokens** - Secure API access
- **Role-Based Access** - User permission management

## 🏗️ Architecture

### Backend Stack
- **Framework**: FastAPI 0.110
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Task Queue**: Celery
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **AI**: Google Gemini API
- **Market Data**: Alpha Vantage API

### Frontend Stack
- **Framework**: React 18.2
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **State Management**: Zustand
- **Charts**: Chart.js
- **HTTP Client**: Axios
- **Routing**: React Router

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Web Server**: Uvicorn
- **Reverse Proxy**: Nginx (production)
- **CI/CD**: GitHub Actions (optional)

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- 4GB RAM minimum
- 10GB disk space

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/oil-gas-valuation-platform.git
cd oil-gas-valuation-platform
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

3. **Start the application**
```bash
docker-compose up -d
```

4. **Access the platform**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

### First-Time Setup

1. **Create an account**
   - Go to http://localhost:5173/register
   - Or use Google Sign-In

2. **Create your first project**
   - Navigate to Projects
   - Click "Create Project"
   - Fill in project details

3. **Upload data** (optional)
   - Upload production data CSV
   - Upload financial data CSV

4. **Configure assumptions**
   - Set decline curves
   - Configure price forecasts
   - Define cost parameters

5. **Run valuation**
   - Execute valuation model
   - View results and analytics

## 📖 Documentation

### API Documentation
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

### User Guides
- [AI Chat User Guide](./AI_CHAT_USER_GUIDE.md)
- [System Guide](./COMPLETE_SYSTEM_GUIDE.md)
- [Architecture](./docs/ARCHITECTURE_AND_EXECUTION_PLAN.md)

### API Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login with email/password
- `POST /api/v1/auth/google` - Google OAuth login
- `POST /api/v1/auth/firebase-login` - Firebase authentication

#### Projects
- `GET /api/v1/projects` - List all projects
- `POST /api/v1/projects` - Create new project
- `GET /api/v1/projects/{id}` - Get project details
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

#### File Upload
- `POST /api/v1/upload/production` - Upload production data
- `POST /api/v1/upload/financials` - Upload financial data
- `GET /api/v1/upload/files/{project_id}` - List project files

#### Financial Modeling
- `POST /api/v1/modeling/assumptions` - Create assumptions
- `GET /api/v1/modeling/assumptions/{project_id}` - Get assumptions
- `POST /api/v1/modeling/synergies` - Create synergy model
- `POST /api/v1/modeling/scenarios` - Create scenario
- `POST /api/v1/modeling/run` - Run valuation

#### AI Assistant (15 endpoints)
- `POST /api/v1/ai/chat` - General AI chat
- `POST /api/v1/ai/analyze-csv` - Analyze CSV file
- `POST /api/v1/ai/analyze-project` - Analyze project
- `POST /api/v1/ai/suggest-assumptions` - Get assumption recommendations
- `POST /api/v1/ai/identify-synergies` - Identify synergies
- `POST /api/v1/ai/assess-risks` - Risk assessment
- `POST /api/v1/ai/generate-report` - Generate report
- `POST /api/v1/ai/market-intelligence` - Market data analysis
- `POST /api/v1/ai/comparable-companies` - Comparable company analysis
- `POST /api/v1/ai/analyze-anything` - General analysis
- `POST /api/v1/ai/scrape-url` - Scrape and analyze URL
- `POST /api/v1/ai/scrape-multiple-urls` - Compare multiple URLs
- `POST /api/v1/ai/research-topic` - Research any topic
- `POST /api/v1/ai/analyze-company-website` - Company website analysis

## 🔧 Configuration

### Required API Keys

1. **Gemini API Key** (Required for AI features)
   - Get from: https://makersuite.google.com/app/apikey
   - Add to `.env`: `GEMINI_API_KEY=your-key-here`

2. **Alpha Vantage API Key** (Required for market data)
   - Get from: https://www.alphavantage.co/support/#api-key
   - Add to `.env`: `ALPHA_VANTAGE_API_KEY=your-key-here`

3. **Firebase Configuration** (Required for Google OAuth)
   - Create project: https://console.firebase.google.com/
   - Enable Google Authentication
   - Add credentials to `.env`

### Environment Variables

See [.env.example](./.env.example) for all configuration options.

## 🧪 Testing

### Run Backend Tests
```bash
docker-compose exec backend pytest
```

### Run Frontend Tests
```bash
docker-compose exec frontend npm test
```

### Run All Tests
```bash
docker-compose exec backend pytest --cov
docker-compose exec frontend npm run test:coverage
```

## 📦 Deployment

### Production Deployment

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed instructions.

#### Quick Deploy Options

**Option 1: Docker Compose (VPS/Cloud)**
```bash
# Set production environment
export ENVIRONMENT=production

# Build and deploy
docker-compose -f docker-compose.prod.yml up -d
```

**Option 2: Kubernetes**
```bash
kubectl apply -f k8s/
```

**Option 3: Cloud Platforms**
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform
- Heroku

### Environment-Specific Configs

- **Development**: `docker-compose.yml`
- **Production**: `docker-compose.prod.yml`
- **Testing**: `docker-compose.test.yml`

## 🛠️ Development

### Project Structure
```
.
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration
│   │   ├── engines/        # Calculation engines
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── tasks/          # Celery tasks
│   ├── alembic/            # Database migrations
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── store/          # State management
│   │   └── utils/          # Utilities
│   ├── Dockerfile
│   └── package.json
├── docs/                   # Documentation
├── docker-compose.yml      # Development setup
└── README.md
```

### Adding New Features

1. **Backend**: Add endpoint in `backend/app/api/v1/`
2. **Frontend**: Add page in `frontend/src/pages/`
3. **Database**: Create migration with `alembic revision`
4. **Tests**: Add tests in respective test directories

### Code Style

- **Backend**: Black, Flake8, MyPy
- **Frontend**: ESLint, Prettier
- **Commits**: Conventional Commits

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** - Modern Python web framework
- **React** - UI library
- **Google Gemini** - AI capabilities
- **Alpha Vantage** - Market data
- **Chart.js** - Data visualization
- **TailwindCSS** - Styling

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/oil-gas-valuation-platform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/oil-gas-valuation-platform/discussions)
- **Email**: support@yourcompany.com

## 🗺️ Roadmap

### Phase 1: Core Platform ✅
- [x] Authentication system
- [x] Project management
- [x] File upload & ETL
- [x] Financial modeling
- [x] Valuation engine
- [x] Basic analytics

### Phase 2: AI Integration ✅
- [x] Gemini AI chat
- [x] Market data integration
- [x] Web scraping
- [x] Research assistant

### Phase 3: Advanced Features 🚧
- [ ] Scenario comparison
- [ ] Sensitivity analysis
- [ ] Advanced visualizations
- [ ] Excel export
- [ ] Audit logging

### Phase 4: Enterprise 📋
- [ ] Multi-tenancy
- [ ] Advanced permissions
- [ ] API rate limiting
- [ ] Audit trails
- [ ] SSO integration

## 📊 System Status

- **Backend**: ✅ Running
- **Frontend**: ✅ Running
- **Database**: ✅ Healthy
- **Redis**: ✅ Healthy
- **AI Services**: ✅ Operational
- **Market Data**: ✅ Connected

---

**Built with ❤️ for the Oil & Gas M&A community**
