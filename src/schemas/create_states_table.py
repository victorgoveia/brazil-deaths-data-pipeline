from sqlalchemy import text

def create_states_table(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS states (
            id SERIAL PRIMARY KEY,
            uf CHAR(2) UNIQUE NOT NULL,
            name TEXT NOT NULL,
            region TEXT
        );
    """))
