import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_auth():
    # Register
    email = "test@example.com"
    password = "password123"
    
    print("Testing Registration...")
    response = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    if response.status_code == 200:
        print("Registration successful")
    elif response.status_code == 400 and "already exists" in response.text:
        print("User already exists, proceeding to login")
    else:
        print(f"Registration failed: {response.text}")
        return

    # Login
    print("Testing Login...")
    response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"Login successful. Token: {token[:10]}...")
    else:
        print(f"Login failed: {response.text}")

if __name__ == "__main__":
    test_auth()
