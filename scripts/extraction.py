import pandas as pd
import re
import glob

path = "data_raw/ITA-CRT-2025-V0.2-1990-20250313-134808_started.xlsx"

def extract_year(path: str):
    years = re.findall(r"19\d{2}|20\d{2}", path)
    return int(years[1])


def process_single(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="Summary1", header=7)

    #Extracting data

    df2 = df.rename(columns={
        "GREENHOUSE GAS SOURCE AND SINK CATEGORIES":"Category", 
        "Net CO2 _x000d_\nemissions/_x000d_\nremovals":"CO2 emissions (kt)"
        })

    df2 = df2[["Category", "CO2 emissions (kt)"]]

    #Cleaning up data

    df2 = df2.fillna("0")
    main_cat = df2[df2["Category"].str.match(r"\d+\.\s") | df2["Category"].str.contains("Total national emissions and removals")].copy()

    main_cat.loc[:,"CO2 emissions (kt)"] = pd.to_numeric(main_cat["CO2 emissions (kt)"], errors="coerce")

    main_cat.loc[:,"Category"] = main_cat["Category"].replace({
        "4.  Land use, land-use change and forestry  (5)": "4.  Land use, land-use change and forestry",
        "6.  Other   (please specify) (7)": "6.  Other   (please specify)"})
    
    #Adding year column

    year = extract_year(path)
    main_cat.loc[:,"Year"] = year

    #Adding no LULUCF emissions

    total_em = main_cat.loc[
    main_cat["Category"] == "Total national emissions and removals",
    "CO2 emissions (kt)"
    ].iloc[0]

    lulucf = main_cat.loc[main_cat["Category"] == "4.  Land use, land-use change and forestry",
                          "CO2 emissions (kt)"].iloc[0]
    no_lulucf_em = total_em - lulucf

    main_cat.loc[len(main_cat)] = {
        "Category": "Emissions without LULUCF",
        "CO2 emissions (kt)": no_lulucf_em,
        "Year": year
    }
    return main_cat

#Creating a dataframe with all years

paths = sorted(glob.glob("data_raw/*.xlsx"))
frames = []
for path in paths:
    try:
        frames.append(process_single(path))
    except Exception as e:
        print(f"[SKIP]: {path}; {e}")

complete_df = pd.concat(frames, ignore_index=True).sort_values(["Year","Category"])
complete_df.to_csv("data_processed/co2_emissions_all_years.csv", index=False)

print("Total rows:", len(complete_df))
print("Saved in: data_processed/co2_emissions_by_sector_all_years.csv")
