import pandas as pd
from sqlalchemy import create_engine
from src.config import DB_CONFIG

def send_to_postgres(df, tabela="obitos_tratados"):
    conn_str = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    engine = create_engine(conn_str)
    df.to_sql(tabela, engine, if_exists="replace", index=False)
    print(f"✅ Tabela '{tabela}' atualizada no PostgreSQL com sucesso.")
