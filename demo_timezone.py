import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def demonstrate_timezone_usage():
    print("=" * 70)
    print("TIMEZONE USAGE DEMO")
    print("=" * 70)
    
    # Login
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "testuser@example.com", "password": "securepass123"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Request WITHOUT timezone (Defaults to UTC)
    print("\n1. Request WITHOUT timezone (Defaults to UTC):")
    print("   GET /api/v1/analytics/stats")
    response = requests.get(f"{BASE_URL}/analytics/stats", headers=headers)
    data = response.json()
    
    periods = data['bookmarks_per_period']['periods']
    counts = data['bookmarks_per_period']['counts']
    tz = data['bookmarks_per_period']['timezone']
    
    # Get last 2 days
    print(f"   Response Timezone: {tz}")
    print(f"   Last 2 Days: {periods[-2:]}")
    print(f"   Counts:      {counts[-2:]}")
    
    # 2. Request WITH timezone (Asia/Kolkata)
    print("\n2. Request WITH timezone (Asia/Kolkata):")
    print("   GET /api/v1/analytics/stats?timezone=Asia/Kolkata")
    params = {"timezone": "Asia/Kolkata"}
    response = requests.get(f"{BASE_URL}/analytics/stats", params=params, headers=headers)
    data = response.json()
    
    periods = data['bookmarks_per_period']['periods']
    counts = data['bookmarks_per_period']['counts']
    tz = data['bookmarks_per_period']['timezone']
    
    print(f"   Response Timezone: {tz}")
    print(f"   Last 2 Days: {periods[-2:]}")
    print(f"   Counts:      {counts[-2:]}")
    
    print("\n" + "=" * 70)
    print("OBSERVATION")
    print("=" * 70)
    print("Notice how the counts shift when the timezone parameter is provided.")

if __name__ == "__main__":
    demonstrate_timezone_usage()
