import requests
import pandas as pd
import logging


from concurrent.futures import ThreadPoolExecutor, as_completed


from src.settings import API_URL, HEADERS, STATES, COLUMNS

logging.basicConfig(level=logging.INFO)


def get_date_range_for_month(year, month):
    start_date = f"{year}-{month:02d}-01"
    if month == 12:
        end_date = f"{year + 1}-01-01"
    else:
        end_date = f"{year}-{month + 1:02d}-01"
    return start_date, end_date


def fetch_monthly_death_records(state, year, month):
    start_date, end_date = get_date_range_for_month(year, month)
    url = f"{API_URL}?start_date={start_date}&end_date={end_date}&state={state}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "data" in data:
            logging.info(f"[{state}] {year}-{month:02d}: {len(data['data'])} registros")
            return [
                [year, month, state, item["name"], item["total"]]
                for item in data["data"]
            ]
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for {state} ({year}-{month}): {e}")
    return []


def fetch_death_data_by_years(years, months=None):
    all_data = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        if months is None:
            tasks = [
                executor.submit(fetch_monthly_death_records, state, year, month)
                for year in years
                for month in range(1, 13)
                for state in STATES
            ]
        else:
            tasks = [
                executor.submit(fetch_monthly_death_records, state, year, month)
                for year in years
                for month in months
                for state in STATES
            ]

        for future in as_completed(tasks):
            result = future.result()
            if result:
                all_data.extend(result)

    df = pd.DataFrame(all_data, columns=COLUMNS)
    logging.info(f"[✓] Total records collected: {len(df)}")
    return df
