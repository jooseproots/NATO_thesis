import pandas as pd

# Paths
UNEMPLOYMENT_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\raw_data\\WB_unemployment_rates.csv"
OUTPUT_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\WB_unemployment_rates_cleaned.csv"

COUNTRIES_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\raw_data\\countries_of_interest.csv"

# Step 1: Load CSV, skipping the metadata rows (first 3 rows are metadata)
df_raw = pd.read_csv(UNEMPLOYMENT_PATH, skiprows=3)

# Step 2: List of countries you're interested in
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

# Step 3: Filter rows to keep only selected countries
df_filtered = df_raw[df_raw["Country Name"].isin(countries_list)]

# Step 4: Select only the columns you want
columns_to_keep = ["Country Name", "2022", "2023", "2024"]
df_final = df_filtered[columns_to_keep]

# Step 5: Optional - Rename columns for clarity
df_final.columns = ["Country", "Unemployment 2022", "Unemployment 2023", "Unemployment 2024"]

# Optional: convert to integers (removing missing data or empty strings)
df_final = df_final.replace('', pd.NA).dropna()
df_final["Unemployment 2022"] = df_final["Unemployment 2022"].astype(float)
df_final["Unemployment 2023"] = df_final["Unemployment 2023"].astype(float)
df_final["Unemployment 2024"] = df_final["Unemployment 2024"].astype(float)

# Reverse the name mappings for the final output
reverse_mappings = {v: k for k, v in name_mappings.items()}
df_final["Country"] = df_final["Country"].replace(reverse_mappings)

# Step 6: Save to CSV
df_final.to_csv(OUTPUT_PATH, index=False)

print("✅ Cleaned data saved to ", OUTPUT_PATH)