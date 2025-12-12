import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_analytics():
    print("=" * 70)
    print("ANALYTICS ENDPOINT TEST")
    print("=" * 70)
    
    # Login
    print("\n1. Logging in...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "testuser@example.com", "password": "securepass123"}
    )
    if response.status_code != 200:
        print(f"✗ Login failed: {response.text}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Login successful")
    
    # Add some test bookmarks from different owners
    print("\n2. Adding test bookmarks from different owners...")
    test_repos = [
        {
            "repo_id": 123456,
            "name": "fastapi",
            "full_name": "tiangolo/fastapi",
            "html_url": "https://github.com/tiangolo/fastapi",
            "description": "FastAPI framework",
            "owner_login": "tiangolo",
            "owner_avatar_url": "https://avatars.githubusercontent.com/u/1326112"
        },
        {
            "repo_id": 234567,
            "name": "flask",
            "full_name": "pallets/flask",
            "html_url": "https://github.com/pallets/flask",
            "description": "Flask framework",
            "owner_login": "pallets",
            "owner_avatar_url": "https://avatars.githubusercontent.com/u/16748505"
        },
        {
            "repo_id": 345678,
            "name": "uvicorn",
            "full_name": "encode/uvicorn",
            "html_url": "https://github.com/encode/uvicorn",
            "description": "ASGI server",
            "owner_login": "encode",
            "owner_avatar_url": "https://avatars.githubusercontent.com/u/30841710"
        },
        {
            "repo_id": 456789,
            "name": "pydantic",
            "full_name": "pydantic/pydantic",
            "html_url": "https://github.com/pydantic/pydantic",
            "description": "Data validation",
            "owner_login": "pydantic",
            "owner_avatar_url": "https://avatars.githubusercontent.com/u/110818415"
        },
        {
            "repo_id": 567890,
            "name": "sqlalchemy",
            "full_name": "sqlalchemy/sqlalchemy",
            "html_url": "https://github.com/sqlalchemy/sqlalchemy",
            "description": "SQL toolkit",
            "owner_login": "sqlalchemy",
            "owner_avatar_url": "https://avatars.githubusercontent.com/u/1830384"
        }
    ]
    
    added_count = 0
    for repo in test_repos:
        response = requests.post(f"{BASE_URL}/bookmarks/", json=repo, headers=headers)
        if response.status_code == 200:
            added_count += 1
        elif "already bookmarked" in response.text:
            pass  # Already exists
    
    print(f"✓ Added {added_count} new bookmarks")
    
    # Get analytics
    print("\n3. Fetching analytics data...")
    response = requests.get(f"{BASE_URL}/analytics/stats", headers=headers)
    
    if response.status_code != 200:
        print(f"✗ Analytics failed: {response.text}")
        return
    
    data = response.json()
    print("✓ Analytics data retrieved successfully\n")
    
    # Display results
    print("=" * 70)
    print("ANALYTICS RESULTS")
    print("=" * 70)
    
    # Summary
    print("\n📊 SUMMARY")
    print(f"  Total Bookmarks: {data['summary']['total_bookmarks']}")
    print(f"  Total Owners: {data['summary']['total_owners']}")
    print(f"  Date Range: {data['summary']['date_range']['start']} to {data['summary']['date_range']['end']}")
    
    # Bookmarks per period
    print("\n📅 BOOKMARKS PER PERIOD")
    for period, count in zip(data['bookmarks_per_period']['periods'], data['bookmarks_per_period']['counts']):
        print(f"  {period}: {count} bookmark(s)")
    
    # Repositories per owner
    print("\n👤 REPOSITORIES PER OWNER (Total)")
    for owner, count in zip(data['repos_per_owner']['owners'], data['repos_per_owner']['counts']):
        print(f"  {owner}: {count} repo(s)")
    
    # Timeline data (Removed as it is not in the current API response)
    # print("\n📈 REPOSITORIES PER OWNER TIMELINE")
    # for item in data.get('repos_per_owner_timeline', []):
    #     print(f"  {item['date']} - {item['owner']}: {item['count']} repo(s)")
    
    print("\n" + "=" * 70)
    print("GRAPH DATA READY")
    print("=" * 70)
    print("\nThe API returns data in three formats:")
    print("1. bookmarks_per_period - Line/Bar chart of total bookmarks over time")
    print("2. repos_per_owner - Pie/Bar chart of repositories per owner")
    
    print("\n✅ Analytics endpoint is working correctly!")
    print("\nFull JSON Response:")
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    test_analytics()
