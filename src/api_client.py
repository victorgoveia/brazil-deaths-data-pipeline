import requests
import pandas as pd
import os
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed


API_URL = "https://transparencia.registrocivil.org.br/api/record/death"
HEADERS = {"User-Agent": "Mozilla/5.0"}
STATES = [
    "AC",
    "AL",
    "AM",
    "AP",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RO",
    "RR",
    "RS",
    "SC",
    "SP",
    "SE",
    "TO",
]
YEARS = range(2020, 2026)
COLUMNS = ["Ano", "Mês", "Estado", "Cidade", "Quantidade"]


def get_date_range_for_month(year, month):
    start_date = datetime(year, month, 1)
    end_date = (
        datetime(year, month + 1, 1) - timedelta(days=1)
        if month < 12
        else datetime(year + 1, 1, 1) - timedelta(days=1)
    )
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def fetch_monthly_death_records(state, year, month):
    start_date, end_date = get_date_range_for_month(year, month)
    url = f"{API_URL}?start_date={start_date}&end_date={end_date}&state={state}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "data" in data:
            return [
                [year, month, state, item["name"], item["total"]]
                for item in data["data"]
            ]
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados para {state} ({year}-{month}): {e}")
    return []


def fetch_all_death_data():
    all_data = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(fetch_monthly_death_records, state, year, month): (
                state,
                year,
                month,
            )
            for year in YEARS
            for month in range(1, 13)
            for state in STATES
        }

        for future in as_completed(futures):
            result = future.result()
            if result:
                all_data.extend(result)

    return pd.DataFrame(all_data, columns=COLUMNS)


def run_data_collection(formato="csv", caminho_saida="data/raw/"):
    df = fetch_all_death_data()
    os.makedirs(caminho_saida, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"dados_obitos_{timestamp}.{formato}"
    caminho_completo = os.path.join(caminho_saida, nome_arquivo)

    if formato == "excel":
        df.to_excel(caminho_completo, index=False)
    elif formato == "csv":
        df.to_csv(caminho_completo, index=False, sep=";")
    else:
        df.to_parquet(caminho_completo, index=False)

    print(f"✅ Dados salvos com sucesso em {caminho_completo}")
    return df
