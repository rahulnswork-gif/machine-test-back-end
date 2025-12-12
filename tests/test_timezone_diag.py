import requests
import json
import time
import random
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api/v1"

def test_timezone_diagnostic():
    print("=" * 70)
    print("TIMEZONE DIAGNOSTIC TEST")
    print("=" * 70)
    
    # Login
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "testuser@example.com", "password": "securepass123"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Explicitly set start_date to cover yesterday and today
    start_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"Testing Range: {start_date} to {end_date}")
    
    # Test 1: UTC
    print("\n1. Querying in UTC...")
    params = {
        "timezone": "UTC",
        "start_date": start_date,
        "end_date": end_date
    }
    response = requests.get(f"{BASE_URL}/analytics/stats", params=params, headers=headers)
    data = response.json()
    
    print(f"  Periods: {data['bookmarks_per_period']['periods']}")
    print(f"  Counts:  {data['bookmarks_per_period']['counts']}")

    # Test 2: Asia/Kolkata
    print("\n2. Querying in Asia/Kolkata...")
    params = {
        "timezone": "Asia/Kolkata",
        "start_date": start_date,
        "end_date": end_date
    }
    response = requests.get(f"{BASE_URL}/analytics/stats", params=params, headers=headers)
    data = response.json()
    
    print(f"  Periods: {data['bookmarks_per_period']['periods']}")
    print(f"  Counts:  {data['bookmarks_per_period']['counts']}")
    
    # Analyze
    # We expect some counts to shift from one day to another, or at least appear.
    # If counts are all 0 in IST, then something is wrong with the query.

if __name__ == "__main__":
    test_timezone_diagnostic()
