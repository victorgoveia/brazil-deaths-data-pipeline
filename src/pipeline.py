from src.api_client import fetch_death_data_by_years
from src.transform import transform_data
from src.loader import send_to_postgres


def run_pipeline():
    print("\n🚀 Iniciando pipeline de dados...")
    df = fetch_death_data_by_years([2025])
    df = transform_data(df)
    send_to_postgres(df)
    print("✅ Pipeline finalizada com sucesso.")
