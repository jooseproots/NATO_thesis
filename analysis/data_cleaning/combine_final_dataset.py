import pandas as pd
import numpy as np
import os

CLEAN_DIR = "clean_data"

# --- Load datasets ---
main = pd.read_csv(os.path.join(CLEAN_DIR, "combined_military_dataset.csv"))
gdp = pd.read_csv(os.path.join(CLEAN_DIR, "WB_GDP_constant_2015_cleaned.csv"))
pop = pd.read_csv(os.path.join(CLEAN_DIR, "WB_Total_population_over_years_cleaned.csv"))
unemp = pd.read_csv(os.path.join(CLEAN_DIR, "WB_unemployment_rates_cleaned.csv"))
edu_interp = pd.read_csv(os.path.join(CLEAN_DIR, "WB_education_interpolation_flags.csv"))
edu = pd.read_csv(os.path.join(CLEAN_DIR, "WB_upper_secondary_education_rates_cleaned.csv"))


# --- reshape GDP dataset ---
gdp_long = gdp.melt(id_vars="Country", var_name="Year", value_name="GDP (2015 USD)")
gdp_long["Year"] = gdp_long["Year"].str.extract("(\d{4})").astype(int)

# --- reshape Population dataset ---
pop_long = pop.melt(id_vars="Country", var_name="Year", value_name="Population")
pop_long["Year"] = pop_long["Year"].str.extract("(\d{4})").astype(int)

# --- reshape Unemployment dataset ---
unemp_long = unemp.melt(id_vars="Country", var_name="Year", value_name="Unemployment rate")
unemp_long["Year"] = unemp_long["Year"].str.extract("(\d{4})").astype(int)

# --- education interpolation flag ---
edu_interp_long = edu_interp.melt(id_vars="Country", var_name="Year", value_name="Education Interpolated")
edu_interp_long["Year"] = edu_interp_long["Year"].str.extract("(\d{4})").astype(int)

# --- reshape Secondary Education dataset ---
edu_long = edu.melt(id_vars="Country", var_name="Year", value_name="Secondary education attainment rate")
edu_long["Year"] = edu_long["Year"].str.extract("(\d{4})").astype(int)

edu_long = edu_long.merge(edu_interp_long, on=["Country", "Year"], how="left")

# --- Merge all with main dataset ---
df = main.merge(pop_long, on=["Country", "Year"], how="left")
df = df.merge(gdp_long, on=["Country", "Year"], how="left")
df = df.merge(unemp_long, on=["Country", "Year"], how="left")
df = df.merge(edu_long, on=["Country", "Year"], how="left")

# --- Create additional columns ---
numeric_cols = [
    "Defence budget per capita", "Defence budget % GDP", "Active Armed Forces",
    "Population", "GDP (2015 USD)", "Unemployment rate", "Secondary education attainment rate"
]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Sort by Country and Year for correct diff calculation
df = df.sort_values(by=['Country', 'Year'])

# Compute GDP per capita
df['GDP per capita'] = df['GDP (2015 USD)'] / df['Population']

# Compute % change from previous year for GDP per capita
df['GDP per capita % change'] = df.groupby('Country')['GDP per capita'].pct_change(fill_method=None) * 100

# Compute % change from previous year for Defence budget per capita
df['Defence budget per capita % change'] = df.groupby('Country')['Defence budget per capita'].pct_change(fill_method=None) * 100

# Compute % change from previous year for Defence budget % GDP
df['Defence budget % GDP % change'] = df.groupby('Country')['Defence budget % GDP'].pct_change(fill_method=None) * 100

# armed forces per capita
df['Active Armed Forces per capita'] = df['Active Armed Forces'] / df['Population']


###########################
# Finalize for regression #
###########################

df = df[
    (~df["Country"].isin(["China", "Iceland"])) &              # Exclude China (not enough education data) and Iceland (No active military)
    (~df["Year"].isin([2013, 2014, 2024]))                    # Exclude years 2013, 2014, because they have no armed forces data and 2024, because it is mostly imputed values
]

df = df.reset_index(drop=True)

# Convert relevant columns to numeric if needed
numeric_cols_new = [
    'Defence budget per capita', 'Defence budget % GDP', 'Active Armed Forces',
    'Population', 'GDP (2015 USD)', 'Unemployment rate',
    'Secondary education attainment rate', 'GDP per capita',
    'GDP per capita % change', 'Defence budget per capita % change',
    'Defence budget % GDP % change', 'Active Armed Forces per capita'
]

# Convert columns to numeric (in case of any string entries)
df[numeric_cols_new] = df[numeric_cols_new].apply(pd.to_numeric, errors='coerce')

df["Active Armed Forces"] = df["Active Armed Forces"].replace(0, np.nan) # replacing nulls with none and removing them because a log transformation can't handle nulls

# Drop rows with missing values
df_clean = df.dropna(subset=["Active Armed Forces"]).copy()

log_cols = ["Active Armed Forces per capita", "GDP per capita", "Defence budget per capita"]
for col in log_cols:
    df_clean[f"log_{col}"] = np.log(df_clean[col])

# Select final data
df_final = df_clean[["Country", "Year", "log_Active Armed Forces per capita", "Unemployment rate", "Secondary education attainment rate", 
               "log_GDP per capita", "log_Defence budget per capita", "Defence budget % GDP", "GDP per capita % change", 
               "Defence budget per capita % change", "Defence budget % GDP % change", "Education Interpolated"]]

# --- Save or inspect result ---
df_final.to_csv(os.path.join(CLEAN_DIR, "final_dataset.csv"), index=False)
print("Final dataset saved")