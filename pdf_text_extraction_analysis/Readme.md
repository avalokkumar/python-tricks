# PDF Text Extraction Backend System


To run the application
```bash
curl -X POST http://localhost:5000/extract -F 'file=@/path/to/sample.pdf'
python run.py
```

## Overview
This backend system extracts text from PDF documents using a combination of Python libraries. It handles PDF parsing, text processing, and allows for integration with other systems through an API. The architecture ensures efficient text extraction, even from scanned PDFs using OCR techniques.

---

## Features
- Extract text from PDFs (both native and scanned).
- Handle multi-page PDFs.
- Supports different PDF formats (text-based, images).
- Provide results in structured format (JSON).
- Offer an API for remote text extraction.
- Support language detection and basic text preprocessing.

---

## Prerequisites
- Python 3.x
- Tesseract-OCR (for scanned PDFs)
- Poppler (for handling PDF rendering)
- Python Libraries:
  - `PyPDF2` or `pdfminer.six` for native PDFs
  - `pytesseract` for OCR
  - `pdf2image` for converting PDF to image (optional for OCR)
  - `Flask` or `FastAPI` for building the API

---

## Architecture
1. **PDF Ingestion Module**:
   - Use `PyPDF2` or `pdfminer.six` for extracting text from native PDF files.
   - For scanned PDFs, use `pdf2image` to convert each page into an image, then use `pytesseract` for OCR-based text extraction.

2. **Text Processing Module**:
   - Clean the extracted text (e.g., remove extra whitespace, newlines).
   - Implement language detection for multilingual PDFs.

3. **API Layer**:
   - Use a RESTful API (Flask or FastAPI) to allow external services to upload PDFs and retrieve extracted text in a structured format like JSON.

4. **Storage**:
   - If needed, store extracted data in a database (e.g., SQLite, PostgreSQL).

---

## Installation
### 1. Install Python Dependencies
```bash
pip install PyPDF2 pdfminer.six pytesseract pdf2image Flask
```

### 2. Install System Dependencies
- **Tesseract-OCR**:
  ```bash
  brew install tesseract
  ```
- **Poppler** (for pdf2image):
  ```bash
  brew install poppler
  ```

---

## Usage

### 1. Native PDF Text Extraction
```python
import PyPDF2

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text
```

### 2. OCR-based Text Extraction (for Scanned PDFs)
```python
import pytesseract
from pdf2image import convert_from_path

def extract_text_from_scanned_pdf(file_path):
    images = convert_from_path(file_path)
    text = ''
    for image in images:
        text += pytesseract.image_to_string(image)
    return text
```

### 3. API for PDF Text Extraction
```python
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_text():
    file = request.files['file']
    text = extract_text_from_pdf(file)  # Use OCR function for scanned PDFs
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)
```

---

## API Endpoints

### POST `/extract`
Upload a PDF file to extract the text:
```bash
curl -X POST http://localhost:5000/extract -F 'file=@sample.pdf'
```

Response:
```json
{
  "text": "Extracted text from the PDF..."
}
```

---

## Performance Considerations
- **Parallel Processing**: Use threading or multiprocessing for handling multiple PDFs concurrently.
- **Caching**: Store extracted text for previously processed PDFs to avoid redundant work.
- **Error Handling**: Ensure the system can handle malformed or corrupted PDFs gracefully.

---

## Future Enhancements
- Add support for extracting images, tables, and metadata from PDFs.
- Introduce advanced text processing like summarization or keyword extraction.
- Enable processing large batches of PDFs using a queuing system (e.g., RabbitMQ).
