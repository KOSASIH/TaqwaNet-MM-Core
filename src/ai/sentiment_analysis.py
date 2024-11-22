# src/ai/sentiment_analysis.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
import torch
import joblib

class SentimentAnalysis:
    def __init__(self, data):
        self.data = data
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

    def preprocess(self):
        """Preprocess the data for training."""
        self.data['text'] = self.data['text'].astype(str)  # Ensure text is string
        self.data['label'] = self.data['label'].astype(int)  # Ensure labels are integers

    def tokenize_data(self):
        """Tokenize the text data."""
        return self.tokenizer(
            self.data['text'].tolist(),
            padding=True,
            truncation=True,
            return_tensors='pt',
            max_length=512
        )

    def train(self):
        """Train the sentiment analysis model."""
        self.preprocess()
        inputs = self.tokenize_data()
        labels = torch.tensor(self.data['label'].tolist())

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(inputs['input_ids'], labels, test_size=0.2, random_state=42)

        # Create a dataset class
        train_dataset = torch.utils.data.TensorDataset(X_train, y_train)
        test_dataset = torch.utils.data.TensorDataset(X_test, y_test)

        # Set training arguments
        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=3,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10,
            evaluation_strategy="epoch"
        )

        # Create a Trainer instance
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=test_dataset
        )

        # Train the model
        trainer.train()

        # Evaluate the model
        predictions, labels, _ = trainer.predict(test_dataset)
        preds = predictions.argmax(axis=1)

        print("Confusion Matrix:")
        print(confusion_matrix(y_test, preds))
        print("\nClassification Report:")
        print(classification_report(y_test, preds))

    def predict(self, new_texts):
        """Predict sentiment for new texts."""
        self.model.eval()
        inputs = self.tokenizer(new_texts, padding=True, truncation=True, return_tensors='pt', max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        predictions = outputs.logits.argmax(axis=1).numpy()
        return predictions

    def save_model(self, model_path='sentiment_model'):
        """Save the model to a directory."""
        self.model.save_pretrained(model_path)
        self.tokenizer.save_pretrained(model_path)

    @staticmethod
    def load_model(model_path='sentiment_model'):
        """Load the model from a directory."""
        model = BertForSequenceClassification.from_pretrained(model_path)
        tokenizer = BertTokenizer.from_pretrained(model_path)
        return model, tokenizer
