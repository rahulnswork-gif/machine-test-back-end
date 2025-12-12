import requests
import sys
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_bookmark_sorting():
    # 1. Login
    email = "test_auth_enhanced@example.com"
    password = "password123"
    
    resp = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        sys.exit(1)
    
    access_token = resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    print("Logged in successfully.")

    # 2. Populate Bookmarks (if empty)
    resp = requests.get(f"{BASE_URL}/bookmarks/", headers=headers)
    if resp.status_code != 200:
        print(f"Failed to get bookmarks: {resp.text}")
        sys.exit(1)
    bookmarks = resp.json().get('data', [])
    
    if len(bookmarks) < 3:
        print("Populating bookmarks...")
        repos_to_add = [
            {"repo_id": 1, "name": "alpha-repo", "full_name": "user/alpha-repo", "html_url": "http://github.com/user/alpha-repo", "owner_login": "user"},
            {"repo_id": 2, "name": "charlie-repo", "full_name": "user/charlie-repo", "html_url": "http://github.com/user/charlie-repo", "owner_login": "user"},
            {"repo_id": 3, "name": "bravo-repo", "full_name": "user/bravo-repo", "html_url": "http://github.com/user/bravo-repo", "owner_login": "user"},
        ]
        
        for repo in repos_to_add:
            try:
                requests.post(f"{BASE_URL}/bookmarks/", json=repo, headers=headers)
            except:
                pass # Ignore if already exists (or error)
        
        # Refresh list
        resp = requests.get(f"{BASE_URL}/bookmarks/", headers=headers)
        bookmarks = resp.json().get('data', [])

    print(f"Total Bookmarks: {len(bookmarks)}")

    # 3. Test Sort by Name ASC
    print("\nTesting Sort by Name ASC...")
    resp = requests.get(f"{BASE_URL}/bookmarks/?sort_by=name&order=asc", headers=headers)
    if resp.status_code != 200:
        print(f"Failed to get bookmarks: {resp.text}")
        sys.exit(1)
        
    bookmarks = resp.json().get('data', [])
    names = [b['name'] for b in bookmarks]
    print(f"Names: {names}")
    
    if names == sorted(names):
        print("SUCCESS: Bookmarks sorted by name ASC")
    else:
        print("FAILURE: Bookmarks NOT sorted by name ASC")

    # 4. Test Sort by Name DESC
    print("\nTesting Sort by Name DESC...")
    resp = requests.get(f"{BASE_URL}/bookmarks/?sort_by=name&order=desc", headers=headers)
    bookmarks = resp.json().get('data', [])
    names = [b['name'] for b in bookmarks]
    print(f"Names: {names}")
    
    if names == sorted(names, reverse=True):
        print("SUCCESS: Bookmarks sorted by name DESC")
    else:
        print("FAILURE: Bookmarks NOT sorted by name DESC")

    # 5. Test Sort by Created At (Default)
    print("\nTesting Sort by Created At (Default - DESC)...")
    resp = requests.get(f"{BASE_URL}/bookmarks/", headers=headers)
    bookmarks = resp.json().get('data', [])
    dates = [b['created_at'] for b in bookmarks]
    # print(f"Dates: {dates}")
    
    if dates == sorted(dates, reverse=True):
        print("SUCCESS: Bookmarks sorted by created_at DESC")
    else:
        print("FAILURE: Bookmarks NOT sorted by created_at DESC")

if __name__ == "__main__":
    test_bookmark_sorting()
