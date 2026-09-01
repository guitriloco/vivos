"""
Document Classifier
Classification logic module
"""

import fitz  # PyMuPDF
import requests
import json
import os


class DocumentClassifier:
    def __init__(self):
        # Load configuration from the main config file
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')

        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            self.api_url = config.get('api_config', {}).get('api_url', 'http://localhost:20128/v1/chat/completions')
            self.model = config.get('api_config', {}).get('model', 'qw/qwen3-coder-plus')
            self.api_key = config.get('api_config', {}).get('api_key', '')
        except FileNotFoundError:
            # Default configuration if config file is not found
            self.api_url = 'http://localhost:20128/v1/chat/completions'
            self.model = 'qw/qwen3-coder-plus'
            self.api_key = 'sk-b00be5686461aefd-evx39g-5d4035ca'

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from a PDF file using PyMuPDF

        Args:
            pdf_path (str): Path to the PDF file

        Returns:
            str: Extracted text from the PDF
        """
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {str(e)}")
            return ""

    def classify_document(self, document_path):
        """
        Classify a document based on its content

        Args:
            document_path (str): Path to the document to classify

        Returns:
            str: Classification category
        """
        # First, extract text from the document if it's a PDF
        if document_path.lower().endswith('.pdf'):
            document_text = self.extract_text_from_pdf(document_path)
        else:
            # For non-PDF files, we might implement other extraction methods
            with open(document_path, 'r', encoding='utf-8', errors='ignore') as f:
                document_text = f.read()

        if not document_text.strip():
            return "Unclassifiable - No readable content"

        # Prepare the prompt for classification
        prompt = f"""
        Analyze the following document content and classify it into one of these categories:
        - Finance
        - Marketing
        - Technology
        - Legal
        - Medical
        - Education
        - Business
        - Personal
        - Other

        Just respond with the category name and nothing else.

        Document content (first 2000 characters):
        {document_text[:2000]}
        """

        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": self.model,
            "stream": False,
            "stream_options": None
        }

        try:
            # Send the request to the API
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                classification = result['choices'][0]['message']['content'].strip()

                # Clean up the response to extract just the category
                if '\n' in classification:
                    classification = classification.split('\n')[0].strip()

                # Remove any leading/trailing quotes
                classification = classification.strip('"\'')

                # Ensure the classification is one of our expected categories
                valid_categories = ['Finance', 'Marketing', 'Technology', 'Legal', 'Medical', 'Education', 'Business', 'Personal', 'Other']
                if classification not in valid_categories:
                    # If the model returned something unexpected, default to 'Other'
                    classification = 'Other'

                return classification
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return f"API Error: {response.status_code}"

        except requests.exceptions.ConnectionError:
            return "Connection Error - API not reachable"
        except Exception as e:
            print(f"Error during classification: {str(e)}")
            return f"Error: {str(e)}"


if __name__ == "__main__":
    # Example usage
    classifier = DocumentClassifier()

    # Example classification (would need an actual PDF file to test)
    # result = classifier.classify_document("path/to/document.pdf")
    # print(f"Classification result: {result}")
    pass