import pandas as pd
import glob
import re

# Step 1: Load and reshape each file
def process_file(file_path, priority):
    df = pd.read_csv(file_path)

    # Identify columns
    budget_cols = [col for col in df.columns if "Defence budget per capita" in col]
    gdp_cols = [col for col in df.columns if "Defence budget % GDP" in col]
    active_col = [col for col in df.columns if "Active Armed Forces" in col][0]
    active_year = int(re.search(r'\d{4}', active_col).group())

    # Melt budget per capita
    budget_df = df.melt(id_vars=["Country"], value_vars=budget_cols,
                        var_name="Metric_Year", value_name="Defence budget per capita")
    budget_df["Year"] = budget_df["Metric_Year"].str.extract(r'(\d{4})').astype(int)
    budget_df.drop("Metric_Year", axis=1, inplace=True)

    # Melt % GDP
    gdp_df = df.melt(id_vars=["Country"], value_vars=gdp_cols,
                     var_name="Metric_Year", value_name="Defence budget % GDP")
    gdp_df["Year"] = gdp_df["Metric_Year"].str.extract(r'(\d{4})').astype(int)
    gdp_df.drop("Metric_Year", axis=1, inplace=True)

    # Merge on Country + Year
    merged = pd.merge(budget_df, gdp_df, on=["Country", "Year"])
    merged["Source Priority"] = priority

    # Extract active personnel for the specific year
    active_df = df[["Country", active_col]].copy()
    active_df.rename(columns={active_col: "Active Armed Forces"}, inplace=True)
    active_df["Year"] = active_year

    return merged, active_df

# Step 2: Process all files
file_paths = sorted(
    glob.glob("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\*_Military_Balance_budget_personnel_report_cleaned.csv"),
    reverse=True
)
budget_dfs = []
active_dfs = []

for i, file_path in enumerate(file_paths):
    budget_df, active_df = process_file(file_path, priority=i)
    budget_dfs.append(budget_df)
    active_dfs.append(active_df)

# Step 3: Combine budget/GDP data and deduplicate by latest source
combined_budget = pd.concat(budget_dfs)
combined_budget = combined_budget.sort_values(by=["Country", "Year", "Source Priority"])
combined_budget = combined_budget.drop_duplicates(subset=["Country", "Year"], keep="first").drop(columns=["Source Priority"])

# Step 4: Combine active personnel data (no deduplicate needed, one year per file)
combined_active = pd.concat(active_dfs)
combined_active = combined_active.drop_duplicates(subset=["Country", "Year"], keep="first")

# Step 5: Merge everything
final = pd.merge(combined_budget, combined_active, on=["Country", "Year"], how="left")

# Step 6: Save to CSV
final.to_csv("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\combined_military_dataset.csv", index=False)

print("Success!")