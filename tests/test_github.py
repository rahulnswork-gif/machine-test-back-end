import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_github():
    # Login first to get token
    email = "test@example.com"
    password = "password123"
    
    print("Logging in...")
    response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Search Users
    print("Testing User Search...")
    response = requests.get(f"{BASE_URL}/github/search/users", params={"q": "rahulsoman"}, headers=headers)
    if response.status_code == 200:
        print("User Search successful")
        print(f"Found {response.json()['total_count']} users")
    else:
        print(f"User Search failed: {response.text}")

    # Search Repos
    print("Testing Repo Search...")
    response = requests.get(f"{BASE_URL}/github/search/repos", params={"q": "fastapi"}, headers=headers)
    if response.status_code == 200:
        print("Repo Search successful")
        print(f"Found {response.json()['total_count']} repos")
    else:
        print(f"Repo Search failed: {response.text}")

    # Get User Repos
    print("Testing Get User Repos...")
    response = requests.get(f"{BASE_URL}/github/users/rahulsoman/repos", headers=headers)
    if response.status_code == 200:
        print("Get User Repos successful")
        print(f"Found {len(response.json())} repos")
    else:
        print(f"Get User Repos failed: {response.text}")

if __name__ == "__main__":
    test_github()
