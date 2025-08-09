import pandas as pd
import numpy as np

# dropa nans, nulls e inf
def apply(df: pd.DataFrame):

    df.replace([np.inf, -np.inf], np.nan, inplace = True)
    print("Quantidade de valores alterados: ", df.isna().sum().sum())
    med_bytes_sec = df["Flow Bytes/s"].median()
    med_packets_sec = df[" Flow Packets/s"].median()
    df.fillna({"Flow Bytes/s": med_bytes_sec}, inplace=True)
    df.fillna({" Flow Packets/s": med_packets_sec}, inplace=True)