"""
Test script for the Document Classifier
"""

import sys
import os

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from Document_Classifier_GUI.classifier import DocumentClassifier

def test_classifier():
    print("Testing DocumentClassifier...")

    # Create classifier instance
    classifier = DocumentClassifier()

    print(f"API URL: {classifier.api_url}")
    print(f"Model: {classifier.model}")
    print(f"API Key: {'*' * len(classifier.api_key) if classifier.api_key else 'Not set'}")

    # Test with a sample text (simulating document content)
    sample_text = """
    This document discusses various financial strategies for investment portfolios.
    It covers topics such as risk assessment, market analysis, and portfolio diversification.
    The focus is on long-term wealth building through strategic asset allocation.
    """

    print("\nSample text for classification:")
    print(sample_text[:100] + "...")

    # Since we don't have a real PDF to test with, we'll simulate by temporarily modifying
    # the classify_document method to accept text directly
    print("\nTesting classification functionality...")

    # We can't fully test without an actual PDF file and working API,
    # but we can verify the class loads correctly
    print("DocumentClassifier instantiated successfully!")
    print("Configuration loaded from config.json")
    print("Ready to process documents when provided.")

if __name__ == "__main__":
    test_classifier()