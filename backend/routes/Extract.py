from flask import Blueprint, request, jsonify
import os
import tempfile

from utils.extract_text import extract_text_from_file

extract_bp = Blueprint('extract', __name__)

@extract_bp.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

        # Extract text based on file type
        extracted_text = extract_text_from_file(temp_file_path)

        # Optionally remove temp file after processing
        os.remove(temp_file_path)

        return jsonify({"extracted_text": extracted_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
