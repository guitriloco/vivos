"""
Local Model Trainer
Machine learning model for document classification
"""

import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib


class DocumentClassificationModel:
    def __init__(self, model_path=None):
        """
        Initialize the document classification model

        Args:
            model_path (str, optional): Path to a pre-trained model
        """
        self.model_path = model_path
        self.pipeline = None
        self.categories = []

        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self._create_pipeline()

    def _create_pipeline(self):
        """
        Create the ML pipeline for document classification
        """
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=10000,
                stop_words='english',
                lowercase=True,
                ngram_range=(1, 2)
            )),
            ('classifier', MultinomialNB(alpha=0.1))
        ])

    def train(self, texts, labels):
        """
        Train the model on text-label pairs

        Args:
            texts (list): List of document texts
            labels (list): List of corresponding labels/categories
        """
        if not texts or not labels:
            raise ValueError("Training data cannot be empty")

        self.categories = list(set(labels))
        self.pipeline.fit(texts, labels)
        print(f"Model trained on {len(texts)} documents with {len(self.categories)} categories")

    def predict(self, texts):
        """
        Predict categories for given texts

        Args:
            texts (list or str): Text or list of texts to classify

        Returns:
            list or str: Predicted category/categories
        """
        if isinstance(texts, str):
            texts = [texts]
            single_input = True
        else:
            single_input = False

        if self.pipeline is None:
            raise ValueError("Model not trained or loaded")

        predictions = self.pipeline.predict(texts)

        if single_input:
            return predictions[0]
        else:
            return predictions

    def predict_proba(self, texts):
        """
        Get prediction probabilities for given texts

        Args:
            texts (list or str): Text or list of texts to classify

        Returns:
            array: Prediction probabilities
        """
        if isinstance(texts, str):
            texts = [texts]

        if self.pipeline is None:
            raise ValueError("Model not trained or loaded")

        return self.pipeline.predict_proba(texts)

    def save_model(self, model_path):
        """
        Save the trained model to disk

        Args:
            model_path (str): Path where to save the model
        """
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump({
            'pipeline': self.pipeline,
            'categories': self.categories
        }, model_path)
        print(f"Model saved to {model_path}")
        self.model_path = model_path

    def load_model(self, model_path):
        """
        Load a pre-trained model from disk

        Args:
            model_path (str): Path to the saved model
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")

        loaded = joblib.load(model_path)
        self.pipeline = loaded['pipeline']
        self.categories = loaded['categories']
        self.model_path = model_path
        print(f"Model loaded from {model_path}")


class AdvancedDocumentClassificationModel(DocumentClassificationModel):
    """
    An advanced version that could potentially integrate with transformer models
    """
    def __init__(self, model_type='naive_bayes', model_path=None):
        """
        Initialize the advanced document classification model

        Args:
            model_type (str): Type of model to use ('naive_bayes', 'svm', etc.)
            model_path (str, optional): Path to a pre-trained model
        """
        self.model_type = model_type
        super().__init__(model_path)

    def _create_pipeline(self):
        """
        Create the ML pipeline based on the model type
        """
        from sklearn.svm import SVC
        from sklearn.linear_model import LogisticRegression

        vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words='english',
            lowercase=True,
            ngram_range=(1, 2)
        )

        if self.model_type == 'svm':
            classifier = SVC(kernel='linear', probability=True)
        elif self.model_type == 'logistic_regression':
            classifier = LogisticRegression(max_iter=1000)
        else:  # Default to Naive Bayes
            classifier = MultinomialNB(alpha=0.1)

        self.pipeline = Pipeline([
            ('tfidf', vectorizer),
            ('classifier', classifier)
        ])


if __name__ == "__main__":
    # Example usage
    model = DocumentClassificationModel()
    print("Document Classification Model initialized")
    print("Ready to train on document data")