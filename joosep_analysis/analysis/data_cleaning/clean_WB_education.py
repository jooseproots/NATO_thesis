import pandas as pd

# Paths
EDUCATION_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\raw_data\\WB_upper_secondary_education_rates.csv"
OUTPUT_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\WB_upper_secondary_education_rates_cleaned.csv"

COUNTRIES_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\raw_data\\countries_of_interest.csv"

# Step 1: Load CSV, skipping the metadata rows (first 3 rows are metadata)
df_raw = pd.read_csv(EDUCATION_PATH, skiprows=3)

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

# Step 3.5: Interpolate missing years
# Replace empty strings with proper NA
df_filtered = df_filtered.replace('', pd.NA)

# Convert all year columns to numeric (from 1960 to 2024)
year_cols = [col for col in df_filtered.columns if col.isdigit()]
df_filtered[year_cols] = df_filtered[year_cols].apply(pd.to_numeric, errors='coerce')

# Interpolate missing values across years (row-wise per country)
df_filtered[year_cols] = df_filtered[year_cols].interpolate(axis=1, limit_direction='both')

# Optional: Forward/backward fill to catch edge cases
df_filtered[year_cols] = df_filtered[year_cols].fillna(axis=1, method='ffill').fillna(axis=1, method='bfill')

# Step 4: Select only the columns you want
columns_to_keep = ["Country Name", "2022", "2023", "2024"]
df_final = df_filtered[columns_to_keep]

# Step 5: Optional - Rename columns for clarity
df_final.columns = ["Country", "Secondary Education Attainment 2022", "Secondary Education Attainment 2023", "Secondary Education Attainment 2024"]

# Optional: convert to integers (removing missing data or empty strings)
df_final["Secondary Education Attainment 2022"] = df_final["Secondary Education Attainment 2022"].astype(float)
df_final["Secondary Education Attainment 2023"] = df_final["Secondary Education Attainment 2023"].astype(float)
df_final["Secondary Education Attainment 2024"] = df_final["Secondary Education Attainment 2024"].astype(float)

# Reverse the name mappings for the final output
reverse_mappings = {v: k for k, v in name_mappings.items()}
df_final["Country"] = df_final["Country"].replace(reverse_mappings)

# Step 6: Save to CSV
df_final.to_csv(OUTPUT_PATH, index=False)

print("✅ Cleaned data saved to ", OUTPUT_PATH)