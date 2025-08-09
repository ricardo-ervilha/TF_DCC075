import kagglehub
import os
import pandas as pd

def load(filenames: list):
    # Realiza o download do dataset (caso não tenha baixado), e o armazena em um .cache
    path = kagglehub.dataset_download("chethuhn/network-intrusion-dataset")

    # carrega os csv's    
    dfs = []
    for fn in filenames:
        filepath = os.path.join(path, fn)
        df = pd.read_csv(filepath)
        dfs.append(df)
    
    # uni tudo em um só
    dfs = pd.concat(dfs)
    return dfs
