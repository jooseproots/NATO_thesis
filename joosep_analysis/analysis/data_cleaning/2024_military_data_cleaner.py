import pandas as pd

# Read the CSV data; here header=None tells pandas that the file has no header row.
RAW_DATA_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\raw_data\\2024_Military_Balance_budget_personnel_report.csv"
CLEAN_DATA_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\2024_Military_Balance_budget_personnel_report_cleaned.csv"

df = pd.read_csv(RAW_DATA_PATH, header=None)

columns_to_keep = [0, 5, 6, 8, 9, 10]
df = df[columns_to_keep]
df.columns = ["Country", "Defence budget per capita prev year", "Defence budget per capita curr year", "Defence budget % GDP prev year", "Defence budget % GDP curr year", "Active Armed Forces"]

# Remove rows, which are not for single countries
df = df[~df["Country"].isin(["Europe", "Russia and Eurasia", "Total", "Total**", "Asia", "Middle East and North Africa", "Middle East and North Africa**", "Latin America and the Caribbean", "Sub-Saharan Africa", "North America", "Summary", "Global totals"])]
# Remove rows with missing values
df = df[~df.apply(lambda row: row.astype(str).str.contains("n.k.").any(), axis=1)]

# Convert strings with commas to integers
int_cols = ["Defence budget per capita prev year", "Defence budget per capita curr year", "Active Armed Forces"]
float_cols = ["Defence budget % GDP prev year", "Defence budget % GDP curr year"]

# Convert comma-separated strings to integers
for col in int_cols:
    df[col] = df[col].astype(str).str.replace(',', '', regex=False).astype(int)

# Convert decimal strings to float (if any)
for col in float_cols:
    df[col] = df[col].astype(str).str.replace(',', '', regex=False).astype(float)

df = df.reset_index(drop=True)
df.to_csv(CLEAN_DATA_PATH, index=False)
