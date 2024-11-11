import statsmodels.api as sm
from matplotlib import pyplot as plt
from statsmodels.tsa.api import VAR
from statsmodels.stats.diagnostic import acorr_ljungbox
import pandas as pd


# The significant coefficients across all equations are those with p-values < 0.05
def var_forecast(df, energy_sources, forecast_steps, plot=True):
    max_lags = 3
    model = VAR(df[energy_sources])
    optimal_lags = model.select_order(maxlags=max_lags)  # Adjust maxlags as needed
    fitted_model = model.fit(maxlags=max_lags, ic='aic')

    # check if residuals are white noise
    for energy_source in energy_sources:
        lb_test = acorr_ljungbox(fitted_model.resid[energy_source], lags=[10], return_df=True)
        # print(f"Ljung-Box test for {energy_source}:")
        # print(lb_test)

    forecast_values = fitted_model.forecast(df[energy_sources].values[-fitted_model.k_ar:], steps=forecast_steps)
    forecast_df = pd.DataFrame(forecast_values,
                               index=pd.date_range(start=df.index[-1] + pd.Timedelta('1h'), periods=forecast_steps, freq='h'),
                               columns=energy_sources)

    print("Forecasted values:\n", forecast_df)

    if plot:
        plt.figure(figsize=(12, 6))
        num_actual_points = 0  # Plot last 10 times the forecast steps of actual data
        plt.xlim([df.index[-num_actual_points], forecast_df.index[-1]])  # Set x-axis limits to show the forecast clearly

        for energy_source in energy_sources:
            plt.plot(df.index[-num_actual_points:], df[energy_source].iloc[-num_actual_points:], label=f'Actual {energy_source}',
                     color='blue')  # Last actual data
            plt.plot(forecast_df.index, forecast_df[energy_source], label=f'Forecast {energy_source}', color='orange', linestyle='--')

        plt.title('Forecast vs Actual for Energy Sources')
        plt.xlabel('Date')
        plt.ylabel('Values')
        plt.legend()
        plt.grid()
        plt.show()

    print(forecast_df)
    return forecast_df

def sarima(df, energy_sources):
    sarima_models = {}

    for source in energy_sources:
        model = sm.tsa.statespace.SARIMAX(
            df[source].dropna(),
            order=(0, 1, 0),  # Adjust based on ACF/PACF
            seasonal_order=(0, 1, 0, 96)  # Adjust based on seasonality
        )
        sarima_models[source] = model.fit()
        print(f"{source} Model Summary:")
        print(sarima_models[source].summary())





