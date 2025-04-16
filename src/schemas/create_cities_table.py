from sqlalchemy import text

def create_cities_table(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS cities (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            state_id INTEGER REFERENCES states(id),
            UNIQUE(name, state_id)
        );
    """))
