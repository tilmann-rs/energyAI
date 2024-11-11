import matplotlib.pyplot as plt
import torch

from data_load.preprocess import preprocess_data, country_years
from data_load.visualize import plot_data
from data_load.data_analytics import mean_seasonality, check_missing_values, check_monotonicity
from model.simple_tsf import sarima, var_forecast
from model.TimesNet import Model as TimesNet

# shortened_columns = {
#     "Biomass  - Actual Aggregated [MW]": "Biomass",
#     "Fossil Brown coal/Lignite  - Actual Aggregated [MW]": "Br. Coal",
#     "Fossil Coal-derived gas  - Actual Aggregated [MW]": "Coal Gas",
#     "Fossil Gas  - Actual Aggregated [MW]": "Gas",
#     "Fossil Hard coal  - Actual Aggregated [MW]": "Hard Coal",
#     "Fossil Oil  - Actual Aggregated [MW]": "Oil",
#     "Fossil Oil shale  - Actual Aggregated [MW]": "Oil Shale",
#     "Fossil Peat  - Actual Aggregated [MW]": "Peat",
#     "Geothermal  - Actual Aggregated [MW]": "Geoth.",
#     "Hydro Pumped Storage  - Actual Aggregated [MW]": "Hydr PS",
#     "Hydro Pumped Storage  - Actual Consumption [MW]": "(C) Hydr PS",
#     "Hydro Run-of-river and poundage  - Actual Aggregated [MW]": "Hydr River",
#     "Hydro Water Reservoir  - Actual Aggregated [MW]": "Water Res",
#     "Marine  - Actual Aggregated [MW]": "Marine",
#     "Nuclear  - Actual Aggregated [MW]": "Nuclear",
#     "Other  - Actual Aggregated [MW]": "Other",
#     "Other renewable  - Actual Aggregated [MW]": "Other Renewabl",
#     "Solar  - Actual Aggregated [MW]": "Solar",
#     "Waste  - Actual Aggregated [MW]": "Waste",
#     "Wind Offshore  - Actual Aggregated [MW]": "Wind Off",
#     "Wind Onshore  - Actual Aggregated [MW]": "Wind On"
# }

country = "Germany"
year_from = "2023"
year_to = "2023"
path = 'data/Big Electricity'

df = country_years(country, year_from, year_to, f'../data/{country}', path)

energy_sources = ["Wind On"]
energy_sources_str = "_".join([source.replace(" ", "") for source in energy_sources])
# save specific source
df[['date'] + energy_sources].to_csv(f"{path}/{country}/{country}_{year_from}-{year_to}_{energy_sources_str}.csv", index=False)


# df = mean_seasonality(df, 'W')
# plot_data(df, energy_sources)

# adf_test(df, energy_sources)

