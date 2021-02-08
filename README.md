# predict-stock-price-arima
Predicting Stock Prices Using ARIMA Forecasting

# Problem: Forecasting Stock Prices using Time Series Modeling
After the Gamestop fiasco with the subredit Wallstreetbets, I became very interested in doing a project with the stock market. The purpose of this project is to see if I can forecast stock prices using time-series modeling

## Method: ARIMA

## Data: Stock market prices from TDAmeritrade API

## Libraries:
- numpy
- pandas
- statsmodels
- requests
- plotly
- matplotlib

# Results
- The AIC of our mode is small at -20964.701. But does this equate to a good model? Probably not.
- If we check the residuals (predictions - close price) the average difference is approximately 0.
    - However, the standard deviation is 12.6, which means 65% of the predictions were off by 0 +- 12.6, which may lead to significant losses.
- At one point the model prediction was off by -135 and 144, these trades would have resulted in enormous losses. 

# Future Work
Accuracy is important. The goal in the future will be reducing the width (standard deviation) of the distributions of residuals
