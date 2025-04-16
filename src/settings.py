import os
from dotenv import load_dotenv, find_dotenv

# Carregar variáveis do .env
load_dotenv(find_dotenv())

# ========================
# Configurações da API
# ========================
API_URL = "https://transparencia.registrocivil.org.br/api/record/death"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# ========================
# Constantes de Estados
# ========================
STATES = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
    "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RO", "RR", "RS", "SC",
    "SP", "SE", "TO"
]
# ========================
# Estrutura dos dados brutos
# ========================
COLUMNS = ["Ano", "Mês", "Estado", "Cidade", "Quantidade"]
# ========================
# Configurações de Banco de Dados
# ========================
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "pipeline")
POSTGRES_TABLE = os.getenv("POSTGRES_TABLE", "deaths")

def get_database_url() -> str:
    return f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
