import linearmodels
import pandas as pd
# import matplotlib.pyplot as plt

df = pd.read_csv("C:\\Users\\joose\\Git_repos\\NATO_thesis\\joosep_analysis\\clean_data\\final_dataset.csv")

##################
# Run regression #
##################

# Exclude interpolated and filled education values
# df = df[(df["Education Interpolated"] == False)]

# Dummy variable for sensitivity analysis on interpolated values
df["Education Dummy"] = df["Education Interpolated"].astype(int)

# Assume df is a MultiIndex DataFrame: (entity, time)
df = df.set_index(['Country', 'Year'])

y = df["log_Active Armed Forces per capita"]
X = df[["Unemployment rate", "Secondary education attainment rate", "log_GDP per capita", 
        "Defence budget % GDP", "GDP per capita % change", 
        "Defence budget % GDP % change", "Education Dummy"]]

# Run Fixed Effects model
model = linearmodels.PanelOLS(y, X, entity_effects=True, time_effects=True)
results = model.fit(cov_type="clustered", cluster_entity=True)
print(results.summary)
print(results.rsquared)
print(results.rsquared_inclusive)

# residuals = results.resids
# fitted = results.fitted_values

# plt.scatter(fitted, residuals, alpha=0.5)
# plt.axhline(0, color='red', linestyle='--')
# plt.xlabel('Fitted values')
# plt.ylabel('Residuals')
# plt.title('Residuals vs Fitted Values')
# plt.show()