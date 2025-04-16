import logging
import requests
import pandas as pd
from datetime import datetime
from calendar import monthrange
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from src.settings import API_URL, HEADERS, STATES, COLUMNS

logging.basicConfig(level=logging.INFO)


def fetch_death_data_by_years(
    years: List[int],
    states: List[str] = STATES,
    max_workers: int = 10,
    timeout: int = 10,
) -> pd.DataFrame:

    now = datetime.now()

    def valid_month(year: int, month: int) -> bool:
        return (year < now.year) or (year == now.year and month <= now.month)

    def build_tasks(years: List[int]) -> List[tuple]:
        return [
            (state, year, month)
            for year in years
            for month in range(1, 13)
            if valid_month(year, month)
            for state in states
        ]

    def fetch_one_month(state: str, year: int, month: int) -> List[List]:
        last_day = monthrange(year, month)[1]
        start = f"{year}-{month:02d}-01"
        end = f"{year}-{month:02d}-{last_day}"
        url = f"{API_URL}?start_date={start}&end_date={end}&state={state}"

        try:
            res = requests.get(url, headers=HEADERS, timeout=timeout)
            res.raise_for_status()
            data = res.json().get("data", [])
            logging.info(f"[{state}] {year}-{month:02d}: {len(data)} registros")
            return [[year, month, state, d["name"], d["total"]] for d in data]
        except Exception as e:
            logging.warning(f"[{state}] {year}-{month:02d} - erro na API: {e}")
            return []

    tasks = build_tasks(years)
    all_data = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(fetch_one_month, s, y, m): (s, y, m) for s, y, m in tasks
        }
        for future in as_completed(future_map):
            result = future.result()
            if result:
                all_data.extend(result)

    df = pd.DataFrame(all_data, columns=COLUMNS)
    logging.info(f"[✓] Total records collected: {len(df)}")
    return df
