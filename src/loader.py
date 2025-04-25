import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

from src.settings import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_TABLE,
    get_database_url,
)


def create_database_if_not_exists():
    conn = psycopg2.connect(
        dbname="postgres",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{POSTGRES_DB}'")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {POSTGRES_DB}")
        print(f">>> Database '{POSTGRES_DB}' created.")
    else:
        print(f">>> Database '{POSTGRES_DB}' already exists.")
    cur.close()
    conn.close()


def prepare_deaths_facts(df: pd.DataFrame) -> pd.DataFrame:
    engine = create_engine(get_database_url())
    with engine.begin() as conn:
        city_rows = conn.execute(text("SELECT id, name, state_id FROM cities")).mappings().all()
        state_rows = conn.execute(text("SELECT id, uf FROM states")).mappings().all()
        year_rows = conn.execute(text("SELECT id, year FROM years")).mappings().all()

    state_map = {r["uf"]: r["id"] for r in state_rows}
    city_map = {(r["name"].strip().title(), r["state_id"]): r["id"] for r in city_rows}
    year_map = {r["year"]: r["id"] for r in year_rows}

    facts = []
    for _, row in df.iterrows():
        uf = row["Estado"].strip().upper()
        city = row["Cidade"].strip().title()
        year = int(row["Ano"])
        month = int(row["Mês"])
        quantity = int(row["Quantidade"])

        state_id = state_map.get(uf)
        city_id = city_map.get((city, state_id))
        year_id = year_map.get(year)

        if city_id and year_id:
            facts.append(
                {
                    "city_id": city_id,
                    "year_id": year_id,
                    "month": month,
                    "quantity": quantity,
                }
            )

    return pd.DataFrame(facts)


def filter_existing_records(df_facts: pd.DataFrame, engine) -> pd.DataFrame:
    with engine.connect() as conn:
        existing = conn.execute(text(
            "SELECT city_id, year_id, month FROM deaths"
        )).fetchall()

    existing_keys = {(row[0], row[1], row[2]) for row in existing}

    filtered = df_facts[
        ~df_facts[["city_id", "year_id", "month"]]
        .apply(tuple, axis=1)
        .isin(existing_keys)
    ]

    return filtered


def send_to_postgres(df: pd.DataFrame):
    create_database_if_not_exists()
    engine = create_engine(get_database_url())
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    df_facts = prepare_deaths_facts(df)

    if df_facts.empty:
        print("⚠️ No data to be inserted into the deaths table.")
        return

    with engine.begin() as conn:
        delete_stmt = text("""
            DELETE FROM deaths
            WHERE year_id = :year_id AND month = :month
        """)

        year_row = conn.execute(
            text("SELECT id FROM years WHERE year = :year"),
            {"year": current_year}
        ).mappings().first()

        year_id = year_row["id"] if year_row else None

        if year_id:
            conn.execute(delete_stmt, {"year_id": year_id, "month": current_month})
            print(f">>> Existing records for {current_month:02d}/{current_year} removed before reinserting.")

    df_facts.to_sql(
        POSTGRES_TABLE, con=engine, if_exists="append", index=False, method="multi"
    )
    print(f">>> {len(df_facts)} records successfully inserted into '{POSTGRES_TABLE}'.")
