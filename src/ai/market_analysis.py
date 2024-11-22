# src/ai/market_analysis.py

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import joblib
import numpy as np
import matplotlib.pyplot as plt

class MarketAnalysis:
    def __init__(self, historical_data):
        self.historical_data = historical_data
        self.model = None

    def preprocess(self):
        """Preprocess the historical data for time series analysis."""
        self.historical_data['date'] = pd.to_datetime(self.historical_data['date'])
        self.historical_data.set_index('date', inplace=True)
        self.historical_data = self.historical_data.asfreq('D')  # Assuming daily frequency
        self.historical_data.fillna(method='ffill', inplace=True)  # Forward fill missing values

    def test_stationarity(self):
        """Perform the Augmented Dickey-Fuller test to check for stationarity."""
        result = adfuller(self.historical_data['price'])
        print('ADF Statistic:', result[0])
        print('p-value:', result[1])
        if result[1] <= 0.05:
            print("The time series is stationary.")
        else:
            print("The time series is not stationary. Consider differencing.")

    def fit(self, order=(1, 1, 1)):
        """Fit the ARIMA model."""
        self.preprocess()
        self.test_stationarity()
        self.model = ARIMA(self.historical_data['price'], order=order)
        self.model = self.model.fit()

    def forecast(self, steps=5):
        """Forecast future market trends."""
        if self.model is None:
            raise Exception("Model is not fitted yet.")
        forecast = self.model.forecast(steps=steps)
        return forecast

    def plot_forecast(self, steps=5):
        """Plot the historical data and forecasted values."""
        if self.model is None:
            raise Exception("Model is not fitted yet.")
        
        forecast = self.forecast(steps)
        plt.figure(figsize=(12, 6))
        plt.plot(self.historical_data['price'], label='Historical Data', color='blue')
        plt.plot(pd.date_range(start=self.historical_data.index[-1], periods=steps + 1, freq='D')[1:], 
                 forecast, label='Forecast', color='orange')
        plt.title('Market Price Forecast')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

    def save_model(self, filename='market_analysis_model.pkl'):
        """Save the model to a file."""
        joblib.dump(self.model, filename)

    @staticmethod
    def load_model(filename='market_analysis_model.pkl'):
        """Load the model from a file."""
        return joblib.load(filename)
