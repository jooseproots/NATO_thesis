import pandas as pd

# Read the CSV data; here header=None tells pandas that the file has no header row.
RAW_DATA_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\raw_data\\2025_Military_Balance_budget_personnel_report.csv"
CLEAN_DATA_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\2025_Military_Balance_budget_personnel_report_cleaned.csv"

COUNTRIES_PATH = COUNTRIES_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\raw_data\\countries_of_interest.csv"

df = pd.read_csv(RAW_DATA_PATH, header=None)

# Load countries of interest
countries_df = pd.read_csv(COUNTRIES_PATH)

# Replace country names to match raw data format
name_mappings = {
    "Czechia": "Czech Republic",
    "North Macedonia": "Macedonia, North",
    "Russia": "Russia [a]",
    "Türkiye": "Turkiye",
    "United Kingdom": "United Kingdom*",
    "Germany": "Germany*",
}
countries_df["Country"] = countries_df["Country"].replace(name_mappings)
countries_list = countries_df["Country"].tolist()

columns_to_keep = [0, 4, 5, 6, 7, 8, 9, 10]
df = df[columns_to_keep]
df.columns = ["Country", "Defence budget per capita 2022", "Defence budget per capita 2023", "Defence budget per capita 2024", "Defence budget % GDP prev year 2022", "Defence budget % GDP prev year 2023", "Defence budget % GDP prev year 2024", "Active Armed Forces 2024"]

# Remove rows, which are not for single countries
df = df[df["Country"].isin(countries_list)]
# Remove rows with missing values
df = df[~df.apply(lambda row: row.astype(str).str.contains("n.k.").any(), axis=1)]

# Convert strings with commas to integers
int_cols = ["Defence budget per capita 2022", "Defence budget per capita 2023", "Defence budget per capita 2024", "Active Armed Forces 2024"]
float_cols = ["Defence budget % GDP prev year 2022", "Defence budget % GDP prev year 2023", "Defence budget % GDP prev year 2024"]

# Convert comma-separated strings to integers
for col in int_cols:
    df[col] = df[col].astype(str).str.replace(',', '', regex=False).astype(int)

# Convert decimal strings to float (if any)
for col in float_cols:
    df[col] = df[col].astype(str).str.replace(',', '', regex=False).astype(float)

# Reverse the name mappings for the final output
reverse_mappings = {v: k for k, v in name_mappings.items()}
df["Country"] = df["Country"].replace(reverse_mappings)

df = df.reset_index(drop=True)
df.to_csv(CLEAN_DATA_PATH, index=False)
