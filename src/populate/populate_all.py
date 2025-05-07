from src.populate.populate_states import populate_states
from src.populate.populate_cities import populate_cities
from src.populate.populate_years import populate_years
import logging


logging.basicConfig(level=logging.INFO)


def populate_all_tables(df):
    logging.info("🌐 Populating dimension tables...")
    populate_states()
    populate_cities(df)
    populate_years(df)
    logging.info("✅ Finished populating dimension tables.")
