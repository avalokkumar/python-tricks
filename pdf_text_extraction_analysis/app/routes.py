from flask import Flask, request, jsonify
import os
from app.extract import detect_and_extract_text

app = Flask(__name__)

# API Route for extracting text from PDF
@app.route('/extract', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)

    # Extract text
    extracted_text = detect_and_extract_text(file_path)
    if extracted_text:
        return jsonify({'text': extracted_text}), 200
    else:
        return jsonify({'error': 'Failed to extract text'}), 500