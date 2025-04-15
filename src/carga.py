import pandas as pd
import psycopg2
import os

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from src.config import DB_CONFIG


def create_database_if_not_exists(dbname, user, password, host="localhost", port=5432):
    conn = psycopg2.connect(
        dbname="postgres", user=user, password=password, host=host, port=port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {dbname}")
        print(f">>> Banco de dados '{dbname}' criado.")
    else:
        print(f">>> Banco '{dbname}' já existe.")
    cur.close()
    conn.close()


def send_to_postgres(df: pd.DataFrame):
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", 5432)
    dbname = os.getenv("POSTGRES_DB")
    tabela = os.getenv("POSTGRES_TABLE", "mortalidade")

    create_database_if_not_exists(dbname, user, password, host, port)

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
    df.to_sql(tabela, con=engine, if_exists="append", index=False)
    print(f">>> Dados inseridos em '{tabela}' com sucesso.")
