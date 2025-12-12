import requests
import json
import time
import random

BASE_URL = "http://localhost:8000/api/v1"

def test_timezone_shift():
    print("=" * 70)
    print("TIMEZONE SHIFT TEST")
    print("=" * 70)
    
    # Login
    print("\n1. Logging in...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "testuser@example.com", "password": "securepass123"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Login successful")
    
    # Create a new bookmark "now"
    # Current time is ~03:00 IST on 12th, which is ~21:30 UTC on 11th.
    print("\n2. Creating a new bookmark...")
    repo_id = random.randint(100000, 999999)
    new_repo = {
        "repo_id": repo_id,
        "name": f"timezone-test-{repo_id}",
        "full_name": f"test/timezone-test-{repo_id}",
        "html_url": "https://github.com/test/timezone-test",
        "description": "Timezone test repo",
        "owner_login": "testuser",
        "owner_avatar_url": "https://example.com/avatar.png"
    }
    
    requests.post(f"{BASE_URL}/bookmarks/", json=new_repo, headers=headers)
    print("✓ Bookmark created")
    
    # Test 1: Query in UTC
    # Should show up on 11th (yesterday) or 12th depending on exact time, 
    # but definitely different from IST if near midnight.
    # Actually, if it's 21:30 UTC on 11th, it MUST be on 11th in UTC.
    print("\n3. Querying in UTC...")
    params = {"timezone": "UTC"}
    response = requests.get(f"{BASE_URL}/analytics/stats", params=params, headers=headers)
    data = response.json()
    
    periods = data['bookmarks_per_period']['periods']
    counts = data['bookmarks_per_period']['counts']
    
    # Find count for 11th and 12th
    count_11_utc = 0
    count_12_utc = 0
    if "11-12-2025" in periods:
        count_11_utc = counts[periods.index("11-12-2025")]
    if "12-12-2025" in periods:
        count_12_utc = counts[periods.index("12-12-2025")]
        
    print(f"  UTC Counts -> 11th: {count_11_utc}, 12th: {count_12_utc}")

    # Test 2: Query in Asia/Kolkata
    # Should show up on 12th (today).
    print("\n4. Querying in Asia/Kolkata...")
    params = {"timezone": "Asia/Kolkata"}
    response = requests.get(f"{BASE_URL}/analytics/stats", params=params, headers=headers)
    data = response.json()
    
    periods = data['bookmarks_per_period']['periods']
    counts = data['bookmarks_per_period']['counts']
    
    count_11_ist = 0
    count_12_ist = 0
    if "11-12-2025" in periods:
        count_11_ist = counts[periods.index("11-12-2025")]
    if "12-12-2025" in periods:
        count_12_ist = counts[periods.index("12-12-2025")]
        
    print(f"  IST Counts -> 11th: {count_11_ist}, 12th: {count_12_ist}")
    
    # Verification
    # In UTC, the new bookmark is on 11th.
    # In IST, the new bookmark is on 12th.
    # So count_12_ist should be > count_12_utc (or count_11_utc > count_11_ist)
    
    if count_12_ist > count_12_utc:
        print("\n✓ SUCCESS: Bookmark shifted to 12th in IST as expected!")
    elif count_11_utc > count_11_ist:
         print("\n✓ SUCCESS: Bookmark present on 11th in UTC but moved in IST!")
    else:
        print("\n✗ FAILURE: No timezone shift detected.")

if __name__ == "__main__":
    test_timezone_shift()
