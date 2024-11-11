from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

# If confidence over 0% than SARIMA, VAR,... can be used
# A p-value less than 0.05 indicates stationarity
# The ADF Statistic is a negative number.
# (The more negative it is, the stronger the evidence that the time series is stationary)
def adf_test(df, energy_sources):
    results = []

    for source in energy_sources:
        adf_result = adfuller(df[source])

        adf_statistic = adf_result[0]
        p_value = adf_result[1]
        critical_values = adf_result[4]

        # Determine if the series is stationary based on critical values and p-value
        if adf_statistic < critical_values['1%']:
            confidence = 99
        elif adf_statistic < critical_values['5%']:
            confidence = 95
        elif adf_statistic < critical_values['10%']:
            confidence = 90
        else:
            confidence = 0  # Non-stationary

        # IF NOT STATIONARY DIFFERENCING POSSIBLE TO MAKE STATIONARY
        # df['Wind Onshore Diff'] = df['Wind Onshore Actual [MW]'].diff()

        # print((source, confidence))
        results.append((source, confidence))

    return results
# EDA - Explanatory Data Analysis

# Check for missing values
def check_missing_values(df):
    missing_values = df.isnull().sum()
    print(missing_values[missing_values > 0])  # Display only columns with missing values
    return missing_values[missing_values > 0]

def check_monotonicity(df, energy_sources):

    results = []

    for source in energy_sources:
        is_increasing = df[source].is_monotonic_increasing
        is_decreasing = df[source].is_monotonic_decreasing
        results.append({
            'Energy Source': source,
            'Monotonic Increasing': is_increasing,
            'Monotonic Decreasing': is_decreasing
        })

    print(results)
    return results

# LAG ANALYSIS
# Assuming `df` is your DataFrame and 'Wind Onshore Actual [MW]' is the target column
# plot_acf(df['Wind Onshore Actual [MW]'], lags=30)
# plt.title('ACF Plot')
# plt.show()
#
# plot_pacf(df['Wind Onshore Actual [MW]'], lags=30)
# plt.title('PACF Plot')
# plt.show()
#
#
# # AUTOCORRELATION
# from pandas.plotting import autocorrelation_plot
# autocorrelation_plot(df['Wind On'])
# plt.show()
#
#
# # Add lag features (e.g., the previous hour's value)
# df['Wind Onshore Lag1'] = df['Wind Onshore Actual [MW]'].shift(1)
#
# # Add time-based features
# df['Hour'] = df.index.hour
# df['DayOfWeek'] = df.index.dayofweek
# df['Month'] = df.index.month


# statistical overview
# print(df.describe())


# SEASONALITY mean, f.e. season = 'M'
def mean_seasonality(df, season):
    df_season = df.resample(season).mean()
    return df_season


#
# # CORRELATION
# import seaborn as sns
#
# def corr_matrix(df):
#     correlation_matrix = df.corr()
#     return correlation_matrix
#
# plt.figure(figsize=(10, 8))
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
# plt.title('Correlation Matrix of Energy Sources')
# plt.show()
# # Plot the heatmap of the correlation matrix
