# src/services/personalized_advisory.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

class PersonalizedAdvisory:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    def prepare_data(self, user_data):
        # Convert user data to DataFrame
        df = pd.DataFrame(user_data)
        
        # Feature engineering (example)
        df['risk_score'] = self.calculate_risk_score(df)
        
        return df

    def calculate_risk_score(self, df):
        # Placeholder for risk score calculation logic
        return df['investment_experience'] * 0.5 + df['age'] * 0.3

    def generate_advice(self, user_data):
        prepared_data = self.prepare_data(user_data)
        predictions = self.model.predict(prepared_data)
        
        advice = []
        for prediction in predictions:
            if prediction == 1:
                advice.append("Consider investing in stocks.")
            else:
                advice.append("Consider safer investment options.")
        
        return advice

if __name__ == "__main__":
    # Load user data (example)
    user_data = [
        {"investment_experience": 5, "age": 30},
        {"investment_experience": 2, "age": 45}
    ]
    
    advisory_service = PersonalizedAdvisory("path/to/model.joblib")
    advice = advisory_service.generate_advice(user_data)
    
    for a in advice:
        print(a)
