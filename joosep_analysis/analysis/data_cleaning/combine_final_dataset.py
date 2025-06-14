import pandas as pd

# --- Load main dataset ---
main = pd.read_csv("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\combined_military_dataset.csv")

# --- Load and reshape GDP dataset ---
gdp = pd.read_csv("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\WB_GDP_constant_2015_cleaned.csv")
gdp_long = gdp.melt(id_vars="Country", var_name="Year", value_name="GDP (2015 USD)")
gdp_long["Year"] = gdp_long["Year"].str.extract("(\d{4})").astype(int)

# --- Load and reshape Population dataset ---
pop = pd.read_csv("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\WB_Total_population_over_years_cleaned.csv")
pop_long = pop.melt(id_vars="Country", var_name="Year", value_name="Population")
pop_long["Year"] = pop_long["Year"].str.extract("(\d{4})").astype(int)

# --- Load and reshape Unemployment dataset ---
unemp = pd.read_csv("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\WB_unemployment_rates_cleaned.csv")
unemp_long = unemp.melt(id_vars="Country", var_name="Year", value_name="Unemployment rate")
unemp_long["Year"] = unemp_long["Year"].str.extract("(\d{4})").astype(int)

# --- Load education interpolation flag ---
edu_interp = pd.read_csv("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\WB_education_interpolation_flags.csv")
edu_interp_long = edu_interp.melt(id_vars="Country", var_name="Year", value_name="Education Interpolated")
edu_interp_long["Year"] = edu_interp_long["Year"].str.extract("(\d{4})").astype(int)

# --- Load and reshape Secondary Education dataset ---
edu = pd.read_csv("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\WB_upper_secondary_education_rates_cleaned.csv")
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

# 2024 GDP per capita % change gets values 0 as 2024 GDP per capita was filled in with 2023 values
# Because of that, I also fill the 2024 GDP per capita % change with values from 2023:
# Identify the 2024 rows where GDP per capita % change is 0 or NaN
mask_2024 = (df["Year"] == 2024) & ((df["GDP per capita % change"].isna()) | (df["GDP per capita % change"] == 0))

# Create a mapping from 2023 values for each country
gdp_change_2023 = df[df["Year"] == 2023][["Country", "GDP per capita % change"]].dropna()
gdp_change_dict = dict(zip(gdp_change_2023["Country"], gdp_change_2023["GDP per capita % change"]))

# Apply the mapping to fill 2024 missing/zero values
df.loc[mask_2024, "GDP per capita % change"] = df.loc[mask_2024, "Country"].map(gdp_change_dict)

# --- Save or inspect result ---
df.to_csv("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\final_dataset.csv", index=False)
print("Final dataset saved")