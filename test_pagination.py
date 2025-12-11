import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_pagination():
    print("=" * 70)
    print("BOOKMARK PAGINATION TEST")
    print("=" * 70)
    
    # Login
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "testuser@example.com", "password": "securepass123"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Default Pagination
    print("\n1. Default Pagination (page=1, per_page=30):")
    response = requests.get(f"{BASE_URL}/bookmarks/", headers=headers)
    data = response.json()
    
    print(f"   Total: {data.get('total')}")
    print(f"   Page: {data.get('page')}")
    print(f"   Per Page: {data.get('per_page')}")
    print(f"   Data Count: {len(data.get('data', []))}")
    
    if 'data' in data and 'total' in data:
        print("✓ Response structure correct")
    else:
        print("✗ Response structure incorrect")
        
    # 2. Custom Pagination
    print("\n2. Custom Pagination (page=1, per_page=2):")
    params = {"page": 1, "per_page": 2}
    response = requests.get(f"{BASE_URL}/bookmarks/", params=params, headers=headers)
    data = response.json()
    
    print(f"   Total: {data.get('total')}")
    print(f"   Page: {data.get('page')}")
    print(f"   Per Page: {data.get('per_page')}")
    print(f"   Data Count: {len(data.get('data', []))}")
    
    if len(data.get('data', [])) <= 2:
        print("✓ Limit respected")
    else:
        print(f"✗ Limit ignored: {len(data.get('data', []))}")

    # 3. Page 2
    print("\n3. Page 2 (page=2, per_page=2):")
    params = {"page": 2, "per_page": 2}
    response = requests.get(f"{BASE_URL}/bookmarks/", params=params, headers=headers)
    data = response.json()
    
    print(f"   Page: {data.get('page')}")
    print(f"   Data Count: {len(data.get('data', []))}")

if __name__ == "__main__":
    test_pagination()
