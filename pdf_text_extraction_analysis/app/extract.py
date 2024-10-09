import PyPDF2
import pytesseract
from pdf2image import convert_from_path
import os

# Extract text from native PDF
def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting from native PDF: {e}")
        return None

# Extract text from scanned PDF using OCR
def extract_text_from_scanned_pdf(file_path):
    try:
        images = convert_from_path(file_path)
        text = ''
        for image in images:
            text += pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error extracting from scanned PDF: {e}")
        return None

# Detect whether the PDF is scanned or native
def detect_and_extract_text(file_path):
    extracted_text = extract_text_from_pdf(file_path)
    if not extracted_text.strip():  # Empty or null text indicates a scanned PDF
        print("Detected scanned PDF. Running OCR...")
        return extract_text_from_scanned_pdf(file_path)
    return extracted_text