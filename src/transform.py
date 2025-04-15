import pandas as pd


def transform_data(df):
    df["Ano"] = df["Ano"].astype(int)
    df["Mês"] = df["Mês"].astype(int)
    df["Quantidade"] = df["Quantidade"].astype(int)
    df["Cidade"] = df["Cidade"].astype(str)
    df["Estado"] = df["Estado"].astype(str)
    return df
