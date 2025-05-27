# MetaCV - Backend

MetaCV is a backend service for extracting structured information from resumes (CVs) in PDF and DOCX formats. It uses OCR and NLP to process both text-based and image-based CVs.

## Features

- Extract key data from CVs: name, email, phone, skills, etc.
- Supports scanned/image-based CVs using Tesseract OCR
- API endpoint for integration or testing via Postman

## Tech Stack

- Python (Flask)
- Tesseract OCR
- Poppler
- mammoth

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/metacv-backend.git
   cd metacv-backend
   ```
2. Install dependencies

pip install -r backend/requirements.txt 

3. Create a .env file in the project root:

    POPPLER_PATH=/path/to/poppler/bin
    TESSERACT_PATH=/path/to/tesseract.exe


functionality 
1. POST /extract
URL: http://localhost:5000/extract
Method: POST
Body Type: form-data
file: Upload CV file (.pdf or .docx)
