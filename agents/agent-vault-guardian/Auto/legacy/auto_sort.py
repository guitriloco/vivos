import os
import json
import concurrent.futures
import fitz  # PyMuPDF
import requests
import time

def extract_pdf_text(pdf_path):
    """Extract text from PDF using PyMuPDF"""
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

def classify_document(text):
    """Classify document using localhost API"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer sk-b00be5686461aefd-evx39g-5d4035ca"
        }

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": f"Classify this document based on its content. Respond with a single category name that best describes the document: {text[:2000]}..."  # Limit text length
                }
            ],
            "model": "qw/qwen3-coder-plus",
            "stream": False,
            "stream_options": None
        }

        response = requests.post("http://localhost:20128/v1/chat/completions",
                                headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            classification = result['choices'][0]['message']['content'].strip()
            return classification
        else:
            print(f"API error: {response.status_code} - {response.text}")
            return "uncategorized"
    except Exception as e:
        print(f"Error classifying document: {str(e)}")
        return "uncategorized"

def process_pdf(pdf_path):
    """Process a single PDF file: extract text and classify"""
    print(f"Processing: {pdf_path}")

    # Extract text from PDF
    text = extract_pdf_text(pdf_path)

    if not text.strip():
        print(f"No text extracted from {pdf_path}, skipping...")
        return

    # Classify the document
    classification = classify_document(text)

    # Create directory based on classification if it doesn't exist
    base_dir = os.path.dirname(pdf_path)
    class_dir = os.path.join(base_dir, classification.replace("/", "_").replace("\\", "_"))

    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    # Move the PDF to the classified directory
    filename = os.path.basename(pdf_path)
    new_path = os.path.join(class_dir, filename)

    # Handle potential filename conflicts
    counter = 1
    original_new_path = new_path
    while os.path.exists(new_path):
        name, ext = os.path.splitext(original_new_path)
        new_path = f"{name}_{counter}{ext}"
        counter += 1

    os.rename(pdf_path, new_path)
    print(f"Classified '{filename}' as '{classification}' and moved to '{class_dir}'")

def main():
    directory = r"C:\Users\guilh\Desktop\projets"

    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist!")
        return

    # Find all PDF files in the directory
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                print(f"Found PDF: {pdf_path}")
                pdf_files.append(pdf_path)

    print(f"Found {len(pdf_files)} PDF files to process.")

    if not pdf_files:
        print("No PDF files found to process.")
        # Let's check if there are any PDFs in subdirectories
        print("Scanning for PDFs in subdirectories...")
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    print(f"  - {os.path.join(root, file)}")
        return

    # Process PDFs concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_pdf, pdf_path) for pdf_path in pdf_files]

        # Wait for all tasks to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # This will raise any exceptions that occurred
            except Exception as e:
                print(f"A processing error occurred: {str(e)}")

if __name__ == "__main__":
    start_time = time.time()
    print("Starting PDF classification process...")
    main()
    end_time = time.time()
    print(f"Process completed in {end_time - start_time:.2f} seconds.")