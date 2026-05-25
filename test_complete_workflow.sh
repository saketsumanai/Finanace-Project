#!/bin/bash

echo "=== Testing Complete Valuation Workflow ==="
echo ""

# Use existing user
EMAIL="testuser@test.com"
PASSWORD="TestPass123!"

# Login
echo "1. Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo "Login failed! Creating new user..."
  
  # Register new user
  EMAIL="testuser$(date +%s)@test.com"
  curl -s -X POST http://localhost:8000/api/v1/auth/register \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\", \"full_name\": \"Test User\"}" > /dev/null
  
  # Login again
  LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")
  
  TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
fi

echo "✓ Logged in successfully"
echo ""

# Create project
echo "2. Creating project..."
PROJECT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Valuation Project",
    "description": "Testing complete workflow",
    "project_type": "Acquisition"
  }')

PROJECT_ID=$(echo $PROJECT_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "✓ Project created: ID=$PROJECT_ID"
echo ""

# Create assumptions
echo "3. Creating assumptions..."
ASSUMPTIONS_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/modeling/assumptions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"project_id\": $PROJECT_ID,
    \"version\": 1,
    \"name\": \"Base Case\",
    \"decline_curve_type\": \"exponential\",
    \"decline_rate\": 0.15,
    \"oil_price_forecast\": [
      {\"year\": 1, \"price\": 75.00},
      {\"year\": 2, \"price\": 78.00},
      {\"year\": 3, \"price\": 80.00}
    ],
    \"gas_price_forecast\": [
      {\"year\": 1, \"price\": 3.50},
      {\"year\": 2, \"price\": 3.75},
      {\"year\": 3, \"price\": 4.00}
    ],
    \"opex_inflation_rate\": 0.03,
    \"capex_schedule\": [
      {\"year\": 1, \"amount\": 5000000}
    ],
    \"transportation_cost_per_unit\": 2.50,
    \"ga_annual\": 500000,
    \"purchase_price\": 50000000,
    \"debt_amount\": 30000000,
    \"equity_amount\": 20000000,
    \"discount_rate\": 0.10,
    \"tax_rate\": 0.21,
    \"exit_multiple\": 5.5,
    \"forecast_years\": 10
  }")

ASSUMPTIONS_ID=$(echo $ASSUMPTIONS_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "✓ Assumptions created: ID=$ASSUMPTIONS_ID"
echo ""

# Create scenario
echo "4. Creating scenario..."
SCENARIO_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/modeling/scenarios \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"project_id\": $PROJECT_ID,
    \"assumptions_id\": $ASSUMPTIONS_ID,
    \"name\": \"Base Case Scenario\",
    \"scenario_type\": \"base\",
    \"description\": \"Base case valuation\"
  }")

SCENARIO_ID=$(echo $SCENARIO_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "✓ Scenario created: ID=$SCENARIO_ID"
echo ""

# Run valuation
echo "5. Running valuation..."
VALUATION_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/modeling/valuation/run \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"scenario_id\": $SCENARIO_ID,
    \"periods_per_year\": 12
  }")

echo "Valuation response:"
echo $VALUATION_RESPONSE | python3 -m json.tool
echo ""

# Get results
echo "6. Getting valuation results..."
RESULTS_RESPONSE=$(curl -s -X GET "http://localhost:8000/api/v1/modeling/valuation/results/$SCENARIO_ID" \
  -H "Authorization: Bearer $TOKEN")

echo "Results:"
echo $RESULTS_RESPONSE | python3 -m json.tool | head -50
echo ""

echo "=== Test Complete ==="
echo ""
echo "Summary:"
echo "- Project ID: $PROJECT_ID"
echo "- Assumptions ID: $ASSUMPTIONS_ID"
echo "- Scenario ID: $SCENARIO_ID"
echo ""
echo "You can now view this in the UI at:"
echo "http://localhost:5173/projects/$PROJECT_ID/modeling"
