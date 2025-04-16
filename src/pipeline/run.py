import logging
from datetime import datetime

from src.schemas.create_all import create_all_tables
from src.populate.populate_all import populate_all_tables
from src.api_client import fetch_death_data_by_years
from src.transform import transform_data
from src.loader import send_to_postgres
from src.pipeline.control_logic import is_first_run, get_years_to_collect

logging.basicConfig(level=logging.INFO)


def run_pipeline():
    logging.info("🚀 Starting pipeline...")

    # 1. Criar tabelas
    create_all_tables()
    logging.info("✅ Tables created.")

    # 2. Verificar se é a primeira execução
    first_time = is_first_run()
    now = datetime.now()
    years = get_years_to_collect(first_time, now)

    # 3. Coletar dados da API
    df_raw = fetch_death_data_by_years(years)
    if df_raw.empty:
        logging.warning("⚠️ No data fetched from API.")
        return

    # 4. Popular tabelas de dimensão (estados, cidades, anos)
    populate_all_tables(df_raw)
    logging.info("✅ Dimension tables populated.")

    # 5. Transformar e carregar dados finais
    df_transformed = transform_data(df_raw)
    send_to_postgres(df_transformed)

    logging.info("✅ Pipeline completed successfully.")
