# Testing File Upload & Assumptions

## Quick Test Guide

### Step 1: Login and Get Token
1. Go to http://localhost:5173
2. Login with your credentials
3. Open browser DevTools (F12)
4. Go to Application > Local Storage > http://localhost:5173
5. Copy the `token` value

### Step 2: Test File Upload via UI
1. Navigate to a project
2. Look for "Upload Data" or similar button
3. Select a CSV or XLSX file
4. Choose file type (Production or Financial)
5. Click Upload
6. Should see success message

### Step 3: Test File Upload via API

Create a test CSV file:
```bash
cat > /tmp/test_production.csv << 'EOF'
date,well_id,oil_production,gas_production
2024-01-01,WELL-001,1000,5000
2024-02-01,WELL-001,950,4800
2024-03-01,WELL-001,900,4600
EOF
```

Upload via curl:
```bash
# Replace YOUR_TOKEN with actual token from Step 1
TOKEN="YOUR_TOKEN"

curl -X POST http://localhost:8000/api/v1/upload/production \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/test_production.csv" \
  -F "project_id=1"
```

Expected response:
```json
{
  "file_id": 1,
  "filename": "test_production.csv",
  "file_size": 123,
  "status": "pending",
  "message": "File uploaded successfully."
}
```

### Step 4: Test Assumptions Creation via API

```bash
TOKEN="YOUR_TOKEN"

curl -X POST http://localhost:8000/api/v1/modeling/assumptions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "version": 1,
    "name": "Base Case",
    "decline_curve_type": "exponential",
    "decline_rate": 0.15,
    "oil_price_forecast": [
      {"year": 1, "price": 75.00},
      {"year": 2, "price": 78.00},
      {"year": 3, "price": 80.00}
    ],
    "gas_price_forecast": [
      {"year": 1, "price": 3.50},
      {"year": 2, "price": 3.75},
      {"year": 3, "price": 4.00}
    ],
    "opex_inflation_rate": 0.03,
    "capex_schedule": [
      {"year": 1, "amount": 5000000},
      {"year": 2, "amount": 3000000}
    ],
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

Expected response:
```json
{
  "id": 1,
  "project_id": 1,
  "version": 1,
  "name": "Base Case",
  "decline_curve_type": "exponential",
  "decline_rate": "0.1500",
  ...
}
```

### Step 5: List Files for Project

```bash
TOKEN="YOUR_TOKEN"

curl -X GET http://localhost:8000/api/v1/upload/project/1 \
  -H "Authorization: Bearer $TOKEN"
```

Expected response:
```json
{
  "project_id": 1,
  "files": [
    {
      "file_id": 1,
      "filename": "test_production.csv",
      "file_type": "production",
      "file_size": 123,
      "status": "pending",
      "quality_score": null,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Step 6: Check File Status

```bash
TOKEN="YOUR_TOKEN"

curl -X GET http://localhost:8000/api/v1/upload/1/status \
  -H "Authorization: Bearer $TOKEN"
```

## What Should Work Now

✅ **File Upload**
- Upload production data (CSV/XLSX)
- Upload financial data (CSV/XLSX)
- Files are saved to disk
- Database records created
- Status tracking

✅ **Assumptions Creation**
- Create modeling assumptions
- Set decline curves
- Define price forecasts
- Configure costs
- Set deal parameters

✅ **Project Management**
- Create projects
- View project list
- Access project details

## Common Issues & Solutions

### Issue: "Project not found"
**Solution**: Make sure you're using the correct project_id. List your projects first:
```bash
curl -X GET http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer $TOKEN"
```

### Issue: "Unauthorized"
**Solution**: Your token may have expired. Login again and get a new token.

### Issue: "File validation failed"
**Solution**: Check file format. Must be CSV or XLSX with correct columns.

## Next Steps After Testing

Once file upload and assumptions work:
1. Create synergy models
2. Create scenarios
3. Run valuations
4. View results
5. Compare scenarios

## API Documentation

Full API documentation available at:
http://localhost:8000/docs

This provides interactive testing of all endpoints.
