import polars as pl

# dropa nans e nulls
def apply(df: pl.DataFrame):
    df = df.unique()
    return df