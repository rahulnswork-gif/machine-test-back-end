import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.core.config import settings

def create_database():
    # Connect to default 'postgres' db to create the new db
    # Construct DSN for default db
    default_db_url = settings.DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
    
    try:
        # Parse the URL to get params for psycopg2
        # This is a bit hacky, better to use sqlalchemy URL parsing or just manual string manipulation if simple
        # Assuming format: postgresql://user:pass@host/db
        
        # Let's just use the parts from settings directly if possible, but settings.DATABASE_URL is built from them.
        # Actually settings has individual fields too.
        
        conn = psycopg2.connect(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            dbname='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        db_name = settings.POSTGRES_DB
        
        # Check if db exists
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cur.fetchone()
        
        if not exists:
            print(f"Creating database {db_name}...")
            cur.execute(f"CREATE DATABASE {db_name}")
            print(f"Database {db_name} created successfully.")
        else:
            print(f"Database {db_name} already exists.")
            
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error creating database: {e}")
        exit(1)

if __name__ == "__main__":
    create_database()
