from sqlalchemy import create_engine, text
from src.settings import get_database_url


def populate_cities(df):
    engine = create_engine(get_database_url())

    with engine.begin() as conn:

        state_map = {
            row["uf"]: row["id"]
            for row in conn.execute(text("SELECT id, uf FROM states")).mappings()
        }

        cities_seen = set()

        for _, row in df.iterrows():
            city = row["Cidade"].strip().title()
            uf = row["Estado"].strip().upper()
            key = (city, uf)

            if key in cities_seen:
                continue
            cities_seen.add(key)

            state_id = state_map.get(uf)
            if not state_id:
                continue

            conn.execute(
                text(
                    """
                INSERT INTO cities (name, state_id)
                VALUES (:city, :state_id)
                ON CONFLICT (name, state_id) DO NOTHING;
            """
                ),
                {"city": city, "state_id": state_id},
            )
