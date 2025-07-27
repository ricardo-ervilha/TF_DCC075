import polars as pl

# dropa nans e nulls
def apply(df: pl.DataFrame):
    df = df.drop_nans()
    df = df.drop_nulls()
    return df