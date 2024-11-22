# src/ai/recommendation_engine.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import numpy as np

class RecommendationEngine:
    def __init__(self, user_data, item_data):
        self.user_data = user_data
        self.item_data = item_data
        self.tfidf_vectorizer = TfidfVectorizer()
        self.item_similarity = None
        self.user_item_matrix = None

    def fit(self):
        """Fit the model using user and item data."""
        self.user_item_matrix = self.user_data.pivot(index='user_id', columns='item_id', values='rating').fillna(0)
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.item_data['description'])
        self.item_similarity = cosine_similarity(tfidf_matrix)

    def recommend(self, user_id, top_n=5):
        """Recommend items for a given user based on their preferences."""
        if user_id not in self.user_item_matrix.index:
            return []

        user_vector = self.user_item_matrix.loc[user_id].values
        scores = self.item_similarity.dot(user_vector)
        recommended_indices = np.argsort(scores)[-top_n:][::-1]
        return self.item_data.iloc[recommended_indices]['item_id'].tolist()

    def evaluate(self, test_data):
        """Evaluate the recommendation engine using RMSE."""
        y_true = []
        y_pred = []
        
        for _, row in test_data.iterrows():
            user_id = row['user_id']
            item_id = row['item_id']
            true_rating = row['rating']
            y_true.append(true_rating)
            recommendations = self.recommend(user_id, top_n=10)
            if item_id in recommendations:
                y_pred.append(true_rating)  # Assuming the predicted rating is the true rating for simplicity
            else:
                y_pred.append(0)  # No recommendation

        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        return rmse

    def save_model(self, filename='recommendation_model.pkl'):
        """Save the model to a file."""
        joblib.dump(self, filename)

    @staticmethod
    def load_model(filename='recommendation_model.pkl'):
        """Load the model from a file."""
        return joblib.load(filename)
