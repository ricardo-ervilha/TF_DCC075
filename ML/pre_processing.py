import pandas as pd
import numpy as np
from utils import stats_df

def apply(df: pd.DataFrame):
    print("Inicia pré-processamento.")
    stats_df(df)

    print("1) Remove duplicatas")
    df.drop_duplicates(inplace=True)
    df.dropna()
    stats_df(df)

    print("2) Substitui valores infinitos pelas medianas")
    df.replace([np.inf, -np.inf], np.nan, inplace = True)
    print("Quantidade de valores alterados: ", df.isna().sum().sum())
    med_bytes_sec = df["Flow Bytes/s"].median()
    med_packets_sec = df["Flow Packets/s"].median()

    print("3) Prenche nan")
    df.fillna({"Flow Bytes/s": med_bytes_sec}, inplace=True)
    df.fillna({"Flow Packets/s": med_packets_sec}, inplace=True)