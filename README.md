# FastAPI Backend - README

## Overview
A complete FastAPI backend application for managing GitHub repository bookmarks with user authentication, GitHub API integration, and analytics.

## Features
- ✅ User registration and JWT authentication
- ✅ GitHub user and repository search
- ✅ Bookmark management (add, list, remove)
- ✅ CSV import with validation
- ✅ Bookmark statistics/analytics
- ✅ PostgreSQL database with Alembic migrations
- ✅ Comprehensive API documentation (Swagger/ReDoc)

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL

### Installation

1. **Clone and navigate to project:**
   ```bash
   cd machine-test-back-end
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   - Copy `.env` and update with your PostgreSQL credentials
   - Optionally add `GITHUB_TOKEN` for higher API rate limits

4. **Initialize database:**
   ```bash
   python3 init_db.py
   alembic upgrade head
   ```

5. **Run server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

6. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token

### GitHub Integration
- `GET /api/v1/github/search/users?q={query}` - Search GitHub users
- `GET /api/v1/github/search/repos?q={query}` - Search repositories
- `GET /api/v1/github/users/{username}/repos` - Get user's repositories

### Bookmarks
- `POST /api/v1/bookmarks/` - Add bookmark
- `GET /api/v1/bookmarks/` - List bookmarks
- `DELETE /api/v1/bookmarks/{id}` - Remove bookmark
- `POST /api/v1/bookmarks/import` - Import from CSV

### Analytics
- `GET /api/v1/analytics/stats` - Get bookmark statistics

## Testing

Run comprehensive tests:
```bash
python3 test_all.py
```

## Project Structure
```
app/
├── api/v1/endpoints/    # API route handlers
├── core/                # Config & security
├── db/                  # Database setup
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── services/            # External services (GitHub)
└── main.py              # App entry point
```

## Tech Stack
- **FastAPI** - Modern web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Alembic** - Migrations
- **JWT** - Authentication
- **Pydantic** - Validation
- **httpx** - Async HTTP client

## License
MIT
