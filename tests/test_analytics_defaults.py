import requests
import sys
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api/v1"

def test_analytics_defaults():
    # 1. Login
    email = "test_auth_enhanced@example.com"
    password = "password123"
    
    resp = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        sys.exit(1)
    
    access_token = resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    # 2. Call stats without start_date
    print("Calling /analytics/stats without start_date...")
    resp = requests.get(f"{BASE_URL}/analytics/stats", headers=headers)
    if resp.status_code != 200:
        print(f"Analytics failed: {resp.text}")
        sys.exit(1)
        
    data = resp.json()
    summary = data.get("summary", {})
    date_range = summary.get("date_range", {})
    
    print(f"Date Range: {date_range}")
    
    # Verify start_date is present (it should be user creation date)
    start_date_str = date_range.get("start")
    if not start_date_str:
        print("Error: start_date missing in response")
        sys.exit(1)
        
    print(f"Start Date (defaulted): {start_date_str}")
    
    # Verify label format
    bookmarks_data = data.get("bookmarks_per_period", {})
    label_format = bookmarks_data.get("label_format")
    duration_days = bookmarks_data.get("duration_days")
    
    print(f"Duration (days): {duration_days}")
    print(f"Label Format: {label_format}")
    
    # Check if label format matches duration logic
    expected_format = '%d-%m-%Y' # Default for short duration (user just created)
    if duration_days > 365:
        expected_format = '%Y'
    elif duration_days > 30:
        expected_format = '%m-%Y'
        
    if label_format == expected_format:
        print(f"SUCCESS: Label format '{label_format}' matches expected for duration {duration_days}")
    else:
        print(f"FAILURE: Label format '{label_format}' does not match expected '{expected_format}' for duration {duration_days}")

if __name__ == "__main__":
    test_analytics_defaults()
