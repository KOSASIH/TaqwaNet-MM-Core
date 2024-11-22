import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Any

class FraudDetectionService:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)  # Adjust contamination based on expected fraud rate
        self.transaction_data: List[List[float]] = []  # Store transaction features
        self.scaler = StandardScaler()  # Standardize features

    def add_transaction(self, transaction: List[float]):
        """Add transaction data for fraud detection."""
        self.transaction_data.append(transaction)

    def train_model(self):
        """Train the fraud detection model."""
        if not self.transaction_data:
            raise Exception("No transaction data available for training.")
        
        # Convert transaction data to a suitable format for training
        X = np.array(self.transaction_data)
        X_scaled = self.scaler.fit_transform(X)  # Standardize the data
        self.model.fit(X_scaled)

    def detect_fraud(self, transaction: List[float]) -> bool:
        """Detect fraud in a new transaction."""
        if not self.model:
            raise Exception("Model has not been trained yet.")
        
        # Standardize the new transaction
        transaction_scaled = self.scaler.transform([transaction])
        prediction = self.model.predict(transaction_scaled)
        return prediction[0] == -1  # -1 indicates a potential fraud

    def get_model(self):
        """Get the trained model."""
        return self.model

# Example usage
if __name__ == "__main__":
    # Initialize the fraud detection service
    fraud_service = FraudDetectionService()

    # Add some sample transaction data (features could include amount, time, user ID, etc.)
    fraud_service.add_transaction([100, 1])  # Normal transaction
    fraud_service.add_transaction([10000, 2])  # Potential fraud transaction
    fraud_service.add_transaction([150, 1])  # Normal transaction
    fraud_service.add_transaction([20000, 3])  # Potential fraud transaction

    # Train the model with the added transactions
    fraud_service.train_model()

    # Detect fraud in a new transaction
    new_transaction = [150, 1]  # Example of a new transaction
    is_fraud = fraud_service.detect_fraud(new_transaction)
    print(f"Transaction {new_transaction} is {'fraudulent' if is_fraud else 'legitimate'}.")

    # Test with another transaction
    suspicious_transaction = [25000, 4]  # Example of a suspicious transaction
    is_fraud = fraud_service.detect_fraud(suspicious_transaction)
    print(f"Transaction {suspicious_transaction} is {'fraudulent' if is_fraud else 'legitimate'}.")
