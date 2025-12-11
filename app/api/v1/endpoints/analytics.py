from typing import Any, List, Dict, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date, text, and_
from datetime import datetime, timedelta, date
import pandas as pd
import pytz

from app.api import deps
from app.models.user import User
from app.models.bookmark import Bookmark

router = APIRouter()

@router.get("/stats")
def get_bookmark_stats(
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    timezone: str = Query("UTC", description="Timezone for date grouping (e.g., 'UTC', 'Asia/Kolkata')"),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get bookmark statistics with date range filtering, zero-filling, and timezone support.
    
    Logic:
    1. Validate timezone.
    2. Filter by start_date and end_date (interpreted in the given timezone).
    3. Group by date in the given timezone.
    4. Fill missing dates with 0 counts.
    """
    
    # Validate timezone
    try:
        tz = pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        raise HTTPException(status_code=400, detail=f"Unknown timezone: {timezone}")
    
    # Default date range if not provided
    if not end_date:
        end_date = datetime.now(tz).date()
    
    # If start_date is not provided, default to user creation date
    if not start_date:
        if isinstance(current_user.created_at, datetime):
            # Convert user creation time to target timezone
            user_created_at = current_user.created_at
            if user_created_at.tzinfo is None:
                user_created_at = pytz.utc.localize(user_created_at)
            start_date = user_created_at.astimezone(tz).date()
        else:
            start_date = end_date - timedelta(days=30)
        
    # Calculate duration in days
    duration_days = (end_date - start_date).days
    
    # Determine label format based on duration
    if duration_days > 365:
        label_format = '%Y'
        freq = 'Y'
    elif duration_days > 30:
        label_format = '%m-%Y'
        freq = 'M'
    else:
        label_format = '%d-%m-%Y'
        freq = 'D'
    
    # 1. Query bookmarks within range (converting DB UTC time to target timezone)
    # Note: Bookmark.created_at is stored as timezone-aware timestamp (UTC) in Postgres
    
    # Create the timezone-aware date expression
    # func.timezone(timezone, col) converts timestamptz to timestamp without time zone in target timezone
    date_expr = cast(
        func.timezone(timezone, Bookmark.created_at),
        Date
    )
    
    query = db.query(
        date_expr.label('date'),
        func.count(Bookmark.id).label('count')
    ).filter(
        and_(
            Bookmark.user_id == current_user.id,
            date_expr >= start_date,
            date_expr <= end_date
        )
    ).group_by(
        date_expr
    ).order_by(
        date_expr
    )
    
    results = query.all()
    
    # Convert DB results to dictionary for easy lookup
    db_data = {r.date: r.count for r in results}
    
    # 2. Generate complete date range and fill zeros
    full_date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    processed_data = {}
    
    for dt in full_date_range:
        d_date = dt.date()
        count = db_data.get(d_date, 0)
        
        label = dt.strftime(label_format)
        
        if label not in processed_data:
            processed_data[label] = 0
        processed_data[label] += count
            
    # Convert to lists for response
    labels = list(processed_data.keys())
    counts = list(processed_data.values())
    
    # 3. Repositories per owner (within date range)
    repos_per_owner = db.query(
        Bookmark.owner_login.label('owner'),
        func.count(Bookmark.id).label('count')
    ).filter(
        and_(
            Bookmark.user_id == current_user.id,
            date_expr >= start_date,
            date_expr <= end_date
        )
    ).group_by(
        Bookmark.owner_login
    ).order_by(
        func.count(Bookmark.id).desc()
    ).all()
    
    data = {
        "bookmarks_per_period": {
            "periods": labels,
            "counts": counts,
            "label_format": label_format,
            "duration_days": duration_days,
            "timezone": timezone
        },
        "repos_per_owner": {
            "owners": [r.owner for r in repos_per_owner],
            "counts": [r.count for r in repos_per_owner]
        },
        "summary": {
            "total_bookmarks": sum(counts),
            "total_owners": len(repos_per_owner),
            "date_range": {
                "start": start_date.strftime('%Y-%m-%d'),
                "end": end_date.strftime('%Y-%m-%d')
            },
            "timezone": timezone
        }
    }
    
    return data
