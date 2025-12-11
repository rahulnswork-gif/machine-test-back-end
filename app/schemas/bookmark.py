from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class BookmarkBase(BaseModel):
    repo_id: int
    name: str
    full_name: str
    html_url: str
    description: Optional[str] = None
    owner_login: str
    owner_avatar_url: Optional[str] = None

class BookmarkCreate(BookmarkBase):
    pass

class Bookmark(BookmarkBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PaginatedBookmarks(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int
    data: list[Bookmark]
