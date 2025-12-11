from typing import Any, Optional
from fastapi import APIRouter, Depends, Query
from app.api import deps
from app.models.user import User
from app.services.github_service import github_service

router = APIRouter()

@router.get("/search/users")
async def search_users(
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(30, ge=1, le=100, description="Results per page"),
    sort: Optional[str] = Query(None, regex="^(followers|repositories|joined)$", description="Sort field"),
    order: Optional[str] = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Search for GitHub users.
    
    Query examples:
    - `tom` - Search for users named tom
    - `location:san+francisco` - Users in San Francisco
    - `followers:>1000` - Users with more than 1000 followers
    """
    return await github_service.search_users(q, page, per_page, sort, order)

@router.get("/search/repos")
async def search_repos(
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(30, ge=1, le=100, description="Results per page"),
    sort: Optional[str] = Query(None, regex="^(stars|forks|help-wanted-issues|updated)$", description="Sort field"),
    order: Optional[str] = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Search for GitHub repositories.
    
    Query examples:
    - `fastapi` - Search for FastAPI repos
    - `language:python` - Python repositories
    - `stars:>1000` - Repos with more than 1000 stars
    - `language:python stars:>1000` - Combine filters
    """
    return await github_service.search_repositories(q, page, per_page, sort, order)

@router.get("/users/{username}/repos")
async def get_user_repos(
    username: str,
    type: str = Query("owner", regex="^(all|owner|member)$", description="Repository type"),
    sort: str = Query("updated", regex="^(created|updated|pushed|full_name)$", description="Sort field"),
    direction: str = Query("desc", regex="^(asc|desc)$", description="Sort direction"),
    per_page: int = Query(30, ge=1, le=100, description="Results per page"),
    page: int = Query(1, ge=1, description="Page number"),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get repositories for a specific GitHub user."""
    return await github_service.get_user_repositories(username, type, sort, direction, per_page, page)

@router.get("/users/{username}")
async def get_user(
    username: str,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get a specific GitHub user's profile."""
    result = await github_service.get_user(username)
    if not result:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.get("/repos/{owner}/{repo}")
async def get_repository(
    owner: str,
    repo: str,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get a specific GitHub repository."""
    result = await github_service.get_repository(owner, repo)
    if not result:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Repository not found")
    return result
