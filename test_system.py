#!/usr/bin/env python3
"""
Simple test script to verify the backend system works
"""
import sys
import subprocess
import json
import time

def test_imports():
    """Test that all required packages can be imported"""
    try:
        print("Testing Python imports...")
        
        # Test FastAPI and related packages
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        import structlog
        import httpx
        
        # Test our app modules
        sys.path.append('backend')
        from app.core.config import settings
        from app.schemas.aircraft import AircraftCreate
        
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_validation():
    """Test data validation with sample aircraft data"""
    try:
        print("Testing data validation...")
        
        sys.path.append('backend')
        from app.schemas.aircraft import AircraftCreate
        
        # Test with valid data
        valid_aircraft = {
            "hex": "ae1460",
            "type": "adsb_icao",
            "flight": "TEST123",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "altitude_baro": 1000
        }
        
        aircraft = AircraftCreate(**valid_aircraft)
        print(f"✅ Valid aircraft created: {aircraft.hex}")
        
        # Test with invalid data
        try:
            invalid_aircraft = {
                "hex": "invalid",  # Too short
                "type": "adsb_icao",
                "latitude": 200,  # Invalid latitude
            }
            AircraftCreate(**invalid_aircraft)
            print("❌ Should have failed validation")
            return False
        except Exception:
            print("✅ Invalid data properly rejected")
        
        return True
        
    except Exception as e:
        print(f"❌ Data validation error: {e}")
        return False

def test_mock_client():
    """Test the mock aircraft client"""
    try:
        print("Testing mock aircraft client...")
        
        sys.path.append('backend')
        from app.clients.mock_aircraft_client import MockAircraftClient
        
        import asyncio
        
        async def run_client_test():
            client = MockAircraftClient()
            data = await client.fetch_data()
            
            print(f"✅ Mock client generated {len(data)} aircraft")
            
            # Validate first aircraft
            if data:
                first_aircraft = data[0]
                if client.validate_data(first_aircraft):
                    print("✅ Mock data validation passed")
                    return True
                else:
                    print("❌ Mock data validation failed")
                    return False
            return True
        
        return asyncio.run(run_client_test())
        
    except Exception as e:
        print(f"❌ Mock client error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing SkyTrace System Components\n")
    
    tests = [
        ("Python Imports", test_imports),
        ("Data Validation", test_data_validation),
        ("Mock Client", test_mock_client),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System components are working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)