from fastapi import APIRouter
from app.api.v1.endpoints import auth, github, bookmarks, analytics

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(github.router, prefix="/github", tags=["github"])
api_router.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
