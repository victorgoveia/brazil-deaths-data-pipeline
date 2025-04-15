import pandas as pd
import psycopg2

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


def send_to_postgres(df, tabela="obitos_tratados"):
    conn_str = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    engine = create_engine(conn_str)
    df.to_sql(tabela, engine, if_exists="replace", index=False)
    print(f"✅ Tabela '{tabela}' atualizada no PostgreSQL com sucesso.")
