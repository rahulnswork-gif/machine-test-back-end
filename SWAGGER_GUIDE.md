# Swagger UI Testing Guide

## Accessing Swagger UI

The API documentation is available at: **http://localhost:8000/docs**

Alternative documentation (ReDoc): **http://localhost:8000/redoc**

## How to Test APIs Using Swagger UI

### Step 1: Register a New User

1. Navigate to http://localhost:8000/docs
2. Scroll to the **auth** section
3. Click on `POST /api/v1/auth/register` to expand it
4. Click the **Try it out** button
5. Edit the request body:
   ```json
   {
     "email": "your-email@example.com",
     "password": "your-secure-password"
   }
   ```
6. Click **Execute**
7. Check the response - you should see a 200 status code with your user details

### Step 2: Login to Get JWT Token

1. Click on `POST /api/v1/auth/login` to expand it
2. Click **Try it out**
3. Fill in the form data:
   - **username**: your-email@example.com (use email here)
   - **password**: your-secure-password
4. Click **Execute**
5. Copy the `access_token` from the response

### Step 3: Authorize Swagger UI

1. Click the **Authorize** button (🔒 icon) at the top right of the page
2. In the popup, paste your token in this format:
   ```
   Bearer <your_access_token>
   ```
   Example: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
3. Click **Authorize**
4. Click **Close**

Now all protected endpoints will automatically include your authentication token!

### Step 4: Test GitHub Endpoints

#### Search GitHub Users
1. Expand `GET /api/v1/github/search/users`
2. Click **Try it out**
3. Enter a query, for example:
   - `location:india` - Find users in India
   - `followers:>1000` - Users with 1000+ followers
4. Optionally set pagination: `per_page=10`, `page=1`
5. Click **Execute**
6. View the results showing GitHub users

#### Search GitHub Repositories
1. Expand `GET /api/v1/github/search/repos`
2. Click **Try it out**
3. Enter a query, for example:
   - `language:python stars:>5000` - Popular Python repos
   - `fastapi` - FastAPI related repos
4. Set sort options: `sort=stars`, `order=desc`
5. Click **Execute**
6. View the results showing repositories

#### Get User's Repositories
1. Expand `GET /api/v1/github/users/{username}/repos`
2. Click **Try it out**
3. Enter a username: `tiangolo`
4. Set parameters: `sort=updated`, `per_page=5`
5. Click **Execute**
6. View the user's repositories

#### Get User Profile
1. Expand `GET /api/v1/github/users/{username}`
2. Click **Try it out**
3. Enter a username: `tiangolo`
4. Click **Execute**
5. View detailed user profile with followers, repos, etc.

#### Get Repository Details
1. Expand `GET /api/v1/github/repos/{owner}/{repo}`
2. Click **Try it out**
3. Enter owner: `tiangolo`
4. Enter repo: `fastapi`
5. Click **Execute**
6. View detailed repository information

### Step 5: Test Bookmark Endpoints

#### Add a Bookmark
1. First, search for a repository to get its details
2. Expand `POST /api/v1/bookmarks/`
3. Click **Try it out**
4. Fill in the request body with repository details:
   ```json
   {
     "repo_id": 160919119,
     "name": "fastapi",
     "full_name": "tiangolo/fastapi",
     "html_url": "https://github.com/tiangolo/fastapi",
     "description": "FastAPI framework, high performance...",
     "owner_login": "tiangolo",
     "owner_avatar_url": "https://avatars.githubusercontent.com/u/1326112"
   }
   ```
5. Click **Execute**
6. Bookmark is created!

#### List Your Bookmarks
1. Expand `GET /api/v1/bookmarks/`
2. Click **Try it out**
3. Optionally set pagination: `skip=0`, `limit=10`
4. Click **Execute**
5. View all your bookmarked repositories

#### Import Bookmarks from CSV
1. Expand `POST /api/v1/bookmarks/import`
2. Click **Try it out**
3. Click **Choose File** and upload a CSV file with columns: `owner,repo`
   
   Example CSV content:
   ```csv
   owner,repo
   tiangolo,fastapi
   pallets,flask
   django,django
   ```
4. Click **Execute**
5. View the imported bookmarks (validated against GitHub API)

#### Delete a Bookmark
1. Expand `DELETE /api/v1/bookmarks/{bookmark_id}`
2. Click **Try it out**
3. Enter the bookmark ID (from the list bookmarks response)
4. Click **Execute**
5. Bookmark is deleted!

### Step 6: Test Analytics Endpoint

1. Expand `GET /api/v1/analytics/stats`
2. Click **Try it out**
3. Click **Execute**
4. View bookmark statistics showing:
   - Dates when bookmarks were created
   - Count of bookmarks per date
   - Data ready for graph plotting

## Features of the Enhanced Swagger UI

✅ **Comprehensive Documentation**: Detailed API description with usage examples
✅ **Interactive Testing**: Test all endpoints directly from the browser
✅ **Authentication Support**: Built-in authorization with JWT tokens
✅ **Request/Response Examples**: See example payloads for all endpoints
✅ **Parameter Validation**: Input validation with helpful error messages
✅ **Schema Definitions**: View all data models and their fields
✅ **Try It Out**: Execute real API calls and see live responses
✅ **Code Generation**: Generate client code in multiple languages

## Tips

- **Response Codes**: 
  - 200: Success
  - 400: Bad Request (validation error)
  - 401: Unauthorized (missing/invalid token)
  - 404: Not Found
  - 429: Rate Limit Exceeded
  - 500: Server Error

- **GitHub Rate Limits**:
  - Without token: 60 requests/hour
  - With token: 5,000 requests/hour
  - Add your GitHub token to `.env` file

- **Search Query Tips**:
  - Use `+` for spaces: `location:san+francisco`
  - Combine filters: `language:python stars:>1000`
  - Use comparison operators: `>`, `>=`, `<`, `<=`

## Alternative: ReDoc

For a different documentation view, visit: http://localhost:8000/redoc

ReDoc provides a cleaner, more readable documentation format with:
- Three-column layout
- Better organization
- Easier navigation
- Download OpenAPI spec

Both Swagger UI and ReDoc use the same OpenAPI specification!
