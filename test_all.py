import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_all():
    print("=" * 50)
    print("COMPREHENSIVE API TEST")
    print("=" * 50)
    
    # 1. Register
    email = "testuser@example.com"
    password = "securepass123"
    
    print("\n1. Testing Registration...")
    response = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    if response.status_code == 200:
        print("✓ Registration successful")
    elif response.status_code == 400 and "already exists" in response.text:
        print("✓ User already exists")
    else:
        print(f"✗ Registration failed: {response.text}")
        return

    # 2. Login
    print("\n2. Testing Login...")
    response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✓ Login successful. Token: {token[:20]}...")
    else:
        print(f"✗ Login failed: {response.text}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Search GitHub Users
    print("\n3. Testing GitHub User Search...")
    response = requests.get(f"{BASE_URL}/github/search/users", params={"q": "tiangolo"}, headers=headers)
    if response.status_code == 200:
        print(f"✓ User Search successful. Found {response.json()['total_count']} users")
    else:
        print(f"✗ User Search failed: {response.text}")

    # 4. Search GitHub Repos
    print("\n4. Testing GitHub Repo Search...")
    response = requests.get(f"{BASE_URL}/github/search/repos", params={"q": "fastapi"}, headers=headers)
    if response.status_code == 200:
        print(f"✓ Repo Search successful. Found {response.json()['total_count']} repos")
        repo = response.json()['items'][0]
    else:
        print(f"✗ Repo Search failed: {response.text}")
        return

    # 5. Get User Repos
    print("\n5. Testing Get User Repos...")
    response = requests.get(f"{BASE_URL}/github/users/tiangolo/repos", headers=headers)
    if response.status_code == 200:
        print(f"✓ Get User Repos successful. Found {len(response.json())} repos")
    else:
        print(f"✗ Get User Repos failed: {response.text}")

    # 6. Add Bookmark
    print("\n6. Testing Add Bookmark...")
    bookmark_data = {
        "repo_id": repo['id'],
        "name": repo['name'],
        "full_name": repo['full_name'],
        "html_url": repo['html_url'],
        "description": repo['description'],
        "owner_login": repo['owner']['login'],
        "owner_avatar_url": repo['owner']['avatar_url']
    }
    
    response = requests.post(f"{BASE_URL}/bookmarks/", json=bookmark_data, headers=headers)
    if response.status_code == 200:
        print("✓ Add Bookmark successful")
        bookmark_id = response.json()['id']
    elif response.status_code == 400 and "already bookmarked" in response.text:
        print("✓ Bookmark already exists")
        list_resp = requests.get(f"{BASE_URL}/bookmarks/", headers=headers)
        bookmark_id = list_resp.json()[0]['id'] if list_resp.json() else None
    else:
        print(f"✗ Add Bookmark failed: {response.text}")
        bookmark_id = None

    # 7. List Bookmarks
    print("\n7. Testing List Bookmarks...")
    response = requests.get(f"{BASE_URL}/bookmarks/", headers=headers)
    if response.status_code == 200:
        print(f"✓ List Bookmarks successful. Count: {len(response.json())}")
    else:
        print(f"✗ List Bookmarks failed: {response.text}")

    # 8. Get Bookmark Stats
    print("\n8. Testing Bookmark Stats...")
    response = requests.get(f"{BASE_URL}/analytics/stats", headers=headers)
    if response.status_code == 200:
        stats = response.json()
        print(f"✓ Bookmark Stats successful. Dates: {len(stats['dates'])}, Total bookmarks: {sum(stats['counts'])}")
    else:
        print(f"✗ Bookmark Stats failed: {response.text}")

    # 9. Import CSV
    print("\n9. Testing Import CSV...")
    csv_content = "owner,repo\ntiangolo,fastapi\npallets,flask"
    files = {'file': ('bookmarks.csv', csv_content, 'text/csv')}
    
    response = requests.post(f"{BASE_URL}/bookmarks/import", files=files, headers=headers)
    if response.status_code == 200:
        print(f"✓ Import CSV successful. Added: {len(response.json())}")
    else:
        print(f"✗ Import CSV failed: {response.text}")

    # 10. Remove Bookmark
    if bookmark_id:
        print("\n10. Testing Remove Bookmark...")
        response = requests.delete(f"{BASE_URL}/bookmarks/{bookmark_id}", headers=headers)
        if response.status_code == 200:
            print("✓ Remove Bookmark successful")
        else:
            print(f"✗ Remove Bookmark failed: {response.text}")

    print("\n" + "=" * 50)
    print("TEST COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    test_all()
