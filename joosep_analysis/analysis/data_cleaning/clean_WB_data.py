import pandas as pd
import os

# Constants and paths
BASE_DIR = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis"
RAW_DIR = os.path.join(BASE_DIR, "raw_data")
CLEAN_DIR = os.path.join(BASE_DIR, "clean_data")
COUNTRIES_PATH = os.path.join(RAW_DIR, "countries_of_interest.csv")

# Desired output years
YEARS = ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]

# Country name mappings
NAME_MAPPINGS = {
    "Russia": "Russian Federation",
    "Slovakia": "Slovak Republic",
    "Türkiye": "Turkiye",
}
REVERSE_MAPPINGS = {v: k for k, v in NAME_MAPPINGS.items()}


def load_countries():
    df = pd.read_csv(COUNTRIES_PATH)
    df["Country"] = df["Country"].replace(NAME_MAPPINGS)
    return df["Country"].tolist()


def clean_and_transform_dataset(name, filename, value_name, interpolate=False):
    path = os.path.join(RAW_DIR, filename)
    df = pd.read_csv(path, skiprows=4)

    # Filter relevant countries
    countries = load_countries()
    df = df[df["Country Name"].isin(countries)]

    # Ensure years exist in the dataset
    available_years = [col for col in df.columns if col.isdigit()]
    selected_years = [year for year in YEARS if year in available_years]

    # Fill in missing requested years (e.g., 2024 may not exist yet)
    for year in YEARS:
        if year not in df.columns:
            df[year] = pd.NA

    # Replace missing data
    df = df.replace('', pd.NA)

    # Interpolate across year columns if needed
    df[YEARS] = df[YEARS].apply(pd.to_numeric, errors='coerce')
    if interpolate:
        df[YEARS] = df[YEARS].interpolate(axis=1, limit_direction='both')
        df[YEARS] = df[YEARS].ffill(axis=1).bfill(axis=1)

    # Construct final DataFrame
    df_final = df[["Country Name"] + YEARS]
    new_column_names = ["Country"] + [f"{value_name} {year}" for year in YEARS]
    df_final.columns = new_column_names

    # Convert to float
    df_final = df_final.copy()
    for col in new_column_names[1:]:
        df_final[col] = df_final[col].astype(float)

    # Reverse country name mappings
    df_final["Country"] = df_final["Country"].replace(REVERSE_MAPPINGS)

    # Save to output
    output_file = os.path.join(CLEAN_DIR, f"{name}_cleaned.csv")
    df_final.to_csv(output_file, index=False)
    print(f"Saved cleaned {name} data to {output_file}")


# Dataset configurations
datasets = [
    {"name": "WB_upper_secondary_education_rates", "file": "WB_upper_secondary_education_rates.csv", "value": "Secondary Education Attainment", "interpolate": True},
    {"name": "WB_GDP_constant_2015", "file": "WB_GDP_constant_2015.csv", "value": "GDP", "interpolate": True},
    {"name": "WB_Total_population_over_years", "file": "WB_Total_population_over_years.csv", "value": "Population", "interpolate": True},
    {"name": "WB_unemployment_rates", "file": "WB_unemployment_rates.csv", "value": "Unemployment", "interpolate": True},
]

# Run all dataset cleaners
for ds in datasets:
    print(f"Processing {ds['name']}...")
    clean_and_transform_dataset(
        name=ds["name"],
        filename=ds["file"],
        value_name=ds["value"],
        interpolate=ds["interpolate"]
    )