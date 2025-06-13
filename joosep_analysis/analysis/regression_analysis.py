import linearmodels
import pandas as pd
import numpy as np

df = pd.read_csv("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\final_dataset.csv")

###############
# Subset data #
###############

# Remove data for Russia and China because it might be unreliable
# Also remove 2024 data as it is mostly filled in/interpolated from 2023 values

df = df[
    (~df["Country"].isin(["Russia", "China"]))                  # Exclude Russia and China
    (df["Year"] != 2024)                                        # Exclude year 2024
    # (df["Country"].isin(["Estonia", "Latvia", "Lithuania"]))    # Test for Baltics
]

df = df.reset_index(drop=True)

##############
# Clean data #
##############

# Convert relevant columns to numeric if needed
numeric_cols = [
    'Defence budget per capita', 'Defence budget % GDP', 'Active Armed Forces',
    'Population', 'GDP (2015 USD)', 'Unemployment rate',
    'Secondary education attainment rate', 'GDP per capita',
    'GDP per capita % change', 'Defence budget per capita % change',
    'Defence budget % GDP % change', 'Active Armed Forces per capita'
]

# Convert columns to numeric (in case of any string entries)
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

df[numeric_cols] = df[numeric_cols].replace(0, np.nan)

# Drop rows with missing values
df_clean = df.dropna(subset=numeric_cols).copy()

log_cols = ["Active Armed Forces per capita", "GDP per capita", "Defence budget per capita"] # 'Active Armed Forces', 'Population', 'GDP (2015 USD)'
for col in log_cols:
    df_clean[f"log_{col}"] = np.log(df_clean[col])

##################
# Run regression #
##################

# Assume df is a MultiIndex DataFrame: (entity, time)
df_clean = df_clean.set_index(['Country', 'Year'])

y = df_clean["log_Active Armed Forces per capita"]
X = df_clean[["Unemployment rate", "Secondary education attainment rate", "log_GDP per capita", 
              "log_Defence budget per capita", "Defence budget % GDP", "GDP per capita % change", 
              "Defence budget per capita % change", "Defence budget % GDP % change"]]

# Run Fixed Effects model
model = linearmodels.PanelOLS(y, X, entity_effects=True)
# model = linearmodels.PanelOLS.from_formula('outcome ~ var1 + var2 + EntityEffects', data=df)
results = model.fit()
print(results.summary)