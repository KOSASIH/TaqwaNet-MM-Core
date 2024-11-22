# src/security/intrusion_detection.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

class IntrusionDetection:
    def __init__(self, data_path):
        """Initialize the IntrusionDetection class."""
        self.data_path = data_path
        self.model = IsolationForest(contamination=0.1)  # Assume 10% of data is anomalous
        self.data = None
        self.features = None
        self.labels = None

    def load_data(self):
        """Load the dataset from the specified path."""
        self.data = pd.read_csv(self.data_path)
        print("Data loaded successfully.")
        print(self.data.head())

    def preprocess_data(self):
        """Preprocess the data for training."""
        # Assuming the last column is the label (0 for normal, 1 for attack)
        self.features = self.data.iloc[:, :-1].values
        self.labels = self.data.iloc[:, -1].values

    def train_model(self):
        """Train the Isolation Forest model."""
        self.model.fit(self.features)
        print("Model trained successfully.")

    def detect_intrusions(self):
        """Detect intrusions in the dataset."""
        predictions = self.model.predict(self.features)
        # Convert predictions: -1 for anomalies, 1 for normal
        predictions = np.where(predictions == -1, 1, 0)
        return predictions

    def evaluate_model(self, predictions):
        """Evaluate the model's performance."""
        print("Confusion Matrix:")
        print(confusion_matrix(self.labels, predictions))
        print("\nClassification Report:")
        print(classification_report(self.labels, predictions))

# Example usage
if __name__ == "__main__":
    # Path to the dataset (CSV file)
    data_path = 'path/to/your/network_traffic_data.csv'

    intrusion_detection = IntrusionDetection(data_path)

    # Load and preprocess the data
    intrusion_detection.load_data()
    intrusion_detection.preprocess_data()

    # Train the model
    intrusion_detection.train_model()

    # Detect intrusions
    predictions = intrusion_detection.detect_intrusions()

    # Evaluate the model
    intrusion_detection.evaluate_model(predictions)
