from sqlalchemy import create_engine
from src.settings import get_database_url
from src.schemas.create_states_table import create_states_table
from src.schemas.create_cities_table import create_cities_table
from src.schemas.create_years_table import create_years_table
from src.schemas.create_deaths_table import create_deaths_table
import logging

logging.basicConfig(level=logging.INFO)


def create_all_tables():
    engine = create_engine(get_database_url())

    with engine.begin() as conn:
        logging.info("🛠️ Creating tables...")
        create_states_table(conn)
        create_cities_table(conn)
        create_years_table(conn)
        create_deaths_table(conn)
        logging.info("✅ Tables successfully created.")
