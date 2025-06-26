import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

CLEAN_DIR = "clean_data"

df = pd.read_csv(os.path.join(CLEAN_DIR, "final_dataset.csv"))

df['Year'] = df['Year'].astype(int)

variables_to_analyze = [
    'log_Active Armed Forces per capita',
    'log_GDP per capita',
    'log_Defence budget per capita',
    'Unemployment rate',
    'Secondary education attainment rate',
    'Defence budget % GDP',
    'GDP per capita % change',
    'Defence budget per capita % change',
    'Defence budget % GDP % change'
]

# Demean each variable within country
for var in variables_to_analyze:
    df[f'{var}_demeaned'] = df[var] - df.groupby('Country')[var].transform('mean')

# Create a new DataFrame with just the demeaned variables
demeaned_vars = [f'{var}_demeaned' for var in variables_to_analyze]
df_demeaned = df[demeaned_vars]

# Compute Pearson correlation matrix
correlation_matrix = df_demeaned.corr()


# Plot the correlation matrix as a heatmap.

# renamed variables to fit better:
rename_dict = {
    'log_Active Armed Forces per capita_demeaned': 'Armed Forces per cap.',
    'log_GDP per capita_demeaned': 'GDP per cap.',
    'log_Defence budget per capita_demeaned': 'Def. spend. per cap.',
    'Unemployment rate_demeaned': 'Unemployment Rate',
    'Secondary education attainment rate_demeaned': 'Secondary education rate',
    'Defence budget % GDP_demeaned': 'Def. spend. % GDP',
    'GDP per capita % change_demeaned': 'GDP per cap. % change',
    'Defence budget per capita % change_demeaned': 'Def. spend. per cap. % change',
    'Defence budget % GDP % change_demeaned': 'Def. spend. % GDP % change'
}

correlation_matrix.rename(index=rename_dict, columns=rename_dict, inplace=True)

# Set the figure size and style
plt.figure(figsize=(10, 8))
sns.set_theme(style='white', font_scale=1.1)

# Apply font to tick labels
ax = sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap='coolwarm',
    vmin=-1, vmax=1,
    linewidths=0.5,
    square=True,
    cbar_kws={"shrink": 0.8}
)

# Set font for x and y tick labels
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname("sans-serif")  # or your desired font
    label.set_fontsize(13)  # adjust as needed

# Add title and show plot
# plt.title('Correlation Matrix', pad=20)
plt.tight_layout()
# plt.show()
plt.savefig("correlation_heatmap.pdf", bbox_inches="tight")
