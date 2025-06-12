import pandas as pd
import numpy as np

import scipy.stats

df = pd.read_csv("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\final_dataset.csv")

df_single_year = df[df["Year"] == 2023].copy()
df_single_year = df_single_year.drop(columns=["Year"])

# Convert relevant columns to numeric if needed
numeric_cols = [
    'Defence budget per capita', 'Defence budget % GDP', 'Active Armed Forces',
    'Population', 'GDP (2015 USD)', 'Unemployment rate',
    'Secondary education attainment rate', 'GDP per capita',
    'GDP per capita % change', 'Defence budget per capita % change',
    'Defence budget % GDP % change', 'Active Armed Forces per capita'
]

# Convert columns to numeric (in case of any string entries)
df_single_year[numeric_cols] = df_single_year[numeric_cols].apply(pd.to_numeric, errors='coerce')

df_single_year[numeric_cols] = df_single_year[numeric_cols].replace(0, np.nan)

# Drop rows with missing values
df_single_year_clean = df_single_year.dropna(subset=numeric_cols).copy()

log_cols = ['Active Armed Forces per capita', 'Active Armed Forces', 'Population', 'GDP (2015 USD)', 'GDP per capita', 'Defence budget per capita']
for col in log_cols:
    df_single_year_clean[f"log_{col}"] = np.log(df_single_year_clean[col])

# Alternative approach:
target = 'log_Active Armed Forces per capita'
results = {}

for col in df_single_year_clean.columns:
    if col != target and col != 'Country':
        # Drop missing values pairwise
        data = df_single_year_clean[[target, col]].dropna()
        if len(data) > 2:  # Ensure there's enough data to compute
            r, p = scipy.stats.pearsonr(data[target], data[col])
            results[col] = {'correlation': r, 'p-value': p}


results_df = pd.DataFrame(results).T
results_df = results_df.sort_values(by="correlation", ascending=False)
print(results_df)