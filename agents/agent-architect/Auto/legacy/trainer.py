"""
Local Model Trainer
Training logic module
"""

import os
import json
import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime
import importlib.util
import os

# Add the current directory to the path to import model
spec = importlib.util.spec_from_file_location("model", os.path.join(os.path.dirname(__file__), "model.py"))
model_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model_module)
DocumentClassificationModel = model_module.DocumentClassificationModel
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib


class ModelTrainer:
    def __init__(self, models_dir):
        """
        Initialize the model trainer

        Args:
            models_dir (str): Directory to save trained models
        """
        self.models_dir = models_dir
        self.model = None

        # Ensure models directory exists
        os.makedirs(models_dir, exist_ok=True)

    def load_training_data_from_history(self, history_db_path, min_confidence=0.7):
        """
        Load training data from classification history database

        Args:
            history_db_path (str): Path to the history database
            min_confidence (float): Minimum confidence score to include in training

        Returns:
            tuple: (texts, labels) for training
        """
        if not os.path.exists(history_db_path):
            raise FileNotFoundError(f"History database not found: {history_db_path}")

        conn = sqlite3.connect(history_db_path)
        cursor = conn.cursor()

        # Query to get documents with sufficient confidence and feedback
        query = '''
            SELECT document_path, assigned_category, confidence_score, metadata
            FROM classifications
            WHERE confidence_score >= ? AND feedback_status = 'positive'
        '''

        cursor.execute(query, (min_confidence,))
        rows = cursor.fetchall()

        texts = []
        labels = []

        for row in rows:
            doc_path, category, confidence, metadata_json = row

            # Try to extract text from the document
            text_content = self._extract_text_from_document(doc_path)
            if text_content and len(text_content.strip()) > 10:  # Only add if we have meaningful text
                texts.append(text_content)
                labels.append(category)

        conn.close()

        print(f"Loaded {len(texts)} training samples from history database")
        return texts, labels

    def _extract_text_from_document(self, doc_path):
        """
        Extract text content from a document path
        For now, this is a simplified version that assumes text files or tries to read any file as text

        Args:
            doc_path (str): Path to the document

        Returns:
            str: Extracted text content
        """
        try:
            # For PDF files, we'd normally use PyMuPDF, but for this trainer we'll try a general approach
            if doc_path.lower().endswith('.pdf'):
                # For now, return a placeholder - in a full implementation, we'd extract actual text
                return f"Content of {os.path.basename(doc_path)}"  # Placeholder
            else:
                # For text files
                with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(10000)  # Limit to first 10K characters
                return content
        except Exception:
            # If we can't read the file, return a placeholder
            return f"Content of {os.path.basename(doc_path)}"  # Placeholder

    def train_model(self, texts, labels, model_name=None):
        """
        Train a new model with the provided data

        Args:
            texts (list): List of document texts
            labels (list): List of corresponding labels
            model_name (str, optional): Name for the model

        Returns:
            str: Path to the saved model
        """
        if len(texts) == 0 or len(labels) == 0:
            raise ValueError("Training data is empty")

        if len(texts) != len(labels):
            raise ValueError("Texts and labels must have the same length")

        # Create and train the model
        self.model = DocumentClassificationModel()
        self.model.train(texts, labels)

        # Generate model name if not provided
        if model_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_name = f"document_classifier_{timestamp}"

        # Save the model
        model_path = os.path.join(self.models_dir, f"{model_name}.joblib")
        self.model.save_model(model_path)

        return model_path

    def evaluate_model(self, texts, labels):
        """
        Evaluate the current model on the provided data

        Args:
            texts (list): List of document texts
            labels (list): List of corresponding labels

        Returns:
            dict: Evaluation metrics
        """
        if self.model is None:
            raise ValueError("No model trained or loaded")

        # Split data for evaluation
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels if len(set(labels)) <= min(len(labels)//2, 10) else None
        )

        # Train on training set
        temp_model = DocumentClassificationModel()
        temp_model.train(X_train, y_train)

        # Predict on test set
        y_pred = temp_model.predict(X_test)

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)

        return {
            'accuracy': accuracy,
            'classification_report': report,
            'test_samples': len(y_test),
            'train_samples': len(y_train)
        }

    def train_from_history(self, history_db_path, min_confidence=0.7, model_name=None):
        """
        Train a model directly from classification history

        Args:
            history_db_path (str): Path to the history database
            min_confidence (float): Minimum confidence score to include in training
            model_name (str, optional): Name for the model

        Returns:
            dict: Training results
        """
        print("Loading training data from history...")
        texts, labels = self.load_training_data_from_history(history_db_path, min_confidence)

        if len(texts) == 0:
            raise ValueError("No suitable training data found in history database")

        print(f"Training model on {len(texts)} samples...")
        model_path = self.train_model(texts, labels, model_name)

        print("Evaluating model...")
        evaluation = self.evaluate_model(texts, labels)

        results = {
            'model_path': model_path,
            'training_samples': len(texts),
            'evaluation': evaluation,
            'timestamp': datetime.now().isoformat()
        }

        print(f"Model training completed. Saved to: {model_path}")
        return results

    def load_model(self, model_path):
        """
        Load a pre-trained model

        Args:
            model_path (str): Path to the saved model
        """
        self.model = DocumentClassificationModel(model_path)
        print(f"Model loaded from {model_path}")

    def predict_with_model(self, texts):
        """
        Use the loaded model to make predictions

        Args:
            texts (list or str): Text or list of texts to classify

        Returns:
            list or str: Predicted category/categories
        """
        if self.model is None:
            raise ValueError("No model loaded. Train or load a model first.")

        return self.model.predict(texts)

    def batch_predict(self, document_paths):
        """
        Make predictions for a batch of documents

        Args:
            document_paths (list): List of document paths to classify

        Returns:
            list: List of prediction results
        """
        results = []
        for doc_path in document_paths:
            try:
                text_content = self._extract_text_from_document(doc_path)
                if text_content and len(text_content.strip()) > 10:
                    predicted_category = self.predict_with_model(text_content)
                    results.append({
                        'document_path': doc_path,
                        'predicted_category': predicted_category,
                        'success': True
                    })
                else:
                    results.append({
                        'document_path': doc_path,
                        'error': 'Could not extract text',
                        'success': False
                    })
            except Exception as e:
                results.append({
                    'document_path': doc_path,
                    'error': str(e),
                    'success': False
                })

        return results


if __name__ == "__main__":
    # Example usage
    trainer = ModelTrainer("./models")
    print("Model trainer initialized")
    print("Ready to train models from classification history")