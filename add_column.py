from sqlalchemy import create_engine, text
from app.core.config import settings

def add_created_at_column():
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        try:
            # Check if column exists
            result = conn.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name='created_at'"
            ))
            if result.fetchone():
                print("Column 'created_at' already exists.")
            else:
                print("Adding 'created_at' column to 'users' table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()"))
                conn.commit()
                print("Column added successfully.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    add_created_at_column()
