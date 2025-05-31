# Ugly code for now :) Got the job done at least

import pandas as pd
import glob

# Load each file into a dictionary
files = {
    2023: "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\2023_Military_Balance_budget_personnel_report_cleaned.csv",
    2024: "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\2024_Military_Balance_budget_personnel_report_cleaned.csv",
    2025: "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\2025_Military_Balance_budget_personnel_report_cleaned.csv"
}

dfs = []

# Process each file
for edition_year, file_path in files.items():
    df = pd.read_csv(file_path)
    
    # Melt per capita budget
    df_percap = df.melt(
        id_vars=["Country"], 
        value_vars=[col for col in df.columns if "Defence budget per capita" in col],
        var_name="Metric", 
        value_name="Defence budget per capita"
    )
    df_percap["Year"] = df_percap["Metric"].str.extract(r'(\d{4})').astype(int)
    
    # Melt % of GDP
    df_gdp = df.melt(
        id_vars=["Country"], 
        value_vars=[col for col in df.columns if "Defence budget % GDP" in col],
        var_name="Metric", 
        value_name="Defence budget % GDP"
    )
    df_gdp["Year"] = df_gdp["Metric"].str.extract(r'(\d{4})').astype(int)
    
    # Melt active personnel
    df_troops = df.melt(
        id_vars=["Country"], 
        value_vars=[col for col in df.columns if "Active Armed Forces" in col],
        var_name="Metric", 
        value_name="Active Armed Forces"
    )
    df_troops["Year"] = df_troops["Metric"].str.extract(r'(\d{4})').astype(int)
    
    # Merge all three metrics
    df_merged = df_percap.drop(columns=["Metric"]).merge(
        df_gdp.drop(columns=["Metric"]), on=["Country", "Year"], how="outer"
    ).merge(
        df_troops.drop(columns=["Metric"]), on=["Country", "Year"], how="outer"
    )

    # Add edition year for duplicate resolution
    df_merged["Edition"] = edition_year
    dfs.append(df_merged)

# Combine all editions
df_all = pd.concat(dfs, ignore_index=True)

# Keep the latest edition for each Country-Year pair
df_all_sorted = df_all.sort_values(by=["Country", "Year", "Edition"], ascending=[True, True, False])

# df_final = df_all_sorted.drop_duplicates(subset=["Country", "Year"], keep="first").drop(columns=["Edition"])

# Mark duplicates based on Country and Year, keep='first' (latest edition)
duplicates_mask = df_all_sorted.duplicated(subset=["Country", "Year"], keep="first")
# Identify rows that have missing Active Armed Forces
missing_forces_mask = df_all_sorted["Active Armed Forces"].isna()
# Drop rows that are duplicates AND missing active forces
drop_mask = duplicates_mask & missing_forces_mask

# Keep only rows that are NOT to be dropped
df_final = df_all_sorted[~drop_mask].copy()

# Sort so rows with non-missing Active Armed Forces come first
df_final = df_final.sort_values(
    by=["Country", "Year", "Active Armed Forces"], 
    ascending=[True, True, False]  # False means non-missing / higher values come first
)

# Now drop duplicates keeping first occurrence (which will be the row with active forces if exists)
df_no_duplicates = df_final.drop_duplicates(subset=["Country", "Year"], keep="first").copy()

# Optional: sort for readability
df_no_duplicates = df_no_duplicates.sort_values(by=["Country", "Year"]).reset_index(drop=True)
df_no_duplicates = df_no_duplicates.drop(columns=["Edition"])

# Save or display
df_no_duplicates.to_csv("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\Military_Balance_combined.csv", index=False)
print("✅ Combined dataset saved successfully.")