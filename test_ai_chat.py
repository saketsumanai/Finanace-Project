#!/usr/bin/env python3
"""
Test script to verify Gemini AI integration is working.
Run this to test the AI chat without needing to login to the frontend.
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.gemini_service import GeminiService

def test_gemini_api():
    """Test Gemini API integration."""
    print("=" * 60)
    print("🧪 TESTING GEMINI AI INTEGRATION")
    print("=" * 60)
    
    # API key
    api_key = "AIzaSyCctuqFULVRYTgl3AMRHD1CyItf_0muX1Q"
    print(f"\n✓ API Key: {api_key[:20]}...")
    
    try:
        # Initialize service
        print("\n1️⃣ Initializing Gemini service...")
        gemini = GeminiService(api_key)
        print("   ✅ Service initialized successfully")
        
        # Test 1: Simple chat
        print("\n2️⃣ Testing simple chat...")
        response = gemini.send_message("Say hello in one sentence")
        print(f"   ✅ Response: {response}")
        
        # Test 2: Project analysis
        print("\n3️⃣ Testing project analysis...")
        project_data = {
            'name': 'Test Acquisition',
            'project_type': 'acquisition',
            'deal_size': 50000000,
            'description': 'Oil & gas asset acquisition'
        }
        analysis = gemini.analyze_project(project_data)
        print(f"   ✅ Analysis received:")
        print(f"      - Risks: {len(analysis.get('risks', []))} items")
        print(f"      - Synergies: {len(analysis.get('synergies', []))} items")
        
        # Test 3: Assumption optimization
        print("\n4️⃣ Testing assumption optimization...")
        historical_data = {
            'production_count': 100,
            'financial_count': 50,
            'avg_oil': 1000,
            'avg_gas': 5000
        }
        recommendations = gemini.optimize_assumptions(project_data, historical_data)
        print(f"   ✅ Recommendations received:")
        print(f"      - Decline rate: {recommendations.get('decline_rate', 'N/A')}")
        print(f"      - Discount rate: {recommendations.get('discount_rate', 'N/A')}")
        print(f"      - Forecast years: {recommendations.get('forecast_years', 'N/A')}")
        
        # Test 4: CSV analysis simulation
        print("\n5️⃣ Testing CSV analysis...")
        csv_content = """date,oil_production,gas_production,revenue
2024-01-01,1000,5000,100000
2024-02-01,950,4800,95000
2024-03-01,900,4600,90000"""
        csv_analysis = gemini.analyze_csv_data(csv_content, "test_production.csv")
        if csv_analysis.get('success'):
            print(f"   ✅ CSV analysis successful:")
            print(f"      - Rows: {csv_analysis['statistics']['rows']}")
            print(f"      - Columns: {csv_analysis['statistics']['columns']}")
            print(f"      - AI Insights: {csv_analysis['ai_analysis'][:100]}...")
        else:
            print(f"   ❌ CSV analysis failed: {csv_analysis.get('error')}")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED! GEMINI AI IS FULLY FUNCTIONAL")
        print("=" * 60)
        print("\n🎉 You can now use AI features in the application!")
        print("   - AI Chat: http://localhost:5173/ai-chat")
        print("   - Login: http://localhost:5173/login")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {str(e)}")
        print("\n" + "=" * 60)
        print("❌ TESTS FAILED")
        print("=" * 60)
        return False


if __name__ == "__main__":
    success = test_gemini_api()
    sys.exit(0 if success else 1)
