#%%
from variables import filenames, features, target
from load_dataset import load
from pre_processing import apply
import polars as pl
import numpy as np
#%%
df = load(filenames)
df.head()
df.shape
#%%
df.duplicated().sum()
df.drop_duplicates(inplace=True)
#%%
df = apply(df, feature_select_set=features)
df_features = df[features]
df_target = df[target]
#%%
missing_val = df.isna().sum()
print(missing_val.loc[missing_val > 0])
# %%
numeric_cols = df.select_dtypes(include = np.number).columns
inf_count = np.isinf(df[numeric_cols]).sum()
print(inf_count[inf_count > 0])
#%%
print(f'Initial missing values: {df.isna().sum().sum()}')

df.replace([np.inf, -np.inf], np.nan, inplace = True)

print(f'Missing values after processing infinite values: {df.isna().sum().sum()}')

# %%
