# src/ai/fraud_detection.py

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib

class FraudDetection:
    def __init__(self, data):
        self.data = data
        self.model = IsolationForest(contamination=0.01, random_state=42)

    def preprocess(self):
        """Preprocess the data for training."""
        # Example preprocessing steps
        self.data.fillna(0, inplace=True)  # Fill missing values
        self.data = pd.get_dummies(self.data)  # Convert categorical variables to dummy variables

    def train(self):
        """Train the fraud detection model."""
        self.preprocess()
        X = self.data.drop('is_fraud', axis=1)  # Features
        y = self.data['is_fraud']  # Target variable

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Fit the model
        self.model.fit(X_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        y_pred = [1 if x == -1 else 0 for x in y_pred]  # Convert -1 to 1 (fraud) and 1 to 0 (not fraud)

        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

    def detect(self, new_data):
        """Detect fraud in new transactions."""
        new_data.fillna(0, inplace=True)  # Fill missing values
        new_data = pd.get_dummies(new_data)  # Convert categorical variables to dummy variables
        predictions = self.model.predict(new_data)
        return [1 if x == -1 else 0 for x in predictions]  # Convert -1 to 1 (fraud) and 1 to 0 (not fraud)

    def save_model(self, filename='fraud_detection_model.pkl'):
        """Save the model to a file."""
        joblib.dump(self.model, filename)

    @staticmethod
    def load_model(filename='fraud_detection_model.pkl'):
        """Load the model from a file."""
        return joblib.load(filename)
