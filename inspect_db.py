from sqlalchemy import create_engine, text
from app.core.config import settings

def inspect_data():
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        # Get the last bookmark
        result = conn.execute(text("SELECT id, created_at FROM bookmarks ORDER BY id DESC LIMIT 1"))
        bookmark = result.fetchone()
        
        if not bookmark:
            print("No bookmarks found.")
            return

        print(f"Last Bookmark ID: {bookmark[0]}")
        print(f"Raw created_at (Python): {bookmark[1]}")
        
        # Check DB timezone conversion
        query = text("""
            SELECT 
                created_at,
                timezone('UTC', created_at) as as_utc,
                timezone('Asia/Kolkata', timezone('UTC', created_at)) as as_ist,
                cast(timezone('Asia/Kolkata', timezone('UTC', created_at)) as date) as ist_date
            FROM bookmarks 
            WHERE id = :id
        """)
        
        result = conn.execute(query, {"id": bookmark[0]}).fetchone()
        print(f"DB Raw: {result[0]}")
        print(f"DB as UTC: {result[1]}")
        print(f"DB as IST: {result[2]}")
        print(f"DB IST Date: {result[3]}")

if __name__ == "__main__":
    inspect_data()
