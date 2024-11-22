# src/ai/predictive_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

class PredictiveModel:
    def __init__(self, data):
        self.data = data
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def preprocess(self):
        """Preprocess the data for training."""
        # Example preprocessing steps
        self.data.fillna(0, inplace=True)  # Fill missing values
        self.data = pd.get_dummies(self.data)  # Convert categorical variables to dummy variables

    def train(self):
        """Train the predictive model."""
        self.preprocess()
        X = self.data.drop('target', axis=1)  # Features
        y = self.data['target']  # Target variable

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Fit the model
        self.model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print("Mean Squared Error:", mse)
        print("R^2 Score:", r2)

    def predict(self, new_data):
        """Predict using the trained model."""
        new_data.fillna(0, inplace=True)  # Fill missing values
        new_data = pd.get_dummies(new_data)  # Convert categorical variables to dummy variables
        predictions = self.model.predict(new_data)
        return predictions

    def save_model(self, filename='predictive_model.pkl'):
        """Save the model to a file."""
        joblib.dump(self.model, filename)

    @staticmethod
    def load_model(filename='predictive_model.pkl'):
        """Load the model from a file."""
        return joblib.load(filename)
