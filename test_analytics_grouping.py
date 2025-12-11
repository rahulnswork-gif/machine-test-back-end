import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_analytics_grouping():
    print("=" * 70)
    print("ANALYTICS GROUPING TEST")
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
    
    # Test different groupings
    groupings = ["day", "week", "month", "year"]
    
    for group in groupings:
        print(f"\nTesting group_by={group}...")
        response = requests.get(f"{BASE_URL}/analytics/stats", params={"group_by": group}, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success for {group}")
            print(f"  Periods: {data['bookmarks_per_period']['periods']}")
            print(f"  Counts: {data['bookmarks_per_period']['counts']}")
            print(f"  Summary Group By: {data['summary']['group_by']}")
        else:
            print(f"✗ Failed for {group}: {response.text}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_analytics_grouping()
