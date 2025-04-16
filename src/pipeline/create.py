import logging
from src.schemas.create_all import create_all_tables
from src.populate.populate_all import populate_all_tables

logging.basicConfig(level=logging.INFO)

def initialize_database(df):
    logging.info("🔧 Initializing database schema and dimensions...")
    create_all_tables()
    populate_all_tables(df)
    logging.info("✅ Database initialization complete.")
