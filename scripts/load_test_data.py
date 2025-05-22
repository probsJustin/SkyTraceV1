#!/usr/bin/env python3
"""
Script to load test data into the SkyTrace system
"""
import json
import asyncio
import httpx

API_BASE_URL = "http://localhost:8000/api/v1"

async def load_test_data():
    """Load test aircraft data"""
    
    # Load test data from file
    with open('backend/test_data.json', 'r') as f:
        test_data = json.load(f)
    
    async with httpx.AsyncClient() as client:
        try:
            # Load aircraft data
            print("Loading test aircraft data...")
            response = await client.post(
                f"{API_BASE_URL}/aircraft/bulk",
                json=test_data["aircraft"]
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Successfully loaded aircraft data:")
                print(f"   - Created: {result['created']}")
                print(f"   - Updated: {result['updated']}")
                print(f"   - Errors: {result['errors']}")
            else:
                print(f"❌ Failed to load aircraft data: {response.status_code}")
                print(response.text)
        
        except Exception as e:
            print(f"❌ Error loading test data: {e}")

if __name__ == "__main__":
    asyncio.run(load_test_data())