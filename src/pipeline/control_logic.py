from sqlalchemy import create_engine, text
from datetime import datetime
from src.settings import get_database_url

def is_first_run() -> bool:
    engine = create_engine(get_database_url())
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM deaths"))
        count = result.scalar()
        return count == 0

def get_years_to_collect(first_run: bool, now: datetime) -> list[int]:
    return list(range(2015, now.year + 1)) if first_run else [now.year]

def get_months_to_collect(first_run: bool, now: datetime) -> list[int]:
    return list(range(1, now.month + 1)) if first_run else [now.month]
