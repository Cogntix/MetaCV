# MetaCV - Backend

MetaCV is a backend service for extracting structured information from resumes (CVs) in PDF and DOCX formats. It uses OCR (Tesseract) and NLP techniques to process both text-based and image-based CVs.

## ✨ Features

- Extracts key data from CVs (e.g., name, email, phone, skills)
- Supports scanned/image-based PDFs using Tesseract OCR
- Works with both `.pdf` and `.docx` formats
- Simple API endpoint for integration or testing via Postman

## 🧰 Tech Stack

- **Python (FastAPI)**
- **PyMuPDF** (for PDF text-based parsing)
- **Tesseract OCR**
- **Poppler** (for `pdf2image`)
- **Mammoth** (for `.docx` text extraction)
  note
- **Python-docx** ( can use it for `.docx` text extraction)

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Cogntix/MetaCV.git
cd MetaCV
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. API Endpoint

🔹 POST /extract
URL: http://localhost:5000/extract
Method: POST
Body Type: form-data
Field: file (Upload your .pdf or .docx file)

    🔹 POST /filterQuestions
    URL: http://localhost:5000/extract
    Method: POST
    Body Type: JSON
    Body Example:
    {
    "jobPosition": "Software Engineer"
    }

    🔹 POST /hybridAnswer
    URL: http://localhost:5000/extract
    Method: POST
    Body Type: JSON
    Body Example:{
    "jobPosition": "Software Engineer",
    "extractedText": "extracted text from CV"
    }

### 5. Run the Server

```bash
python backend/app.py
```
