from variables import filenames, features, target
from load_dataset import load
from pre_processing import apply
import polars as pl

df = load(filenames[:2])
df = apply(df, feature_select_set=features)

df_features = df[features]
df_target = df[target]
