import requests
import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

from src.settings import API_URL, HEADERS, STATES, COLUMNS

logging.basicConfig(level=logging.INFO)


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
            logging.info(
                f"[{state}] {year}-{month:02d}: {len(data['data'])} registros encontrados."
            )
            return [
                [year, month, state, item["name"], item["total"]]
                for item in data["data"]
            ]
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao buscar dados para {state} ({year}-{month}): {e}")
    return []


def fetch_death_data_by_years(years):
    all_data = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(fetch_monthly_death_records, state, year, month): (
                state,
                year,
                month,
            )
            for year in years
            for month in range(1, 13)
            for state in STATES
        }

        for future in as_completed(futures):
            result = future.result()
            if result:
                all_data.extend(result)

    df = pd.DataFrame(all_data, columns=COLUMNS)
    logging.info(f"Total de registros coletados: {len(df)}")
    return df
