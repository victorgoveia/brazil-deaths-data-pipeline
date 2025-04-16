import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

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
    """
    Conecta ao banco 'postgres' e cria o banco principal, se ele ainda não existir.
    """
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
        print(f">>> Banco de dados '{POSTGRES_DB}' criado.")
    else:
        print(f">>> Banco '{POSTGRES_DB}' já existe.")
    cur.close()
    conn.close()


def prepare_deaths_facts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte os dados brutos para o formato de fato (FKs) com city_id, year_id.
    """
    engine = create_engine(get_database_url())
    with engine.begin() as conn:
        # Mapeamento das dimensões
        city_rows = conn.execute(text("SELECT id, name, state_id FROM cities")).mappings().all()
        state_rows = conn.execute(text("SELECT id, uf FROM states")).mappings().all()
        year_rows = conn.execute(text("SELECT id, year FROM years")).mappings().all()

    # Dicionários para lookup
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


def send_to_postgres(df: pd.DataFrame):
    """
    Garante que o banco existe, transforma os dados e envia para a tabela 'deaths'.
    """
    create_database_if_not_exists()
    engine = create_engine(get_database_url())

    df_facts = prepare_deaths_facts(df)

    if df_facts.empty:
        print("⚠️ Nenhum dado a ser inserido na tabela de mortes.")
        return

    df_facts.to_sql(
        POSTGRES_TABLE, con=engine, if_exists="append", index=False, method="multi"
    )
    print(f">>> {len(df_facts)} registros inseridos em '{POSTGRES_TABLE}' com sucesso.")
