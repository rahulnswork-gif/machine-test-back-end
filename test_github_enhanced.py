import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_github_enhanced():
    print("=" * 60)
    print("ENHANCED GITHUB API TEST")
    print("=" * 60)
    
    # Login first to get token
    email = "testuser@example.com"
    password = "securepass123"
    
    print("\n1. Logging in...")
    response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    if response.status_code != 200:
        print(f"✗ Login failed: {response.text}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Login successful")
    
    # Test 1: Search Users with pagination
    print("\n2. Testing User Search with pagination...")
    response = requests.get(
        f"{BASE_URL}/github/search/users",
        params={"q": "location:india", "per_page": 5, "page": 1},
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✓ User Search successful")
        print(f"  Total count: {data.get('total_count', 0)}")
        print(f"  Returned: {len(data.get('items', []))}")
        if data.get('items'):
            print(f"  First user: {data['items'][0]['login']}")
    else:
        print(f"✗ User Search failed: {response.text}")

    # Test 2: Search Repos with filters
    print("\n3. Testing Repo Search with filters...")
    response = requests.get(
        f"{BASE_URL}/github/search/repos",
        params={
            "q": "language:python stars:>5000",
            "sort": "stars",
            "order": "desc",
            "per_page": 5
        },
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Repo Search successful")
        print(f"  Total count: {data.get('total_count', 0)}")
        print(f"  Returned: {len(data.get('items', []))}")
        if data.get('items'):
            repo = data['items'][0]
            print(f"  Top repo: {repo['full_name']} ({repo['stargazers_count']} stars)")
    else:
        print(f"✗ Repo Search failed: {response.text}")

    # Test 3: Get User Repos with sorting
    print("\n4. Testing Get User Repos with sorting...")
    response = requests.get(
        f"{BASE_URL}/github/users/tiangolo/repos",
        params={
            "type": "owner",
            "sort": "updated",
            "direction": "desc",
            "per_page": 5
        },
        headers=headers
    )
    if response.status_code == 200:
        repos = response.json()
        print(f"✓ Get User Repos successful")
        print(f"  Found {len(repos)} repos")
        if repos:
            print(f"  Most recent: {repos[0]['name']}")
    else:
        print(f"✗ Get User Repos failed: {response.text}")

    # Test 4: Get specific user profile
    print("\n5. Testing Get User Profile...")
    response = requests.get(
        f"{BASE_URL}/github/users/tiangolo",
        headers=headers
    )
    if response.status_code == 200:
        user = response.json()
        print(f"✓ Get User Profile successful")
        print(f"  Name: {user.get('name', 'N/A')}")
        print(f"  Public repos: {user.get('public_repos', 0)}")
        print(f"  Followers: {user.get('followers', 0)}")
    else:
        print(f"✗ Get User Profile failed: {response.text}")

    # Test 5: Get specific repository
    print("\n6. Testing Get Repository...")
    response = requests.get(
        f"{BASE_URL}/github/repos/tiangolo/fastapi",
        headers=headers
    )
    if response.status_code == 200:
        repo = response.json()
        print(f"✓ Get Repository successful")
        print(f"  Name: {repo['full_name']}")
        print(f"  Stars: {repo['stargazers_count']}")
        print(f"  Forks: {repo['forks_count']}")
        print(f"  Language: {repo['language']}")
        print(f"  Description: {repo['description'][:50]}...")
    else:
        print(f"✗ Get Repository failed: {response.text}")

    # Test 6: Test with non-existent user
    print("\n7. Testing error handling (non-existent user)...")
    response = requests.get(
        f"{BASE_URL}/github/users/thisuserdoesnotexist12345",
        headers=headers
    )
    if response.status_code == 404:
        print("✓ Error handling works correctly (404 returned)")
    else:
        print(f"✗ Unexpected response: {response.status_code}")

    print("\n" + "=" * 60)
    print("ENHANCED TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_github_enhanced()
