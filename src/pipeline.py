from src.api_client import run_data_collection
from src.transform import transform_data
from src.loader import send_to_postgres


def run_pipeline():
    print("\n🚀 Iniciando pipeline de dados...")
    df = run_data_collection(formato="csv")
    df = transform_data(df)
    send_to_postgres(df)
    print("✅ Pipeline finalizada com sucesso.")
