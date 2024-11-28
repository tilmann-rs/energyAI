import os

import numpy as np
import pandas as pd
import glob
import re

from_column_shown = 0
to_column_shown = 19  # after NaN colums
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)         # Set display width (adjust based on your screen size)
pd.set_option('display.max_colwidth', None)  # No limit on column width
pd.set_option('display.colheader_justify', 'left')  # Prevent wrapping of header text


# Shortened column label
shortened_columns = {
    "Biomass  - Actual Aggregated [MW]": "Biomass",
    "Fossil Brown coal/Lignite  - Actual Aggregated [MW]": "Br. Coal",
    "Fossil Coal-derived gas  - Actual Aggregated [MW]": "Coal Gas",
    "Fossil Gas  - Actual Aggregated [MW]": "Gas",
    "Fossil Hard coal  - Actual Aggregated [MW]": "Hard Coal",
    "Fossil Oil  - Actual Aggregated [MW]": "Oil",
    "Fossil Oil shale  - Actual Aggregated [MW]": "Oil Shale",
    "Fossil Peat  - Actual Aggregated [MW]": "Peat",
    "Geothermal  - Actual Aggregated [MW]": "Geoth.",
    "Hydro Pumped Storage  - Actual Aggregated [MW]": "Hydr PS",
    "Hydro Pumped Storage  - Actual Consumption [MW]": "(C) Hydr PS",
    "Hydro Run-of-river and poundage  - Actual Aggregated [MW]": "Hydr River",
    "Hydro Water Reservoir  - Actual Aggregated [MW]": "Water Res",
    "Marine  - Actual Aggregated [MW]": "Marine",
    "Nuclear  - Actual Aggregated [MW]": "Nuclear",
    "Other  - Actual Aggregated [MW]": "Other",
    "Other renewable  - Actual Aggregated [MW]": "Other Renewabl",
    "Solar  - Actual Aggregated [MW]": "Solar",
    "Waste  - Actual Aggregated [MW]": "Waste",
    "Wind Offshore  - Actual Aggregated [MW]": "Wind Off",
    "Wind Onshore  - Actual Aggregated [MW]": "Wind On"
}


def preprocess_data(df):

    df.rename(columns=shortened_columns, inplace=True)

    if 'Area' in df.columns:        # Removin Area colum (non numeric)
        df.drop(columns=['Area'], inplace=True)

    no_value_columns = [col for col in df.columns if (df[col].iloc[:1] == "n/e").all()]
    df = df.drop(columns=no_value_columns)      # df cleaned from columns with all "n/e" values

    df['date'] = pd.to_datetime(df['MTU'].str.split(' - ').str[0], format='%d.%m.%Y %H:%M')      # convert to datetime format

    df.set_index('date', inplace=True)       # set 'MTU' as the index for easier time series manipulation
    df.drop(columns=['MTU'], inplace=True)

    # Convert remaining columns to numeric (if needed), with non-numeric values handled as NaN
    for col in df.columns[2:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.groupby(df.index).mean()  # Average duplicate entries

    df = df.asfreq('15min')  # Set frequency to 15 minutes

    df.interpolate(method='linear', inplace=True)   # Interpolate missing values

    df.sort_index(inplace=True)

    # print(df.iloc[:, from_column_shown:to_column_shown].head())
    return df


def prepare_energy_data(country, start_year, end_year, features, source, target, correlation_calc=False, time_stamp_saved_seperately=False, index=False, header=False):
    # Define the file path pattern and find all matching files
    source_files = f"{source}/*.csv"
    files = glob.glob(source_files)
    clean_data = None
    os.makedirs(f"{target}", exist_ok=True)

    # Filter files based on the year range
    filtered_files = []
    for file in files:
        # Extract the start year from the filename
        match = re.search(r'_(\d{4})01010000-', file)
        if match:
            file_year = int(match.group(1))
            if int(start_year) <= file_year <= int(end_year):
                filtered_files.append(file)

    # Concatenate
    if filtered_files:
        all_data = pd.concat([pd.read_csv(f) for f in filtered_files])
        clean_data = preprocess_data(all_data)

        # SAVE all available features or
        if features is None:
            file_name = f"{country}_{start_year}-{end_year}"
            df = clean_data

        # SAVE specific features
        else:
            energy_sources_str = "_".join([feature.replace(" ", "") for feature in features])
            file_name = f"{country}_{start_year}-{end_year}_{energy_sources_str}"
            df = clean_data[features]

        df.to_csv(f"{target}/{file_name}.csv", index=index, header=header)
        if correlation_calc:
            save_correlation(df, target, file_name)
        if time_stamp_saved_seperately:
            separate_timestamps(df, target, file_name)

        print(f"Files saved at {target}.")
    else:
        print("No files found within the specified year range. Normally its 2015 to 2024 available")

    return clean_data


def save_correlation(df, target, file):
    corr_mat = df.corr()
    target_file_corr = "corr_" + file
    corr_mat.to_csv(f"{target}/Correlations/{target_file_corr}.csv", index=False, header=False)

def separate_timestamps(df, target, file):
    # save as csv and npy
    clean_data_no_index = df.reset_index()

    target_file_timestamps = "ts_" + file
    clean_data_no_index['date'].to_csv(f"{target}/Timestamps/{target_file_timestamps}.csv", index=False, header=False)

    timestamps = clean_data_no_index['date'].values
    timestamps_unix = timestamps.astype('datetime64[s]').view(np.int64)
    target_file_timestamps = "ts_" + file
    np.save(f"{target}/Timestamps/{target_file_timestamps}.npy", timestamps_unix)
