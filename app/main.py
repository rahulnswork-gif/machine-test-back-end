"""
Main application entry point.
Configures FastAPI application, CORS, and API routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.core.config import settings
from app.api.v1.api import api_router

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="""
## GitHub Repository Bookmark Manager API

A comprehensive backend application for managing GitHub repository bookmarks with user authentication and analytics.

### Features

* **Authentication**: Secure JWT-based user registration and login
* **GitHub Integration**: Search users, repositories, and view detailed information
* **Bookmark Management**: Save, organize, and manage your favorite GitHub repositories
* **CSV Import**: Bulk import repositories from CSV files with validation
* **Analytics**: Track your bookmarking activity over time

### Authentication

Most endpoints require authentication. To use them:

1. Register a new account using `/api/v1/auth/register`
2. Login using `/api/v1/auth/login` to get your JWT token
3. Click the **Authorize** button (🔒) at the top right
4. Enter your token in the format: `Bearer <your_token>`
5. Click **Authorize** and then **Close**

Now you can test all protected endpoints!

### GitHub API

This application uses the official GitHub REST API. You can use advanced search queries:

**User Search Examples:**
- `location:india` - Users in India
- `followers:>1000` - Users with 1000+ followers
- `language:python` - Users who code in Python

**Repository Search Examples:**
- `language:python stars:>1000` - Popular Python repos
- `fastapi` - Search for FastAPI related repos
- `topic:machine-learning` - ML repositories

### Rate Limits

- **Without GitHub Token**: 60 requests/hour
- **With GitHub Token**: 5,000 requests/hour

Configure your GitHub token in the `.env` file to increase limits.
        """,
        routes=app.routes,
        contact={
            "name": "Mozilor Machine Test",
            "url": "http://localhost:8000",
        },
        license_info={
            "name": "MIT",
        }
    )
    
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set custom OpenAPI schema
app.openapi = custom_openapi

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Root"])
def read_root():
    """
    Welcome endpoint - Returns a welcome message and API information.
    
    This is the root endpoint of the API. Use `/docs` for Swagger UI documentation.
    """
    return {
        "message": "Welcome to Mozilor Machine Test Backend",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0"
    }
