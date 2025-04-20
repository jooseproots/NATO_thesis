import pandas as pd

# Paths
POP_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\raw_data\\WB_Total_population_over_years.csv"
MIL_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\2023_Military_Balance_budget_personnel_report_cleaned.csv"
OUTPUT_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\WB_Total_population_over_years_cleaned.csv"

# Get countries in the military dataset
mil_df = pd.read_csv(MIL_PATH)
mil_countries = mil_df["Country"].tolist()

# Load population data (skip metadata rows)
population_df = pd.read_csv(POP_PATH, skiprows=4)

# Filter only relevant countries
population_df = population_df[population_df["Country Name"].isin(mil_countries)]

# Keep only country name and selected years
fields_to_keep = ["Country Name", "2022", "2023"]
population_df = population_df[fields_to_keep]

# Rename for clarity
population_df.columns = ["Country", "Population 2022", "Population 2023"]

# Optional: convert to integers (removing missing data or empty strings)
population_df = population_df.replace('', pd.NA).dropna()
population_df["Population 2022"] = population_df["Population 2022"].astype(int)
population_df["Population 2023"] = population_df["Population 2023"].astype(int)

# Save to file
population_df.to_csv(OUTPUT_PATH, index=False)

print("Filtered population data saved!")