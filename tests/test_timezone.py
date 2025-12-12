import requests
import json
from datetime import datetime, timedelta
import pytz

BASE_URL = "http://localhost:8000/api/v1"

def test_timezone_support():
    print("=" * 70)
    print("TIMEZONE SUPPORT TEST")
    print("=" * 70)
    
    # Login
    print("\n1. Logging in...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "testuser@example.com", "password": "securepass123"}
    )
    if response.status_code != 200:
        print(f"✗ Login failed: {response.text}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Login successful")
    
    # Test Case 1: UTC (Default)
    print("\n2. Testing UTC Timezone...")
    params = {"timezone": "UTC"}
    response = requests.get(f"{BASE_URL}/analytics/stats", params=params, headers=headers)
    data = response.json()
    
    print(f"  Timezone: {data['bookmarks_per_period']['timezone']}")
    print(f"  Periods (Last 3): {data['bookmarks_per_period']['periods'][-3:]}")
    print(f"  Counts (Last 3): {data['bookmarks_per_period']['counts'][-3:]}")

    # Test Case 2: Asia/Kolkata (IST)
    print("\n3. Testing Asia/Kolkata Timezone...")
    params = {"timezone": "Asia/Kolkata"}
    response = requests.get(f"{BASE_URL}/analytics/stats", params=params, headers=headers)
    
    if response.status_code != 200:
        print(f"✗ Failed: {response.text}")
    else:
        data = response.json()
        print(f"  Timezone: {data['bookmarks_per_period']['timezone']}")
        print(f"  Periods (Last 3): {data['bookmarks_per_period']['periods'][-3:]}")
        print(f"  Counts (Last 3): {data['bookmarks_per_period']['counts'][-3:]}")
        
        # Check if counts differ or shift
        # Note: Depending on the time of day, a bookmark might shift from one day to another
        # e.g. 2025-12-11 22:00 UTC is 2025-12-12 03:30 IST
        
    # Test Case 3: Invalid Timezone
    print("\n4. Testing Invalid Timezone...")
    params = {"timezone": "Invalid/Timezone"}
    response = requests.get(f"{BASE_URL}/analytics/stats", params=params, headers=headers)
    
    if response.status_code == 400:
        print("✓ Correctly handled invalid timezone")
    else:
        print(f"✗ Failed to handle invalid timezone: {response.status_code}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_timezone_support()
