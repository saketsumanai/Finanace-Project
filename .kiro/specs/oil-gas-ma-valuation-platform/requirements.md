# Requirements Document

## Introduction

This document specifies the requirements for a production-quality Oil & Gas M&A valuation platform. The system enables investment banks, private equity firms, and energy corporates to evaluate upstream oil and gas acquisitions through data ingestion, financial modeling, synergy analysis, cash flow forecasting, and valuation metrics computation. The platform provides institutional-grade analytics comparable to tools used by Goldman Sachs, Evercore, JPMorgan Energy, McKinsey Energy Practice, and Enverus.

## Glossary

- **Platform**: The Oil & Gas M&A valuation web application system
- **Asset_Intake_Module**: The subsystem responsible for uploading and processing historical data files
- **ETL_Pipeline**: Extract, Transform, Load pipeline for data validation and normalization
- **Financial_Engine**: The calculation subsystem that computes valuation metrics and forecasts
- **Visualization_Suite**: The charting and dashboard subsystem
- **Authentication_Service**: The user authentication and authorization subsystem
- **Database**: PostgreSQL database storing all application data
- **API**: FastAPI REST interface for backend operations
- **Frontend**: React-based user interface
- **User**: An authenticated person using the platform
- **Project**: A collection of data, assumptions, and scenarios for a specific M&A analysis
- **Scenario**: A set of assumptions (Bull/Base/Bear) used for valuation modeling
- **Synergy**: Cost savings or revenue enhancements from combining operations
- **DCF**: Discounted Cash Flow valuation methodology
- **IRR**: Internal Rate of Return metric
- **NPV**: Net Present Value metric
- **EBITDA**: Earnings Before Interest, Taxes, Depreciation, and Amortization
- **EBITDAX**: EBITDA before exploration expenses
- **CAPEX**: Capital Expenditures
- **OPEX**: Operating Expenses
- **Decline_Curve**: Mathematical model of production decline over time
- **Waterfall_Chart**: Visualization showing sequential value contributions
- **Audit_Log**: Record of all system actions for compliance tracking

## Requirements

### Requirement 1: User Authentication and Authorization

**User Story:** As a platform administrator, I want secure user authentication and role-based access control, so that only authorized users can access sensitive financial data.

#### Acceptance Criteria

1. WHEN a User submits valid credentials, THE Authentication_Service SHALL issue a JWT token valid for 24 hours
2. WHEN a User submits invalid credentials, THE Authentication_Service SHALL reject the request and return an error message within 200ms
3. THE Authentication_Service SHALL enforce role-based permissions for all API endpoints
4. WHEN a User attempts to access a resource without proper permissions, THE Authentication_Service SHALL return a 403 Forbidden response
5. THE Platform SHALL log all authentication attempts to the Audit_Log table

### Requirement 2: File Upload and Validation

**User Story:** As an analyst, I want to upload historical production and financial data files, so that I can begin valuation analysis.

#### Acceptance Criteria

1. WHEN a User uploads a CSV or XLSX file, THE Asset_Intake_Module SHALL accept files up to 50MB in size
2. WHEN a file is uploaded, THE Asset_Intake_Module SHALL validate the file format within 5 seconds
3. IF a file contains invalid data types or missing required columns, THEN THE Asset_Intake_Module SHALL return a detailed validation error report
4. THE Asset_Intake_Module SHALL support CSV and XLSX file formats
5. WHEN a valid file is uploaded, THE Asset_Intake_Module SHALL store the file metadata in the uploaded_files table
6. THE Asset_Intake_Module SHALL sanitize all uploaded files to prevent malicious code execution

### Requirement 3: Data Extraction and Transformation

**User Story:** As an analyst, I want uploaded data to be automatically processed and normalized, so that I can work with clean, consistent data.

#### Acceptance Criteria

1. WHEN a valid file is uploaded, THE ETL_Pipeline SHALL extract data from the file within 10 seconds for files up to 50MB
2. THE ETL_Pipeline SHALL normalize units to standard formats (barrels for oil, MCF for gas, USD for currency)
3. WHEN data contains multiple currencies, THE ETL_Pipeline SHALL convert all values to USD using current exchange rates
4. THE ETL_Pipeline SHALL validate data ranges for production volumes, costs, and revenues
5. WHEN data validation completes, THE ETL_Pipeline SHALL compute a data quality score between 0 and 100
6. THE ETL_Pipeline SHALL store processed data in the production_data and financial_data tables
7. IF data extraction fails, THEN THE ETL_Pipeline SHALL log the error and notify the User

### Requirement 4: Asset Intake Dashboard

**User Story:** As an analyst, I want to view uploaded data status and historical KPIs, so that I can verify data quality before modeling.

#### Acceptance Criteria

1. THE Frontend SHALL display a file upload interface with drag-and-drop support
2. WHEN data processing completes, THE Frontend SHALL display validation status and data quality score
3. THE Frontend SHALL display historical KPI cards showing total production, average EBITDA, and total CAPEX
4. THE Frontend SHALL render production trend charts for the most recent 5 years of data
5. THE Frontend SHALL display EBITDA summary charts with monthly or quarterly granularity
6. WHEN a User clicks on a data quality issue, THE Frontend SHALL display detailed validation messages

### Requirement 5: Financial Modeling Configuration

**User Story:** As an analyst, I want to configure modeling assumptions, so that I can customize the valuation to specific deal parameters.

#### Acceptance Criteria

1. THE Frontend SHALL provide input forms for production assumptions including decline curves, commodity prices, and reserve estimates
2. THE Frontend SHALL provide input forms for cost assumptions including OPEX inflation, CAPEX schedules, and G&A expenses
3. THE Frontend SHALL provide input forms for synergy assumptions including overhead cuts, procurement efficiencies, and workforce consolidation
4. THE Frontend SHALL provide input forms for deal structure including purchase price, debt structure, and discount rate
5. WHEN a User saves assumptions, THE API SHALL validate all numeric inputs are within reasonable ranges
6. THE API SHALL store assumptions in the assumptions table linked to the Project
7. THE Frontend SHALL support creating multiple Scenario configurations (Bull, Base, Bear)

### Requirement 6: Production Decline Curve Modeling

**User Story:** As an analyst, I want to model future production using decline curves, so that I can forecast revenue streams.

#### Acceptance Criteria

1. THE Financial_Engine SHALL support exponential, hyperbolic, and harmonic decline curve models
2. WHEN a User selects a decline curve type and parameters, THE Financial_Engine SHALL compute monthly production forecasts for 20 years
3. THE Financial_Engine SHALL apply decline rates separately for oil and gas production streams
4. FOR ALL production forecasts, THE Financial_Engine SHALL ensure production volumes are non-negative
5. THE Financial_Engine SHALL store production forecasts in the valuation_outputs table

### Requirement 7: Cash Flow Forecasting

**User Story:** As an analyst, I want to forecast future cash flows, so that I can compute valuation metrics.

#### Acceptance Criteria

1. WHEN assumptions are configured, THE Financial_Engine SHALL compute annual revenue based on production forecasts and commodity prices
2. THE Financial_Engine SHALL compute annual OPEX by applying inflation rates to historical operating expenses
3. THE Financial_Engine SHALL compute annual CAPEX based on the configured capital expenditure schedule
4. THE Financial_Engine SHALL compute EBITDA as revenue minus OPEX minus transportation costs
5. THE Financial_Engine SHALL compute EBITDAX as EBITDA plus exploration expenses
6. THE Financial_Engine SHALL compute free cash flow as EBITDA minus CAPEX minus taxes plus depreciation
7. THE Financial_Engine SHALL compute cash flows for a 20-year forecast period
8. THE Financial_Engine SHALL store cash flow forecasts in the valuation_outputs table

### Requirement 8: Synergy Modeling

**User Story:** As an analyst, I want to model operational synergies, so that I can quantify value creation from the acquisition.

#### Acceptance Criteria

1. THE Financial_Engine SHALL compute cost synergies from operational overhead reductions
2. THE Financial_Engine SHALL compute cost synergies from procurement efficiencies
3. THE Financial_Engine SHALL compute cost synergies from workforce consolidation
4. THE Financial_Engine SHALL compute cost synergies from shared infrastructure savings
5. THE Financial_Engine SHALL apply synergy realization schedules over a configurable ramp-up period
6. WHEN synergies are modeled, THE Financial_Engine SHALL add synergy values to the base cash flow forecast
7. THE Financial_Engine SHALL store synergy calculations in the synergy_models table

### Requirement 9: Valuation Metrics Calculation

**User Story:** As an analyst, I want to compute valuation metrics, so that I can assess deal attractiveness.

#### Acceptance Criteria

1. WHEN cash flows are forecasted, THE Financial_Engine SHALL compute NPV using the configured discount rate
2. THE Financial_Engine SHALL compute IRR by finding the discount rate where NPV equals zero
3. THE Financial_Engine SHALL compute payback period as the time to recover initial investment
4. THE Financial_Engine SHALL compute ROIC as net operating profit after tax divided by invested capital
5. THE Financial_Engine SHALL compute terminal value using the exit multiple method
6. THE Financial_Engine SHALL compute debt paydown schedule based on free cash flow allocation
7. THE Financial_Engine SHALL compute accretion or dilution to earnings per share
8. FOR ALL IRR calculations, THE Financial_Engine SHALL converge to a solution within 0.01% accuracy or return an error
9. THE Financial_Engine SHALL store valuation metrics in the valuation_outputs table

### Requirement 10: Multi-Scenario Analysis

**User Story:** As an analyst, I want to run Bull, Base, and Bear scenarios, so that I can understand valuation sensitivity.

#### Acceptance Criteria

1. THE Financial_Engine SHALL support creating multiple Scenario configurations per Project
2. WHEN a User requests scenario analysis, THE Financial_Engine SHALL compute valuation metrics for all configured scenarios
3. THE Financial_Engine SHALL execute scenario calculations in parallel to minimize computation time
4. THE API SHALL return scenario results within 30 seconds for projects with up to 20 years of forecasts
5. THE Frontend SHALL display scenario comparison tables showing NPV, IRR, and payback period for each scenario

### Requirement 11: Sensitivity Analysis

**User Story:** As an analyst, I want to perform sensitivity analysis on key assumptions, so that I can identify value drivers.

#### Acceptance Criteria

1. THE Financial_Engine SHALL support sensitivity tables varying two assumptions simultaneously
2. THE Financial_Engine SHALL compute NPV and IRR for each combination in the sensitivity table
3. WHERE sensitivity analysis is requested, THE Financial_Engine SHALL support varying commodity prices, discount rates, CAPEX, OPEX, and synergy realization
4. THE Financial_Engine SHALL generate sensitivity tables with at least 5 values per variable
5. THE API SHALL return sensitivity results within 60 seconds

### Requirement 12: Waterfall Chart Visualization

**User Story:** As an analyst, I want to view a waterfall chart of value creation, so that I can communicate synergy contributions.

#### Acceptance Criteria

1. THE Visualization_Suite SHALL render a waterfall chart showing sequential value contributions
2. THE Visualization_Suite SHALL display base EBITDA as the starting point
3. THE Visualization_Suite SHALL display revenue synergies, cost synergies, operational efficiencies, and financing impacts as incremental bars
4. THE Visualization_Suite SHALL display final projected margin as the ending point
5. THE Visualization_Suite SHALL support exporting the waterfall chart as PNG or SVG
6. WHEN a User hovers over a bar, THE Visualization_Suite SHALL display the exact value and percentage contribution

### Requirement 13: IRR Projection Chart

**User Story:** As an analyst, I want to view IRR projections over time, so that I can understand return profiles.

#### Acceptance Criteria

1. THE Visualization_Suite SHALL render a line chart showing IRR projections for each year in the forecast period
2. THE Visualization_Suite SHALL display separate lines for Bull, Base, and Bear scenarios
3. THE Visualization_Suite SHALL highlight the target IRR threshold with a horizontal reference line
4. THE Visualization_Suite SHALL support zooming and panning on the chart
5. WHEN a User clicks on a data point, THE Visualization_Suite SHALL display detailed metrics for that year

### Requirement 14: Cash Flow Forecast Chart

**User Story:** As an analyst, I want to view forecasted cash flows, so that I can assess liquidity and debt service capacity.

#### Acceptance Criteria

1. THE Visualization_Suite SHALL render a stacked bar chart showing annual cash flow components
2. THE Visualization_Suite SHALL display revenue, OPEX, CAPEX, and free cash flow as separate series
3. THE Visualization_Suite SHALL support toggling visibility of individual cash flow components
4. THE Visualization_Suite SHALL display cash flows for the entire 20-year forecast period
5. THE Visualization_Suite SHALL support exporting cash flow data to CSV format

### Requirement 15: Production Decline Curve Chart

**User Story:** As an analyst, I want to view production decline curves, so that I can validate production forecasts.

#### Acceptance Criteria

1. THE Visualization_Suite SHALL render a line chart showing historical and forecasted production
2. THE Visualization_Suite SHALL display separate lines for oil and gas production
3. THE Visualization_Suite SHALL visually distinguish historical data from forecasted data
4. THE Visualization_Suite SHALL display the decline curve type and parameters on the chart
5. THE Visualization_Suite SHALL support displaying production in barrels per day or monthly totals

### Requirement 16: EBITDA Trend Chart

**User Story:** As an analyst, I want to view EBITDA trends, so that I can assess profitability over time.

#### Acceptance Criteria

1. THE Visualization_Suite SHALL render a line chart showing historical and forecasted EBITDA
2. THE Visualization_Suite SHALL display EBITDA and EBITDAX as separate lines
3. THE Visualization_Suite SHALL support monthly, quarterly, or annual aggregation
4. THE Visualization_Suite SHALL display synergy contributions as a separate series
5. WHEN a User hovers over a data point, THE Visualization_Suite SHALL display the exact EBITDA value and date

### Requirement 17: Synergy Realization Timeline Chart

**User Story:** As an analyst, I want to view synergy realization over time, so that I can understand the value creation schedule.

#### Acceptance Criteria

1. THE Visualization_Suite SHALL render a stacked area chart showing synergy realization by category
2. THE Visualization_Suite SHALL display operational overhead cuts, procurement efficiencies, workforce consolidation, and infrastructure savings as separate areas
3. THE Visualization_Suite SHALL display cumulative synergy value over the forecast period
4. THE Visualization_Suite SHALL support displaying synergies in absolute dollars or as percentage of target
5. THE Visualization_Suite SHALL display the synergy ramp-up schedule

### Requirement 18: Debt Paydown Chart

**User Story:** As an analyst, I want to view debt paydown schedules, so that I can assess leverage reduction.

#### Acceptance Criteria

1. THE Visualization_Suite SHALL render a line chart showing debt balance over time
2. THE Visualization_Suite SHALL display debt service coverage ratio as a secondary axis
3. THE Visualization_Suite SHALL highlight periods where debt service coverage falls below 1.2x
4. THE Visualization_Suite SHALL display principal and interest payments as separate series
5. THE Visualization_Suite SHALL support comparing debt paydown across scenarios

### Requirement 19: Project Management

**User Story:** As an analyst, I want to create and manage multiple projects, so that I can analyze different acquisition opportunities.

#### Acceptance Criteria

1. WHEN a User creates a new project, THE API SHALL generate a unique project identifier
2. THE API SHALL store project metadata including name, description, creation date, and owner in the projects table
3. THE API SHALL support listing all projects accessible to the User
4. THE API SHALL support updating project metadata
5. THE API SHALL support deleting projects and all associated data
6. WHEN a project is deleted, THE API SHALL remove all related records from uploaded_files, production_data, financial_data, assumptions, scenarios, synergy_models, and valuation_outputs tables

### Requirement 20: Data Export

**User Story:** As an analyst, I want to export valuation results, so that I can include them in investment memos and presentations.

#### Acceptance Criteria

1. THE API SHALL support exporting cash flow forecasts to XLSX format
2. THE API SHALL support exporting valuation metrics to XLSX format
3. THE API SHALL support exporting scenario comparison tables to XLSX format
4. THE API SHALL support exporting sensitivity tables to XLSX format
5. WHEN a User requests an export, THE API SHALL generate the file within 10 seconds
6. THE API SHALL include project metadata and assumptions in exported files

### Requirement 21: Audit Logging

**User Story:** As a compliance officer, I want all system actions to be logged, so that I can maintain an audit trail.

#### Acceptance Criteria

1. THE Platform SHALL log all User authentication events to the Audit_Log table
2. THE Platform SHALL log all file uploads to the Audit_Log table
3. THE Platform SHALL log all assumption changes to the Audit_Log table
4. THE Platform SHALL log all valuation calculations to the Audit_Log table
5. THE Platform SHALL log all data exports to the Audit_Log table
6. WHEN an audit log entry is created, THE Platform SHALL record the User identifier, timestamp, action type, and affected resources
7. THE Platform SHALL retain audit logs for at least 7 years

### Requirement 22: API Rate Limiting

**User Story:** As a platform administrator, I want API rate limiting, so that I can prevent abuse and ensure fair resource allocation.

#### Acceptance Criteria

1. THE API SHALL limit authenticated users to 1000 requests per hour
2. THE API SHALL limit unauthenticated requests to 100 requests per hour
3. WHEN a User exceeds the rate limit, THE API SHALL return a 429 Too Many Requests response
4. THE API SHALL include rate limit headers in all responses showing remaining quota and reset time
5. WHERE a User has premium access, THE API SHALL apply higher rate limits of 5000 requests per hour

### Requirement 23: Input Validation

**User Story:** As a platform administrator, I want comprehensive input validation, so that I can prevent invalid data from corrupting the system.

#### Acceptance Criteria

1. THE API SHALL validate all numeric inputs are within reasonable ranges for financial data
2. THE API SHALL validate all date inputs are in ISO 8601 format
3. THE API SHALL validate all currency codes are valid ISO 4217 codes
4. WHEN invalid input is received, THE API SHALL return a 400 Bad Request response with detailed error messages
5. THE API SHALL sanitize all text inputs to prevent SQL injection and XSS attacks
6. THE API SHALL validate file uploads contain only allowed MIME types

### Requirement 24: Database Schema

**User Story:** As a database administrator, I want a well-designed schema, so that I can ensure data integrity and query performance.

#### Acceptance Criteria

1. THE Database SHALL include tables for users, projects, uploaded_files, production_data, financial_data, assumptions, scenarios, synergy_models, valuation_outputs, and audit_logs
2. THE Database SHALL enforce foreign key constraints between related tables
3. THE Database SHALL include indexes on frequently queried columns
4. THE Database SHALL support concurrent access from multiple users
5. THE Database SHALL use transactions to ensure data consistency during multi-step operations

### Requirement 25: Performance Optimization

**User Story:** As an analyst, I want fast response times, so that I can work efficiently.

#### Acceptance Criteria

1. THE API SHALL respond to data retrieval requests within 500ms for datasets up to 10,000 rows
2. THE Financial_Engine SHALL complete valuation calculations within 30 seconds for 20-year forecasts
3. THE Frontend SHALL render charts within 2 seconds after receiving data
4. THE Platform SHALL support at least 50 concurrent users without performance degradation
5. THE API SHALL use caching for frequently accessed data to reduce database load
6. THE API SHALL use background workers for long-running calculations

### Requirement 26: User Interface Design

**User Story:** As an analyst, I want a professional and intuitive interface, so that I can work efficiently.

#### Acceptance Criteria

1. THE Frontend SHALL implement a dark mode and light mode theme
2. THE Frontend SHALL be responsive and support desktop, tablet, and mobile screen sizes
3. THE Frontend SHALL use animated transitions for navigation and data updates
4. THE Frontend SHALL follow accessibility guidelines including keyboard navigation and screen reader support
5. THE Frontend SHALL display loading indicators during asynchronous operations
6. THE Frontend SHALL display error messages in a user-friendly format

### Requirement 27: Error Handling

**User Story:** As an analyst, I want clear error messages, so that I can understand and resolve issues.

#### Acceptance Criteria

1. WHEN an error occurs, THE API SHALL return a structured error response with error code, message, and details
2. THE Frontend SHALL display error messages in modal dialogs or toast notifications
3. THE Platform SHALL log all errors to application logs for debugging
4. IF a calculation fails, THEN THE Financial_Engine SHALL return a descriptive error message indicating which assumption caused the failure
5. THE Platform SHALL handle network errors gracefully and allow users to retry failed operations

### Requirement 28: Configuration File Parser

**User Story:** As an analyst, I want to save and load modeling configurations, so that I can reuse assumptions across projects.

#### Acceptance Criteria

1. THE Platform SHALL support exporting assumptions to JSON configuration files
2. THE Platform SHALL support importing assumptions from JSON configuration files
3. WHEN a configuration file is imported, THE Configuration_Parser SHALL parse it into an Assumptions object
4. WHEN an invalid configuration file is provided, THE Configuration_Parser SHALL return a descriptive error
5. THE Configuration_Printer SHALL format Assumptions objects back into valid JSON configuration files
6. FOR ALL valid Assumptions objects, parsing then printing then parsing SHALL produce an equivalent object

### Requirement 29: Deployment and Infrastructure

**User Story:** As a DevOps engineer, I want containerized deployment, so that I can deploy the platform consistently across environments.

#### Acceptance Criteria

1. THE Platform SHALL provide Docker containers for the Frontend, API, and Database
2. THE Platform SHALL provide a Docker Compose configuration for local development
3. THE Platform SHALL use Nginx as a reverse proxy for the API and Frontend
4. THE Platform SHALL support environment-specific configuration through environment variables
5. THE Platform SHALL include health check endpoints for monitoring

### Requirement 30: Testing Coverage

**User Story:** As a developer, I want comprehensive test coverage, so that I can ensure system reliability.

#### Acceptance Criteria

1. THE Platform SHALL include unit tests for all Financial_Engine calculation functions
2. THE Platform SHALL include integration tests for all API endpoints
3. THE Platform SHALL include component tests for all Frontend components
4. THE Platform SHALL achieve at least 80% code coverage for backend code
5. THE Platform SHALL include tests validating financial calculation accuracy against known benchmarks
6. THE Platform SHALL include tests for error handling and edge cases
