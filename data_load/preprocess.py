import os

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

    df = df.groupby(df.index).mean() # Average duplicate entries

    df = df.asfreq('15min')  # Set frequency to 15 minutes

    df.interpolate(method='linear', inplace=True)   # Interpolate missing values

    df.sort_index(inplace=True)

    # print(df.iloc[:, from_column_shown:to_column_shown].head())
    return df


def country_years(country, start_year, end_year, source, target):
    # Define the file path pattern and find all matching files
    source_files = f"{source}/*.csv"
    files = glob.glob(source_files)
    target_file = f"{target}/{country}/{country}_{start_year}-{end_year}.csv"
    df = None
    os.makedirs(f"{target}/{country}", exist_ok=True)

    # Filter files based on the year range
    filtered_files = []
    for file in files:
        # Extract the start year from the filename
        match = re.search(r'_(\d{4})01010000-', file)
        if match:
            file_year = int(match.group(1))
            if int(start_year) <= file_year <= int(end_year):
                filtered_files.append(file)

    # Concatenate and save if any files match
    if filtered_files:
        all_data = pd.concat([pd.read_csv(f) for f in filtered_files])
        clean_data = preprocess_data(all_data)
        clean_data.to_csv(target_file, index=True)   # save the file
        df = pd.read_csv(target_file)
    else:
        print("No files found within the specified year range. Its 2015 to 2024 available")

    return df
