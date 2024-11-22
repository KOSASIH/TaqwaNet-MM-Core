# predictive_analytics.py

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

class PredictiveAnalytics:
    def __init__(self, data):
        self.data = data

    def train_model(self, order=(5, 1, 0)):
        model = ARIMA(self.data, order=order)
        self.model_fit = model.fit()
        print(self.model_fit.summary())

    def forecast(self, steps=5):
        forecast = self.model_fit.forecast(steps=steps)
        return forecast

    def plot_forecast(self, steps=5):
        forecast = self.forecast(steps)
        plt.figure(figsize=(10, 5))
        plt.plot(self.data, label='Historical Data')
        plt.plot(range(len(self.data), len(self.data) + steps), forecast, label='Forecast', color='red')
        plt.legend()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Load your time series data
    data = pd.read_csv('market_data.csv', parse_dates=['date'], index_col='date')
    market_data = data['price']  # Assuming 'price' is the column to forecast

    predictor = PredictiveAnalytics(market_data)
    predictor.train_model(order =(5, 1, 0))
    predictor.plot_forecast(steps=10)
