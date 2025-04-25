from sqlalchemy import create_engine, text
from src.settings import get_database_url


def populate_years(df):
    engine = create_engine(get_database_url())

    with engine.begin() as conn:
        anos_unicos = df["Ano"].dropna().astype(int).unique()

        for year in anos_unicos:
            conn.execute(text("""
                INSERT INTO years (year)
                VALUES (:year)
                ON CONFLICT (year) DO NOTHING;
            """), {"year": int(year)})
