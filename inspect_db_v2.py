from sqlalchemy import create_engine, text
from app.core.config import settings

def inspect_data_v2():
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        # Get the last bookmark
        result = conn.execute(text("SELECT id FROM bookmarks ORDER BY id DESC LIMIT 1"))
        bookmark = result.fetchone()
        
        if not bookmark:
            return

        # Check correct conversion
        query = text("""
            SELECT 
                created_at,
                timezone('Asia/Kolkata', created_at) as correct_ist,
                cast(timezone('Asia/Kolkata', created_at) as date) as correct_ist_date
            FROM bookmarks 
            WHERE id = :id
        """)
        
        result = conn.execute(query, {"id": bookmark[0]}).fetchone()
        print(f"DB Raw: {result[0]}")
        print(f"Correct IST: {result[1]}")
        print(f"Correct IST Date: {result[2]}")

if __name__ == "__main__":
    inspect_data_v2()
