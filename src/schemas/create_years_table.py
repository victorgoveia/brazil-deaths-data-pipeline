from sqlalchemy import text

def create_years_table(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS years (
            id SERIAL PRIMARY KEY,
            year INT UNIQUE NOT NULL
        );
    """))
