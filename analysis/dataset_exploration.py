import pandas as pd
import scipy.stats
import plotly.express
import plotly.graph_objects as go
import plotly.subplots
import os

CLEAN_DIR = "clean_data"

df = pd.read_csv(os.path.join(CLEAN_DIR, "final_dataset.csv"))

print(df.info())

# Decribe columns
columns_to_check = [
    "log_Active Armed Forces per capita", "Unemployment rate", "Secondary education attainment rate", "log_GDP per capita",
    "log_Defence budget per capita", "Defence budget % GDP", "GDP per capita % change",
    "Defence budget per capita % change", "Defence budget % GDP % change"
]

print(df[columns_to_check].describe())


# Plot histograms:
# Determine subplot grid size (e.g., 3 columns)
cols = 3
rows = (len(columns_to_check) + cols - 1) // cols

fig = plotly.subplots.make_subplots(rows=rows, cols=cols, subplot_titles=columns_to_check)

for i, col in enumerate(columns_to_check):
    row = i // cols + 1
    col_pos = i % cols + 1
    fig.add_trace(
        go.Histogram(x=df[col], nbinsx=40, name=col, marker_color='steelblue'),
        row=row, col=col_pos
    )

fig.update_layout(height=300 * rows, width=900, title_text="Distributions of Variables")
fig.show()


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


# Interpolation numbers
total_interpolated = df["Education Interpolated"].sum()
print("Total interpolated values:", total_interpolated)

interpolated_per_country = df[df["Education Interpolated"] == True].groupby("Country").size()
print(interpolated_per_country)