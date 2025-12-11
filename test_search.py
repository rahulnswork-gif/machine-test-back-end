import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_search():
    print("=" * 70)
    print("BOOKMARK SEARCH TEST")
    print("=" * 70)
    
    # Login
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "testuser@example.com", "password": "securepass123"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Search for 'fastapi' (should find something if we bookmarked fastapi related repos)
    # Or search for 'test' since we created 'timezone-test' earlier
    query = "test"
    print(f"\n1. Searching for '{query}'...")
    params = {"q": query}
    response = requests.get(f"{BASE_URL}/bookmarks/", params=params, headers=headers)
    data = response.json()
    
    print(f"   Total Found: {data.get('total')}")
    print(f"   Data Count: {len(data.get('data', []))}")
    
    for bm in data.get('data', []):
        print(f"   - {bm['full_name']}")
        if query.lower() in bm['full_name'].lower() or query.lower() in (bm.get('description') or '').lower():
            pass
        else:
            print("     ✗ Match not obvious in name/desc")

    # 2. Search for non-existent term
    query = "nonexistentterm12345"
    print(f"\n2. Searching for '{query}'...")
    params = {"q": query}
    response = requests.get(f"{BASE_URL}/bookmarks/", params=params, headers=headers)
    data = response.json()
    
    print(f"   Total Found: {data.get('total')}")
    
    if data.get('total') == 0:
        print("✓ Correctly found 0 results")
    else:
        print(f"✗ Found {data.get('total')} results, expected 0")

if __name__ == "__main__":
    test_search()
