from typing import Any, List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
import pandas as pd
import io

from app.api import deps
from app.models.user import User
from app.models.bookmark import Bookmark
from app.schemas.bookmark import BookmarkCreate, Bookmark as BookmarkSchema, PaginatedBookmarks
from app.services.github_service import github_service

router = APIRouter()

@router.post("/", response_model=BookmarkSchema)
def create_bookmark(
    *,
    db: Session = Depends(deps.get_db),
    bookmark_in: BookmarkCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    # Check if already bookmarked
    existing = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.repo_id == bookmark_in.repo_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Repository already bookmarked")
    
    bookmark = Bookmark(
        **bookmark_in.dict(),
        user_id=current_user.id
    )
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark

from sqlalchemy import or_

@router.get("/", response_model=PaginatedBookmarks)
def read_bookmarks(
    db: Session = Depends(deps.get_db),
    page: int = 1,
    per_page: int = 30,
    q: Optional[str] = Query(None, description="Search query"),
    sort_by: str = Query("created_at", description="Field to sort by (created_at, name, full_name)"),
    order: str = Query("desc", description="Sort order (asc, desc)"),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    # Calculate skip
    skip = (page - 1) * per_page
    
    # Base query
    query = db.query(Bookmark).filter(Bookmark.user_id == current_user.id)
    
    # Apply search filter if provided
    if q:
        search_filter = or_(
            Bookmark.name.ilike(f"%{q}%"),
            Bookmark.full_name.ilike(f"%{q}%"),
            Bookmark.description.ilike(f"%{q}%")
        )
        query = query.filter(search_filter)
    
    # Get total count (after filtering)
    total_count = query.count()
    
    # Apply sorting
    if order == "asc":
        sort_attr = getattr(Bookmark, sort_by, Bookmark.created_at).asc()
    else:
        sort_attr = getattr(Bookmark, sort_by, Bookmark.created_at).desc()
        
    # Get paginated results
    bookmarks = query.order_by(
        sort_attr
    ).offset(skip).limit(per_page).all()
    
    return {
        "total": total_count,
        "page": page,
        "per_page": per_page,
        "total_pages": (total_count + per_page - 1) // per_page if per_page > 0 else 0,
        "data": bookmarks
    }

@router.delete("/{bookmark_id}", response_model=BookmarkSchema)
def delete_bookmark(
    *,
    db: Session = Depends(deps.get_db),
    bookmark_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    bookmark = db.query(Bookmark).filter(
        Bookmark.id == bookmark_id,
        Bookmark.user_id == current_user.id
    ).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    db.delete(bookmark)
    db.commit()
    return bookmark

@router.post("/import", response_model=List[BookmarkSchema])
async def import_bookmarks(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    contents = await file.read()
    try:
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    except Exception:
        raise HTTPException(status_code=400, detail="Could not parse CSV file.")
    
    # Expected columns: owner, repo
    if 'owner' not in df.columns or 'repo' not in df.columns:
        raise HTTPException(status_code=400, detail="CSV must contain 'owner' and 'repo' columns.")
    
    added_bookmarks = []
    
    for _, row in df.iterrows():
        owner = row['owner']
        repo_name = row['repo']
        
        # Validate with GitHub API
        try:
            repo_data = await github_service.get_repository(owner, repo_name)
            if not repo_data:
                continue # Skip if not found
            
            # Check if already bookmarked
            existing = db.query(Bookmark).filter(
                Bookmark.user_id == current_user.id,
                Bookmark.repo_id == repo_data['id']
            ).first()
            if existing:
                continue
            
            bookmark = Bookmark(
                user_id=current_user.id,
                repo_id=repo_data['id'],
                name=repo_data['name'],
                full_name=repo_data['full_name'],
                html_url=repo_data['html_url'],
                description=repo_data.get('description'),
                owner_login=repo_data['owner']['login'],
                owner_avatar_url=repo_data['owner']['avatar_url']
            )
            db.add(bookmark)
            added_bookmarks.append(bookmark)
            
        except Exception as e:
            print(f"Error processing {owner}/{repo_name}: {e}")
            continue

    db.commit()
    for bm in added_bookmarks:
        db.refresh(bm)
        
    return added_bookmarks
