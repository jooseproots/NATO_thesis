import pandas as pd
import scipy.stats
import plotly.express

df = pd.read_csv("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\final_dataset.csv")

print(df.info())

# Decribe columns
columns_to_check = [
    "Unemployment rate", "Secondary education attainment rate", "GDP per capita",
    "Defence budget per capita", "Defence budget % GDP", "GDP per capita % change",
    "Defence budget per capita % change", "Defence budget % GDP % change"
]

print(df[columns_to_check].describe())


# Z score outliers
df_clean = df[columns_to_check].dropna()

z_scores = df_clean.apply(scipy.stats.zscore)

                                      # 3 is a common threshold
outliers_z = df_clean[(z_scores.abs() > 3).any(axis=1)]
print(outliers_z)


# IQR outliers
def detect_outliers_iqr(df: pd.DataFrame, column: str):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]

for col in columns_to_check:
    outliers = detect_outliers_iqr(df, col)
    print(outliers[["Country", "Year", col]])


# Education rate interpolation check
fig = plotly.express.line(
    df,
    x='Year',
    y='Secondary education attainment rate',
    color='Country',
    title='Education Rate Over Time by Country',
    labels={'Secondary education attainment rate': 'Education Rate (%)'},
)

fig.update_layout(
    legend_title_text='Country',
    hovermode='x unified',
    template='plotly_white',
    height=600,
    width=1000
)

fig.show()