import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api/v1"

def test_refined_analytics():
    print("=" * 70)
    print("REFINED ANALYTICS TEST")
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
    
    # Test Case 1: Short range (<= 30 days) -> DD-MM-YYYY
    print("\n2. Testing Short Range (Last 7 days)...")
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)
    
    params = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    }
    
    response = requests.get(f"{BASE_URL}/analytics/stats", params=params, headers=headers)
    data = response.json()
    
    print(f"  Range: {params['start_date']} to {params['end_date']}")
    print(f"  Duration: {data['bookmarks_per_period']['duration_days']} days")
    print(f"  Label Format: {data['bookmarks_per_period']['label_format']}")
    print(f"  Periods (First 3): {data['bookmarks_per_period']['periods'][:3]}")
    print(f"  Counts (First 3): {data['bookmarks_per_period']['counts'][:3]}")
    
    if len(data['bookmarks_per_period']['periods']) == 7:
        print("✓ Correct number of periods (7 days)")
    else:
        print(f"✗ Incorrect periods: {len(data['bookmarks_per_period']['periods'])}")

    # Test Case 2: Medium range (> 30 days) -> MM-YYYY
    print("\n3. Testing Medium Range (Last 60 days)...")
    start_date = end_date - timedelta(days=60)
    params = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    }
    
    response = requests.get(f"{BASE_URL}/analytics/stats", params=params, headers=headers)
    data = response.json()
    
    print(f"  Range: {params['start_date']} to {params['end_date']}")
    print(f"  Duration: {data['bookmarks_per_period']['duration_days']} days")
    print(f"  Label Format: {data['bookmarks_per_period']['label_format']}")
    print(f"  Periods (Sample): {data['bookmarks_per_period']['periods'][:3]}")
    
    if data['bookmarks_per_period']['label_format'] == '%m-%Y':
        print("✓ Correct label format (MM-YYYY)")
    else:
        print(f"✗ Incorrect label format: {data['bookmarks_per_period']['label_format']}")

    # Test Case 3: Long range (> 365 days) -> YYYY
    print("\n4. Testing Long Range (Last 400 days)...")
    start_date = end_date - timedelta(days=400)
    params = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    }
    
    response = requests.get(f"{BASE_URL}/analytics/stats", params=params, headers=headers)
    data = response.json()
    
    print(f"  Range: {params['start_date']} to {params['end_date']}")
    print(f"  Duration: {data['bookmarks_per_period']['duration_days']} days")
    print(f"  Label Format: {data['bookmarks_per_period']['label_format']}")
    print(f"  Periods (Sample): {data['bookmarks_per_period']['periods'][:3]}")
    
    if data['bookmarks_per_period']['label_format'] == '%Y':
        print("✓ Correct label format (YYYY)")
    else:
        print(f"✗ Incorrect label format: {data['bookmarks_per_period']['label_format']}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_refined_analytics()
