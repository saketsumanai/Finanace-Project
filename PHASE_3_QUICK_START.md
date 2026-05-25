# Phase 3: Quick Start Guide

## 🚀 Getting Started with Financial Modeling

This guide shows you how to use the Phase 3 financial modeling APIs.

---

## Prerequisites

1. Backend server running: `docker-compose up`
2. Database migrated: `alembic upgrade head`
3. User authenticated: JWT token obtained from `/api/v1/auth/login`
4. Project created with historical data uploaded (Phase 1 & 2)

---

## API Base URL

```
http://localhost:8000/api/v1/modeling
```

---

## Quick Workflow

### 1️⃣ Create Assumptions

**Endpoint:** `POST /modeling/assumptions`

**Minimal Example:**
```json
{
  "project_id": "your-project-uuid",
  "name": "Base Case",
  "version": 1,
  "decline_curve_type": "hyperbolic",
  "decline_rate": 0.15,
  "hyperbolic_b": 0.5,
  "oil_price_forecast": [
    {"year": 1, "price": 70.0},
    {"year": 10, "price": 80.0}
  ],
  "gas_price_forecast": [
    {"year": 1, "price": 3.5},
    {"year": 10, "price": 4.0}
  ],
  "purchase_price": 50000000,
  "discount_rate": 0.12,
  "tax_rate": 0.21,
  "exit_multiple": 5.5
}
```

**Response:**
```json
{
  "id": "assumptions-uuid",
  "project_id": "your-project-uuid",
  "name": "Base Case",
  "version": 1,
  ...
}
```

---

### 2️⃣ Add Synergies (Optional)

**Endpoint:** `POST /modeling/assumptions/{assumptions_id}/synergies`

**Example:**
```json
{
  "category": "operational_overhead",
  "description": "Consolidate field offices",
  "target_value": 2000000,
  "realization_schedule": [
    {"year": 1, "percentage": 0.25},
    {"year": 2, "percentage": 0.60},
    {"year": 3, "percentage": 0.85},
    {"year": 4, "percentage": 1.00}
  ]
}
```

---

### 3️⃣ Create Scenario

**Endpoint:** `POST /modeling/scenarios`

**Example:**
```json
{
  "project_id": "your-project-uuid",
  "assumptions_id": "assumptions-uuid",
  "name": "Base Case",
  "scenario_type": "base",
  "description": "Conservative assumptions"
}
```

**Response:**
```json
{
  "id": "scenario-uuid",
  "project_id": "your-project-uuid",
  "assumptions_id": "assumptions-uuid",
  "name": "Base Case",
  "scenario_type": "base",
  ...
}
```

---

### 4️⃣ Run Valuation

**Endpoint:** `POST /modeling/valuation/run`

**Example:**
```json
{
  "scenario_id": "scenario-uuid",
  "periods_per_year": 12
}
```

**Response:**
```json
{
  "scenario_id": "scenario-uuid",
  "scenario_name": "Base Case",
  "scenario_type": "base",
  "metrics": {
    "npv": 15234567.89,
    "irr": 0.1845,
    "payback_period": 3.2,
    "roi": 0.45,
    "roic": 0.18,
    "profitability_index": 1.30,
    "terminal_value": 45000000
  },
  "summary_financials": {
    "total_revenue": 250000000,
    "total_opex": 80000000,
    "total_capex": 15000000,
    "total_synergies": 25000000,
    "total_ebitda": 120000000,
    "total_fcf": 95000000
  }
}
```

---

### 5️⃣ Get Detailed Results

**Endpoint:** `GET /modeling/valuation/results/{scenario_id}`

**Response includes:**
- All valuation metrics
- Annual data for all forecast years
- Production forecasts
- Revenue and cost breakdowns
- Cash flow details

---

### 6️⃣ Compare Scenarios

**Endpoint:** `POST /modeling/valuation/compare`

**Example:**
```json
{
  "scenario_ids": [
    "base-scenario-uuid",
    "bull-scenario-uuid",
    "bear-scenario-uuid"
  ]
}
```

**Response:**
```json
{
  "scenarios": [
    {
      "scenario_id": "base-scenario-uuid",
      "scenario_name": "Base Case",
      "scenario_type": "base",
      "npv": 15234567.89,
      "irr": 0.1845,
      "payback_period": 3.2,
      "roic": 0.18
    },
    {
      "scenario_id": "bull-scenario-uuid",
      "scenario_name": "Bull Case",
      "scenario_type": "bull",
      "npv": 25000000.00,
      "irr": 0.2250,
      "payback_period": 2.5,
      "roic": 0.25
    },
    ...
  ]
}
```

---

## Common Parameters

### Decline Curve Types
- `"exponential"` - Constant percentage decline (most conservative)
- `"hyperbolic"` - Variable decline (most common, requires `hyperbolic_b`)
- `"harmonic"` - Slowest decline (most optimistic)

### Scenario Types
- `"base"` - Base case assumptions
- `"bull"` - Optimistic assumptions
- `"bear"` - Conservative assumptions
- `"custom"` - Custom scenario

### Synergy Categories
- `"operational_overhead"` - G&A and overhead reduction
- `"procurement_efficiency"` - Volume discounts and supplier savings
- `"workforce_consolidation"` - Labor optimization
- `"shared_infrastructure"` - Shared facilities and equipment

---

## Full Example: Complete Workflow

```bash
# 1. Create assumptions
curl -X POST http://localhost:8000/api/v1/modeling/assumptions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "PROJECT_UUID",
    "name": "Base Case Assumptions",
    "version": 1,
    "decline_curve_type": "hyperbolic",
    "decline_rate": 0.15,
    "hyperbolic_b": 0.5,
    "oil_price_forecast": [
      {"year": 1, "price": 70.0},
      {"year": 5, "price": 75.0},
      {"year": 10, "price": 80.0}
    ],
    "gas_price_forecast": [
      {"year": 1, "price": 3.5},
      {"year": 5, "price": 3.8},
      {"year": 10, "price": 4.0}
    ],
    "opex_inflation_rate": 0.03,
    "capex_schedule": [
      {"year": 1, "amount": 5000000},
      {"year": 3, "amount": 2000000}
    ],
    "transportation_cost_per_unit": 2.5,
    "ga_annual": 1000000,
    "purchase_price": 50000000,
    "debt_amount": 30000000,
    "equity_amount": 20000000,
    "discount_rate": 0.12,
    "tax_rate": 0.21,
    "exit_multiple": 5.5,
    "forecast_years": 20
  }'

# Save the returned assumptions_id

# 2. Add synergy model
curl -X POST http://localhost:8000/api/v1/modeling/assumptions/ASSUMPTIONS_UUID/synergies \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "operational_overhead",
    "description": "Consolidate field offices and eliminate duplicate G&A",
    "target_value": 2000000,
    "realization_schedule": [
      {"year": 1, "percentage": 0.25},
      {"year": 2, "percentage": 0.60},
      {"year": 3, "percentage": 0.85},
      {"year": 4, "percentage": 1.00}
    ]
  }'

# 3. Create scenario
curl -X POST http://localhost:8000/api/v1/modeling/scenarios \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "PROJECT_UUID",
    "assumptions_id": "ASSUMPTIONS_UUID",
    "name": "Base Case",
    "scenario_type": "base",
    "description": "Conservative assumptions with standard synergy realization"
  }'

# Save the returned scenario_id

# 4. Run valuation
curl -X POST http://localhost:8000/api/v1/modeling/valuation/run \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "scenario_id": "SCENARIO_UUID",
    "periods_per_year": 12
  }'

# 5. Get results
curl -X GET http://localhost:8000/api/v1/modeling/valuation/results/SCENARIO_UUID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Python Example

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"
TOKEN = "your-jwt-token"
headers = {"Authorization": f"Bearer {TOKEN}"}

# 1. Create assumptions
assumptions_data = {
    "project_id": "project-uuid",
    "name": "Base Case",
    "version": 1,
    "decline_curve_type": "hyperbolic",
    "decline_rate": 0.15,
    "hyperbolic_b": 0.5,
    "oil_price_forecast": [
        {"year": 1, "price": 70.0},
        {"year": 10, "price": 80.0}
    ],
    "gas_price_forecast": [
        {"year": 1, "price": 3.5},
        {"year": 10, "price": 4.0}
    ],
    "purchase_price": 50000000,
    "discount_rate": 0.12,
    "tax_rate": 0.21,
    "exit_multiple": 5.5
}

response = requests.post(
    f"{BASE_URL}/modeling/assumptions",
    json=assumptions_data,
    headers=headers
)
assumptions = response.json()
assumptions_id = assumptions["id"]

# 2. Add synergy
synergy_data = {
    "category": "operational_overhead",
    "target_value": 2000000,
    "realization_schedule": [
        {"year": 1, "percentage": 0.25},
        {"year": 2, "percentage": 0.60},
        {"year": 3, "percentage": 0.85},
        {"year": 4, "percentage": 1.00}
    ]
}

requests.post(
    f"{BASE_URL}/modeling/assumptions/{assumptions_id}/synergies",
    json=synergy_data,
    headers=headers
)

# 3. Create scenario
scenario_data = {
    "project_id": "project-uuid",
    "assumptions_id": assumptions_id,
    "name": "Base Case",
    "scenario_type": "base"
}

response = requests.post(
    f"{BASE_URL}/modeling/scenarios",
    json=scenario_data,
    headers=headers
)
scenario = response.json()
scenario_id = scenario["id"]

# 4. Run valuation
valuation_request = {
    "scenario_id": scenario_id,
    "periods_per_year": 12
}

response = requests.post(
    f"{BASE_URL}/modeling/valuation/run",
    json=valuation_request,
    headers=headers
)
results = response.json()

print(f"NPV: ${results['metrics']['npv']:,.2f}")
print(f"IRR: {results['metrics']['irr']*100:.2f}%")
print(f"Payback: {results['metrics']['payback_period']:.1f} years")
```

---

## Tips & Best Practices

### 1. **Start Simple**
- Begin with minimal assumptions
- Add complexity gradually
- Test with known values

### 2. **Validate Inputs**
- Check decline rates (typically 10-30%)
- Verify price forecasts are reasonable
- Ensure CAPEX schedule makes sense

### 3. **Use Realistic Synergies**
- Don't over-estimate synergy values
- Use conservative realization schedules
- Document assumptions clearly

### 4. **Compare Scenarios**
- Always create Bull/Base/Bear cases
- Use consistent assumptions across scenarios
- Vary only key drivers

### 5. **Review Results**
- Check if IRR > discount rate
- Verify payback period is reasonable
- Ensure NPV makes sense given investment

---

## Common Issues

### Issue: "No historical production data available"
**Solution:** Upload production data first (Phase 2)

### Issue: "hyperbolic_b is required"
**Solution:** Provide `hyperbolic_b` when using hyperbolic decline curve

### Issue: "Scenario not found"
**Solution:** Verify scenario_id is correct and belongs to your user

### Issue: "Valuation failed"
**Solution:** Check that historical data exists and assumptions are valid

---

## Next Steps

1. ✅ Create assumptions for your project
2. ✅ Add synergy models
3. ✅ Create Bull/Base/Bear scenarios
4. ✅ Run valuations
5. ✅ Compare results
6. 🔜 Build frontend UI (Phase 4)
7. 🔜 Add visualizations (Phase 5)

---

## API Documentation

Full interactive documentation:
```
http://localhost:8000/api/v1/docs
```

---

## Support

- **Architecture**: `docs/ARCHITECTURE_AND_EXECUTION_PLAN.md`
- **Full Documentation**: `PHASE_3_COMPLETE.md`
- **Summary**: `PHASE_3_SUMMARY.md`
- **This Guide**: `PHASE_3_QUICK_START.md`

---

**Happy Modeling! 🚀**
