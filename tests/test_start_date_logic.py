import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api/v1"

def test_start_date_logic():
    print("=" * 70)
    print("START DATE LOGIC TEST")
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
    
    # Test Case 1: No start_date provided (should default to user creation date)
    print("\n2. Testing Default Start Date (No start_date provided)...")
    
    # We expect the start date to be the user's creation date.
    # Since we don't know the exact creation date of 'testuser', we'll infer it from the response
    # or check if the duration is reasonable (likely > 0 days if user was created earlier)
    
    response = requests.get(f"{BASE_URL}/analytics/stats", headers=headers)
    data = response.json()
    
    start_date_str = data['summary']['date_range']['start']
    end_date_str = data['summary']['date_range']['end']
    
    print(f"  Returned Range: {start_date_str} to {end_date_str}")
    print(f"  Duration: {data['bookmarks_per_period']['duration_days']} days")
    
    # Verify that start_date is NOT just 30 days ago (unless user was created exactly 30 days ago)
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    if start_date_str != thirty_days_ago:
        print(f"✓ Start date ({start_date_str}) is likely the user creation date (different from 30 days ago: {thirty_days_ago})")
    else:
        print(f"⚠ Start date is exactly 30 days ago. This might be coincidence or fallback logic.")

    # Test Case 2: Explicit start_date provided
    print("\n3. Testing Explicit Start Date...")
    explicit_start = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    params = {"start_date": explicit_start}
    
    response = requests.get(f"{BASE_URL}/analytics/stats", params=params, headers=headers)
    data = response.json()
    
    returned_start = data['summary']['date_range']['start']
    
    if returned_start == explicit_start:
        print(f"✓ Explicit start date respected: {returned_start}")
    else:
        print(f"✗ Explicit start date ignored. Expected {explicit_start}, got {returned_start}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_start_date_logic()
