import pandas as pd
import os

# File paths
BASE_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis"
RAW_DIR = os.path.join(BASE_PATH, "raw_data")
CLEAN_DIR = os.path.join(BASE_PATH, "clean_data")
COUNTRIES_PATH = os.path.join(RAW_DIR, "countries_of_interest.csv")

# Yearly configurations
YEAR_CONFIGS = {
    2021: {"skiprows": 2, "inflation_factor": 237.0 / 271.0},
    2022: {"skiprows": 2, "inflation_factor": 237.0 / 292.7},
    2023: {"skiprows": 3, "inflation_factor": 237.0 / 304.7},
    2024: {"skiprows": 3, "inflation_factor": 237.0 / 313.7},
    2025: {"skiprows": 0, "inflation_factor": 237.0 / 322.3},
}

# Process each year
for year in range(2021, 2026):
    print(f"Processing year {year}...")

    # Country name mappings
    name_mappings = {
        "Czechia": "Czech Republic",
        "North Macedonia": "Macedonia, North",
        "Russia": "Russia [a]",
        "Türkiye": "Turkiye",
        "United Kingdom": "United Kingdom*",
    }

    if year == 2025:
        name_mappings["Germany"] = "Germany*"

    if year in [2021, 2022, 2023]:
        name_mappings["Türkiye"] = "Turkey" 

    reverse_mappings = {v: k for k, v in name_mappings.items()}

    # Load country list
    countries_df = pd.read_csv(COUNTRIES_PATH)
    countries_df["Country"] = countries_df["Country"].replace(name_mappings)
    countries_list = countries_df["Country"].tolist()

    raw_file = os.path.join(RAW_DIR, f"{year}_Military_Balance_budget_personnel_report.csv")
    clean_file = os.path.join(CLEAN_DIR, f"{year}_Military_Balance_budget_personnel_report_cleaned.csv")
    
    config = YEAR_CONFIGS[year]
    df = pd.read_csv(raw_file, skiprows=config["skiprows"], header=None)

    # Select and rename columns
    columns_to_keep = [0, 4, 5, 6, 7, 8, 9, 10]
    ############################## TODO: continue here ################################
    df = df[columns_to_keep]
    df.columns = [
        "Country",
        f"Defence budget per capita {year - 3}",
        f"Defence budget per capita {year - 2}",
        f"Defence budget per capita {year - 1}",
        f"Defence budget % GDP {year - 3}",
        f"Defence budget % GDP {year - 2}",
        f"Defence budget % GDP {year - 1}",
        f"Active Armed Forces {year - 1}"
    ]

    # Filter countries
    df = df[df["Country"].isin(countries_list)]

    # Remove missing rows
    df = df[~df.apply(lambda row: row.astype(str).str.contains(r'n.k.|^-$', regex=True).any(), axis=1)]

    # Define column lists
    int_cols = [col for col in df.columns if "per capita" in col or "Armed Forces" in col]
    float_cols = [col for col in df.columns if "% GDP" in col]

    # Clean and convert types
    for col in int_cols:
        df[col] = df[col].astype(str).str.replace(",", "", regex=False).astype(float).astype(int)

    for col in float_cols:
        df[col] = df[col].astype(str).str.replace(",", "", regex=False).astype(float)

    # Inflation correction
    per_capita_cols = [col for col in df.columns if "per capita" in col]
    for col in per_capita_cols:
        df[col] = df[col] * config["inflation_factor"]

    # Reverse name mappings for output
    df["Country"] = df["Country"].replace(reverse_mappings)

    df = df.reset_index(drop=True)
    df.to_csv(clean_file, index=False)

print("✅ All files processed and saved.")