import pandas as pd


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Garante os tipos corretos e formata os valores para uso seguro no banco.
    """
    df = df.copy()

    df["Ano"] = df["Ano"].astype(int)
    df["Mês"] = df["Mês"].astype(int)
    df["Quantidade"] = df["Quantidade"].astype(int)

    df["Cidade"] = df["Cidade"].astype(str).str.strip().str.title()
    df["Estado"] = df["Estado"].astype(str).str.strip().str.upper()

    return df
