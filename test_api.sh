#!/bin/bash

# Test API endpoints

echo "=== Testing Backend API ==="
echo ""

# Step 1: Register a test user
echo "1. Registering test user..."
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test_'$(date +%s)'@example.com",
    "password": "TestPass123!",
    "full_name": "Test User"
  }')

echo "Register response: $REGISTER_RESPONSE"
echo ""

# Step 2: Login
echo "2. Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "saketsuman.ai.2023@gmail.com",
    "password": "Saket@123"
  }')

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "Login failed! Response: $LOGIN_RESPONSE"
  exit 1
fi

echo "Login successful! Token: ${TOKEN:0:50}..."
echo ""

# Step 3: Create a project
echo "3. Creating project..."
PROJECT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Project '$(date +%s)'",
    "description": "Test project for API testing",
    "project_type": "Acquisition"
  }')

PROJECT_ID=$(echo $PROJECT_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -z "$PROJECT_ID" ]; then
  echo "Project creation failed! Response: $PROJECT_RESPONSE"
  exit 1
fi

echo "Project created! ID: $PROJECT_ID"
echo ""

# Step 4: Create assumptions
echo "4. Creating assumptions..."
ASSUMPTIONS_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/modeling/assumptions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": '$PROJECT_ID',
    "version": 1,
    "name": "Base Case",
    "decline_curve_type": "exponential",
    "decline_rate": 0.15,
    "oil_price_forecast": [
      {"year": 1, "price": 75.00},
      {"year": 2, "price": 78.00}
    ],
    "gas_price_forecast": [
      {"year": 1, "price": 3.50},
      {"year": 2, "price": 3.75}
    ],
    "opex_inflation_rate": 0.03,
    "capex_schedule": [
      {"year": 1, "amount": 5000000}
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
  }')

ASSUMPTIONS_ID=$(echo $ASSUMPTIONS_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -z "$ASSUMPTIONS_ID" ]; then
  echo "Assumptions creation failed! Response: $ASSUMPTIONS_RESPONSE"
else
  echo "Assumptions created! ID: $ASSUMPTIONS_ID"
fi
echo ""

# Step 5: Create a test CSV file
echo "5. Creating test production data file..."
cat > /tmp/test_production.csv << 'EOF'
date,well_id,oil_production,gas_production,water_production
2024-01-01,WELL-001,1000,5000,500
2024-02-01,WELL-001,950,4800,520
2024-03-01,WELL-001,900,4600,540
EOF

echo "Test file created"
echo ""

# Step 6: Upload file
echo "6. Uploading production data..."
UPLOAD_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/upload/production \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/test_production.csv" \
  -F "project_id=$PROJECT_ID")

echo "Upload response: $UPLOAD_RESPONSE"
echo ""

echo "=== Test Complete ==="
echo ""
echo "Summary:"
echo "- Project ID: $PROJECT_ID"
echo "- Assumptions ID: $ASSUMPTIONS_ID"
echo ""
echo "You can now:"
echo "1. View project at: http://localhost:5173/projects/$PROJECT_ID"
echo "2. Check API docs at: http://localhost:8000/api/v1/docs"
