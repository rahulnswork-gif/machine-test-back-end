import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_auth_flow():
    # 1. Register a new user (or login if exists)
    email = "test_auth_enhanced@example.com"
    password = "password123"
    
    print(f"Testing with user: {email}")
    
    # Try to register
    resp = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    if resp.status_code == 200:
        print("Registration successful")
    elif resp.status_code == 400 and "exists" in resp.text:
        print("User already exists, proceeding to login")
    else:
        print(f"Registration failed: {resp.text}")
        sys.exit(1)

    # 2. Login
    resp = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        sys.exit(1)
    
    tokens = resp.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    
    if not access_token or not refresh_token:
        print("Failed to get tokens")
        sys.exit(1)
        
    print("Login successful. Got access and refresh tokens.")
    print(f"Access Token: {access_token[:20]}...")
    print(f"Refresh Token: {refresh_token[:20]}...")

    # 3. Test Access Token
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(f"{BASE_URL}/bookmarks/", headers=headers)
    if resp.status_code != 200:
        print(f"Access token failed: {resp.text}")
        sys.exit(1)
    print("Access token works.")

    # 4. Test Refresh Token
    # Note: The refresh endpoint expects the refresh token in the Authorization header?
    # Let's check the code. Yes, depends(reusable_oauth2) which looks for Bearer token.
    refresh_headers = {"Authorization": f"Bearer {refresh_token}"}
    resp = requests.post(f"{BASE_URL}/auth/refresh", headers=refresh_headers)
    if resp.status_code != 200:
        print(f"Refresh failed: {resp.text}")
        sys.exit(1)
    
    new_tokens = resp.json()
    new_access_token = new_tokens.get("access_token")
    print("Refresh successful. Got new access token.")
    
    # 5. Test Logout
    # Logout using the *new* access token (or the old one, both should work to blacklist *that* token)
    # The requirement says "logout API". Usually this blacklists the *access* token so it can't be used anymore.
    # Let's blacklist the new access token.
    logout_headers = {"Authorization": f"Bearer {new_access_token}"}
    resp = requests.post(f"{BASE_URL}/auth/logout", headers=logout_headers)
    if resp.status_code != 200:
        print(f"Logout failed: {resp.text}")
        sys.exit(1)
    print("Logout successful.")
    
    # 6. Verify Blacklist
    # Try to use the blacklisted token
    resp = requests.get(f"{BASE_URL}/bookmarks/", headers=logout_headers)
    if resp.status_code == 401:
        print("Blacklisted token correctly rejected.")
    else:
        print(f"Error: Blacklisted token was accepted! Status: {resp.status_code}")
        sys.exit(1)

if __name__ == "__main__":
    test_auth_flow()
