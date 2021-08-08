# These are the functions used throughout the Jupyter notebook
# Feel free to copy and play with them in your own environment

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARMA

def get_data(symbol,
             client_id,
             periodType = 'year',
             n_periods = 20,
             frequencyType = 'daily',
             frequency = 1):
    """
    Yields a dataframe of  close price data for the given parameters
    
    --Parameters--
    
    symbol: Ticker symbol
    
    periodType: The type of period to show. Valid values are day, month, year, or ytd (year to date). Default is            day.
        
    n_periods: 	The number of periods to show.

        Example: For a 2 day / 1 min chart, the values would be:

        period: 2
        periodType: day
        frequency: 1
        frequencyType: min

        Valid periods by periodType (defaults marked with an asterisk):

        day: 1, 2, 3, 4, 5, 10*
        month: 1*, 2, 3, 6
        year: 1*, 2, 3, 5, 10, 15, 20
        ytd: 1*

    frequencyType: The type of frequency with which a new candle is formed. Valid frequencyTypes by periodType              (defaults marked with an asterisk):

        day: minute*
        month: daily, weekly*
        year: daily, weekly, monthly*
        ytd: daily, weekly*
    
    frequency: The number of the frequencyType to be included in each candle.

        Valid frequencies by frequencyType (defaults marked with an asterisk):

        minute: 1*, 5, 10, 15, 30
        daily: 1*
        weekly: 1*
        monthly: 1*
    
    """  
    # Initialize parameters
    parameters = {
        'apikey': client_id,
        'periodType': periodType,
        'period': str(n_periods),
        'frequencyType': frequencyType,
        'frequency': str(frequency),
    }
    
    # Request from API
    api_url = f'https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory'
    data = requests.get(url = api_url, params = parameters).json()
    
    # Create dataframe
    dataframe = pd.DataFrame(data['candles'])

    # Convert to datetime format
    for i in range(len(dataframe['datetime'])):
        dataframe['datetime'][i] = datetime.fromtimestamp(dataframe['datetime'][i]/1000)
    
    # Set datetime to be our index
    dataframe = dataframe.set_index('datetime')

    # Remove open, high, low, and volumn columns.
    # For this project, we will be working only with the close price
    dataframe.drop(labels=[
                            'open',
                            'high',
                            'low',
                            'volume'
                            ], axis=1,
                            inplace=True
                    )
    
    return dataframe, symbol

def calc_return(dataframe, lag = 1):
    """
    Adds a column of the previous close to the dataframe. Lag is a user-input parameter.
    """
    prevClose = [x for x in dataframe['close'][:-lag]]
    prevClose = [np.nan for i in range(lag)] + prevClose
    dataframe[f'{lag}-day prevClose'] = prevClose
    dataframe['return'] = np.log(dataframe[f'{lag}-day prevClose']).diff()
    
    return dataframe

def mean_std(dataframe, length=20):
    """
    Adds 2 columns to our dataframe: A rolling mean and standard deviations of user-defined lengths
    """
    dataframe[f'sma{length}'] = dataframe['return'].rolling(length).mean()
    dataframe[f'std{length}'] = dataframe['return'].rolling(length).std()
    # Remove leading NaNs
    dataframe.dropna(inplace=True)

# The code below is  the process to plot the forecasted results
# Define number of steps to take
steps = 2

# Define forecast array for 2 days into the future
forecast = ar1.forecast(steps=steps)[0]
forecast1 = dataframe['close'][-1] * (1 + forecast[0])
forecast2 = forecast1 * (1 + forecast[1])
forecast_array = np.array([forecast1, forecast2])

# Plot close price
plt.figure(figsize=(12, 8))
plt.plot(dataframe['close'][-200:].values, color='blue')

# Plot predicted close price
preds=dataframe['predictions'][-200:].values
plt.plot(preds, color='red')

# Plot forecasts
plt.plot(
    pd.DataFrame(
        np.array(
            [
                preds[-1], forecast1
            ]
        ).T,
        index = range(
            len(
                dataframe['close'][-200:].values
            ) + 1,
            len(
                dataframe['close'][-200:].values
            ) + 3
        )
    ), color='green'
)

plt.plot(
    pd.DataFrame(
        forecast_array,
        index = range(
            len(
                dataframe['close'][-200:].values
            ) + 1,
            len(
                dataframe['close'][-200:].values
            ) + 1 + steps
        )
    ), color = 'green'
)

plt.title('Google Forecasted Price')
plt.show()