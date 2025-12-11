import httpx
from typing import Optional
from fastapi import HTTPException
from app.core.config import settings

GITHUB_API_URL = "https://api.github.com"

class GitHubService:
    def __init__(self):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        if settings.GITHUB_TOKEN:
            self.headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

    async def _make_request(self, url: str, params: Optional[dict] = None):
        """Make a request to GitHub API with proper error handling"""
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                response = await client.get(url, params=params, headers=self.headers)
                
                # Check rate limit
                if response.status_code == 403:
                    rate_limit_remaining = response.headers.get("X-RateLimit-Remaining", "0")
                    if rate_limit_remaining == "0":
                        reset_time = response.headers.get("X-RateLimit-Reset", "unknown")
                        raise HTTPException(
                            status_code=429,
                            detail=f"GitHub API rate limit exceeded. Resets at: {reset_time}"
                        )
                
                if response.status_code == 404:
                    return None
                    
                if response.status_code != 200:
                    error_detail = response.json().get("message", "GitHub API error") if response.text else "GitHub API error"
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"GitHub API error: {error_detail}"
                    )
                
                return response.json()
                
            except httpx.TimeoutException:
                raise HTTPException(status_code=504, detail="GitHub API request timeout")
            except httpx.RequestError as e:
                raise HTTPException(status_code=503, detail=f"GitHub API connection error: {str(e)}")

    async def search_users(
        self,
        query: str,
        page: int = 1,
        per_page: int = 30,
        sort: Optional[str] = None,
        order: Optional[str] = "desc"
    ):
        """
        Search for users on GitHub
        
        Args:
            query: Search query (e.g., "tom", "location:san+francisco")
            page: Page number (default: 1)
            per_page: Results per page, max 100 (default: 30)
            sort: Sort by 'followers', 'repositories', or 'joined' (default: best match)
            order: 'asc' or 'desc' (default: 'desc')
        """
        params = {
            "q": query,
            "page": page,
            "per_page": min(per_page, 100)
        }
        if sort:
            params["sort"] = sort
            params["order"] = order
            
        return await self._make_request(f"{GITHUB_API_URL}/search/users", params)

    async def search_repositories(
        self,
        query: str,
        page: int = 1,
        per_page: int = 30,
        sort: Optional[str] = None,
        order: Optional[str] = "desc"
    ):
        """
        Search for repositories on GitHub
        
        Args:
            query: Search query (e.g., "fastapi", "language:python stars:>1000")
            page: Page number (default: 1)
            per_page: Results per page, max 100 (default: 30)
            sort: Sort by 'stars', 'forks', 'help-wanted-issues', 'updated' (default: best match)
            order: 'asc' or 'desc' (default: 'desc')
        """
        params = {
            "q": query,
            "page": page,
            "per_page": min(per_page, 100)
        }
        if sort:
            params["sort"] = sort
            params["order"] = order
            
        return await self._make_request(f"{GITHUB_API_URL}/search/repositories", params)

    async def get_user_repositories(
        self,
        username: str,
        type: str = "owner",
        sort: str = "updated",
        direction: str = "desc",
        per_page: int = 30,
        page: int = 1
    ):
        """
        Get repositories for a specific user
        
        Args:
            username: GitHub username
            type: 'all', 'owner', 'member' (default: 'owner')
            sort: 'created', 'updated', 'pushed', 'full_name' (default: 'updated')
            direction: 'asc' or 'desc' (default: 'desc')
            per_page: Results per page, max 100 (default: 30)
            page: Page number (default: 1)
        """
        params = {
            "type": type,
            "sort": sort,
            "direction": direction,
            "per_page": min(per_page, 100),
            "page": page
        }
        
        return await self._make_request(f"{GITHUB_API_URL}/users/{username}/repos", params)
    
    async def get_repository(self, owner: str, repo: str):
        """
        Get a specific repository
        
        Args:
            owner: Repository owner username
            repo: Repository name
        """
        return await self._make_request(f"{GITHUB_API_URL}/repos/{owner}/{repo}")
    
    async def get_user(self, username: str):
        """
        Get a specific user's profile
        
        Args:
            username: GitHub username
        """
        return await self._make_request(f"{GITHUB_API_URL}/users/{username}")

github_service = GitHubService()
