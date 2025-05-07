from sqlalchemy import create_engine, text
from src.settings import get_database_url


STATES_DATA = [
    ("AC", "Acre", "Norte"),
    ("AL", "Alagoas", "Nordeste"),
    ("AM", "Amazonas", "Norte"),
    ("AP", "Amapá", "Norte"),
    ("BA", "Bahia", "Nordeste"),
    ("CE", "Ceará", "Nordeste"),
    ("DF", "Distrito Federal", "Centro-Oeste"),
    ("ES", "Espírito Santo", "Sudeste"),
    ("GO", "Goiás", "Centro-Oeste"),
    ("MA", "Maranhão", "Nordeste"),
    ("MT", "Mato Grosso", "Centro-Oeste"),
    ("MS", "Mato Grosso do Sul", "Centro-Oeste"),
    ("MG", "Minas Gerais", "Sudeste"),
    ("PA", "Pará", "Norte"),
    ("PB", "Paraíba", "Nordeste"),
    ("PR", "Paraná", "Sul"),
    ("PE", "Pernambuco", "Nordeste"),
    ("PI", "Piauí", "Nordeste"),
    ("RJ", "Rio de Janeiro", "Sudeste"),
    ("RN", "Rio Grande do Norte", "Nordeste"),
    ("RO", "Rondônia", "Norte"),
    ("RR", "Roraima", "Norte"),
    ("RS", "Rio Grande do Sul", "Sul"),
    ("SC", "Santa Catarina", "Sul"),
    ("SP", "São Paulo", "Sudeste"),
    ("SE", "Sergipe", "Nordeste"),
    ("TO", "Tocantins", "Norte"),
]


def populate_states():
    engine = create_engine(get_database_url())
    with engine.begin() as conn:
        for uf, name, region in STATES_DATA:
            conn.execute(
                text(
                    """
                INSERT INTO states (uf, name, region)
                VALUES (:uf, :name, :region)
                ON CONFLICT (uf) DO NOTHING;
            """
                ),
                {"uf": uf, "name": name, "region": region},
            )
