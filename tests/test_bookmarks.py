import requests
import csv
import io

BASE_URL = "http://localhost:8000/api/v1"

def test_bookmarks():
    # Login
    email = "test@example.com"
    password = "password123"
    
    print("Logging in...")
    response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Add Bookmark
    print("Testing Add Bookmark...")
    # Need a valid repo ID. Let's search first or just use a known one.
    # FastAPI repo ID is 160919119 (approx, let's search)
    search_resp = requests.get(f"{BASE_URL}/github/search/repos", params={"q": "fastapi"}, headers=headers)
    if search_resp.status_code != 200:
        print("Search failed, cannot add bookmark")
        return
    
    repo = search_resp.json()['items'][0]
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
        print("Add Bookmark successful")
        bookmark_id = response.json()['id']
    elif response.status_code == 400 and "already bookmarked" in response.text:
        print("Bookmark already exists")
        # Get list to find id
        list_resp = requests.get(f"{BASE_URL}/bookmarks/", headers=headers)
        data = list_resp.json().get('data', [])
        bookmark_id = data[0]['id'] if data else None
    else:
        print(f"Add Bookmark failed: {response.text}")
        return

    # List Bookmarks
    print("Testing List Bookmarks...")
    response = requests.get(f"{BASE_URL}/bookmarks/", headers=headers)
    if response.status_code == 200:
        data = response.json().get('data', [])
        print(f"List Bookmarks successful. Count: {len(data)}")
    else:
        print(f"List Bookmarks failed: {response.text}")

    # Remove Bookmark
    print("Testing Remove Bookmark...")
    response = requests.delete(f"{BASE_URL}/bookmarks/{bookmark_id}", headers=headers)
    if response.status_code == 200:
        print("Remove Bookmark successful")
    else:
        print(f"Remove Bookmark failed: {response.text}")

    # Import CSV
    print("Testing Import CSV...")
    csv_content = "owner,repo\ntiangolo,fastapi\nrahulsoman,portfolio"
    files = {'file': ('bookmarks.csv', csv_content, 'text/csv')}
    
    response = requests.post(f"{BASE_URL}/bookmarks/import", files=files, headers=headers)
    if response.status_code == 200:
        print(f"Import CSV successful. Added: {len(response.json())}")
    else:
        print(f"Import CSV failed: {response.text}")

if __name__ == "__main__":
    test_bookmarks()
