import pandas as pd
import statsmodels.stats.outliers_influence

CLEAN_DIR = "clean_data"

df = pd.read_csv(os.path.join(CLEAN_DIR, "final_dataset.csv"))

df['Year'] = df['Year'].astype(int)

variables_to_analyze = [
    'log_GDP per capita',
    'log_Defence budget per capita',
    'Unemployment rate',
    'Secondary education attainment rate',
    'Defence budget % GDP',
    'GDP per capita % change',
    'Defence budget per capita % change',
    'Defence budget % GDP % change'
]

# Demean each variable within country
for var in variables_to_analyze:
    df[f'{var}_demeaned'] = df[var] - df.groupby('Country')[var].transform('mean')

# Create a new DataFrame with just the demeaned variables
demeaned_vars = [f'{var}_demeaned' for var in variables_to_analyze]
df_demeaned = df[demeaned_vars]

df_demeaned = df_demeaned.drop("log_Defence budget per capita_demeaned", axis=1)
df_demeaned = df_demeaned.drop("Defence budget per capita % change_demeaned", axis=1)

# Calculate VIF for each explanatory variable
vif_df = pd.DataFrame({
    'Variable': df_demeaned.columns,
    'VIF': [statsmodels.stats.outliers_influence.variance_inflation_factor(df_demeaned.values, i) for i in range(df_demeaned.shape[1])]
})

print(vif_df)