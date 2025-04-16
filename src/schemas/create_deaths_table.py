from sqlalchemy import text

def create_deaths_table(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS deaths (
            id SERIAL PRIMARY KEY,
            city_id INTEGER REFERENCES cities(id) ON DELETE CASCADE,
            year_id INTEGER REFERENCES years(id) ON DELETE CASCADE,
            month INT NOT NULL CHECK (month >= 1 AND month <= 12),
            quantity INT NOT NULL,
            UNIQUE(city_id, year_id, month)
        );
    """))
