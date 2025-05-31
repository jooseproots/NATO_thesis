import pandas as pd

# Read the CSV data; here header=None tells pandas that the file has no header row.
RAW_DATA_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\raw_data\\2024_Military_Balance_budget_personnel_report.csv"
CLEAN_DATA_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\2024_Military_Balance_budget_personnel_report_cleaned.csv"

COUNTRIES_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\raw_data\\countries_of_interest.csv"

# Load the file, skipping the first two rows
df = pd.read_csv(RAW_DATA_PATH, skiprows=3, header=None)

# Load countries of interest
countries_df = pd.read_csv(COUNTRIES_PATH)

# Replace country names to match raw data format
name_mappings = {
    "Czechia": "Czech Republic",
    "North Macedonia": "Macedonia, North",
    "Russia": "Russia [a]",
    "Türkiye": "Turkiye",
    "United Kingdom": "United Kingdom*"
}
countries_df["Country"] = countries_df["Country"].replace(name_mappings)
countries_list = countries_df["Country"].tolist()

columns_to_keep = [0, 4, 5, 6, 7, 8, 9, 10]
df = df[columns_to_keep]
df.columns = ["Country", "Defence budget per capita 2021", "Defence budget per capita 2022", "Defence budget per capita 2023", "Defence budget % GDP 2021", "Defence budget % GDP 2022", "Defence budget % GDP 2023", "Active Armed Forces 2023"]

# Remove rows, which are not for single countries
df = df[df["Country"].isin(countries_list)]
# Remove rows with missing values
df = df[~df.apply(lambda row: row.astype(str).str.contains(r'n.k.|^-$', regex=True).any(), axis=1)]

# Convert to correct data types
int_cols = ["Defence budget per capita 2021", "Defence budget per capita 2022", "Defence budget per capita 2023", "Active Armed Forces 2023"]
float_cols = ["Defence budget % GDP 2021", "Defence budget % GDP 2022", "Defence budget % GDP 2023"]

for col in int_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(',', '', regex=False)
        .astype(float)   # use float here first
        .astype(int)     # then cast to int
    )

for col in float_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(',', '', regex=False)
        .astype(float)
    )

# Reverse the name mappings for the final output
reverse_mappings = {v: k for k, v in name_mappings.items()}
df["Country"] = df["Country"].replace(reverse_mappings)

df = df.reset_index(drop=True)
df.to_csv(CLEAN_DATA_PATH, index=False)
