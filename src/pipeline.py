from src.coleta import coletar_dados
from src.tratamento import tratar_dados
from src.loader import send_to_postgres

def executar_pipeline():
    print("\n🚀 Iniciando pipeline de dados...")
    df = coletar_dados(formato="csv")  # ou parquet
    df = tratar_dados(df)
    send_to_postgres(df)
    print("✅ Pipeline finalizada com sucesso.")
