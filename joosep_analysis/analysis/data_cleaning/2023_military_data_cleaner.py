import pandas as pd

# Read the CSV data; here header=None tells pandas that the file has no header row.
RAW_DATA_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\raw_data\\2023_Military_Balance_budget_personnel_report.csv"
CLEAN_DATA_PATH = "C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\2023_Military_Balance_budget_personnel_report_cleaned.csv"

# Load the file, skipping the first two rows
df = pd.read_csv(RAW_DATA_PATH, skiprows=3, header=None)

columns_to_keep = [0, 5, 6, 8, 9, 10]
df = df.iloc[:, columns_to_keep]
df.columns = ["Country", "Defence budget per capita prev year", "Defence budget per capita curr year", "Defence budget % GDP prev year", "Defence budget % GDP curr year", "Active Armed Forces"]

# Remove rows, which are not for single countries
df = df[~df["Country"].isin(["Europe", "Russia and Eurasia", "Total", "Total**", "Asia", "Middle East and North Africa", "Middle East and North Africa**", "Latin America and the Caribbean", "Sub-Saharan Africa", "North America", "Summary", "Global totals"])]
# Remove rows with missing values
df = df[~df.apply(lambda row: row.astype(str).str.contains(r'n.k.|^-$', regex=True).any(), axis=1)]

# Convert to correct data types
int_cols = ["Defence budget per capita prev year", "Defence budget per capita curr year", "Active Armed Forces"]
float_cols = ["Defence budget % GDP prev year", "Defence budget % GDP curr year"]

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

df = df.reset_index(drop=True)
df.to_csv(CLEAN_DATA_PATH, index=False)
