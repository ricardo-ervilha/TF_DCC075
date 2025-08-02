import kagglehub
import polars as pl
import os

def load(filenames: list):
    # Realiza o download do dataset (caso não tenha baixado), e o armazena em um .cache
    path = kagglehub.dataset_download("chethuhn/network-intrusion-dataset")
    # print(path) # Descomente caso queira ver onde foi guardado.
    
    dfs = []
    for fn in filenames:
        filepath = os.path.join(path, fn)
        pldf = pl.read_csv(filepath, infer_schema_length=10000)
        pldf = pldf.rename({col: col.strip() for col in pldf.columns})
        dfs.append(pldf)
    
    dfs = pl.concat(dfs)
    
    return dfs