import pandas as pd

# Paths
POP_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\raw_data\\WB_Total_population_over_years.csv"
OUTPUT_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\WB_Total_population_over_years_cleaned.csv"

COUNTRIES_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\raw_data\\countries_of_interest.csv"


# Get countries in the military dataset
countries_df = pd.read_csv(COUNTRIES_PATH)

# Replace country names to match raw data format
name_mappings = {
    "Russia": "Russian Federation",
    "Slovakia": "Slovak Republic",
    "Türkiye": "Turkiye",
}
countries_df["Country"] = countries_df["Country"].replace(name_mappings)
countries_list = countries_df["Country"].tolist()

# Load population data (skip metadata rows)
population_df = pd.read_csv(POP_PATH, skiprows=4)

# Filter only relevant countries
population_df = population_df[population_df["Country Name"].isin(countries_list)]

# Keep only country name and selected years
fields_to_keep = ["Country Name", "2021", "2022", "2023"]
population_df = population_df[fields_to_keep]

# Rename for clarity
population_df.columns = ["Country", "Population 2021", "Population 2022", "Population 2023"]

# Optional: convert to integers (removing missing data or empty strings)
population_df = population_df.replace('', pd.NA).dropna()
population_df["Population 2021"] = population_df["Population 2021"].astype(int)
population_df["Population 2022"] = population_df["Population 2022"].astype(int)
population_df["Population 2023"] = population_df["Population 2023"].astype(int)

# Reverse the name mappings for the final output
reverse_mappings = {v: k for k, v in name_mappings.items()}
population_df["Country"] = population_df["Country"].replace(reverse_mappings)

# Save to file
population_df.to_csv(OUTPUT_PATH, index=False)

print("Filtered population data saved!")