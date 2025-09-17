import pandas as pd
from matplotlib import pyplot as plt

path = "data_processed/co2_emissions_all_years.csv"
df = pd.read_csv(path)
df["CO2 emissions (kt)"] = pd.to_numeric(df["CO2 emissions (kt)"], errors="coerce")
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

prova = df.loc[df["Category"] == "Total national emissions and removals", 
               ["Category","CO2 emissions (kt)","Year"]].round(2)


cats = ["1. Energy", "2.  Industrial processes and product use", "3.  Agriculture", "5.  Waste"]
df_filtered = df[df["Category"].isin(cats)]
df_pivot = df_filtered.pivot(index="Year", columns="Category", values="CO2 emissions (kt)")

df_pivot.plot(figsize=(10,6))
plt.ylabel("CO₂ emissions (kt)")
plt.title("Emissioni CO₂ per categoria")
plt.show()
