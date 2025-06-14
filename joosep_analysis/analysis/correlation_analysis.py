import pandas as pd

df = pd.read_csv("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\final_dataset.csv")

df['Year'] = df['Year'].astype(int)

variables_to_analyze = [
    'log_Active Armed Forces per capita',
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

# Compute Pearson correlation matrix
correlation_matrix = df_demeaned.corr()
print(correlation_matrix.round(2))

# latex_table = correlation_matrix.round(2).to_latex(index=True, float_format="%.2f")
# print(latex_table)