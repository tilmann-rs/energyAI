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


# TIMES NET
#
# seq_len = 48  # Length of input sequence (e.g., 48 for the last 12 hours if data is 15 min intervals)
# pred_len = 12  # Length of the prediction sequence (e.g., 12 for the next 3 hours)
#
#
# # Select multiple energy sources
# data = df[energy_sources].values
#
# # Create sequences for the selected energy sources
# X, y = create_sequences(data, seq_len, pred_len)
#
#
# class Config:
#     def __init__(self):
#         self.seq_len = seq_len
#         self.pred_len = pred_len
#         self.label_len = 48
#         self.d_ff = 256
#         self.num_kernels = 2
#         self.top_k = 2
#         self.enc_in = 3  # Update this to the number of input features (e.g., 3 for Wind, Solar, Hydro)
#         self.d_model = 64  # Model dimension
#         self.embed = 'season'  # Embedding type
#         self.freq = 't'  # Frequency
#         self.dropout = 0.1
#         self.e_layers = 2  # Number of encoder layers
#         self.c_out = 3  # Update to the number of output features if predicting all sources
#         self.task_name = 'energy forecast'
#
#
# configs = Config()
#
#
# model = TimesNet(configs)
#
#
# with torch.no_grad():
#     predictions = model(X, None, X[:, -pred_len:, :], None)
#
# # Check the predictions shape
# print(predictions.shape)
#
# def plot_predictions(actual, predicted, title="Energy Source Predictions"):
#     plt.figure(figsize=(12, 6))
#     plt.plot(actual, label='Actual Values', color='blue')
#     plt.plot(predicted, label='Predicted Values', color='orange')
#     plt.title(title)
#     plt.xlabel('Time Steps')
#     plt.ylabel('Energy (MW)')
#     plt.legend()
#     plt.show()
#
#
# actual = y.detach().cpu().numpy()  # Actual values
# predicted = predictions.detach().cpu().numpy()  # Predicted values
#
# # Plot for the first sample
# sample_idx = 0  # Change this index to view different samples
# plot_predictions(actual[sample_idx], predicted[sample_idx], title="Energy Source Predictions")
#
#
#









