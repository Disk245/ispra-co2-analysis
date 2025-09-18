import pandas as pd
from matplotlib import pyplot as plt

path = "data_processed/co2_emissions_all_years.csv"
df = pd.read_csv(path)
df["CO2 emissions (kt)"] = pd.to_numeric(df["CO2 emissions (kt)"], errors="coerce")
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

prova = df.loc[df["Category"] == "Total national emissions and removals", 
               ["Category","CO2 emissions (kt)","Year"]].round(2)


path_policies = "D:/Python projects and excercises/co2-emissions-italy/data_processed/policies.csv"
policies = pd.read_csv(path_policies)
policies["Year"] = pd.to_numeric(policies["Year"], errors="coerce")
print(policies[["Year","Event"]].head(5))
