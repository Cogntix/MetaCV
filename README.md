# MetaCV - Backend

MetaCV is a backend service for extracting structured information from resumes (CVs) in PDF and DOCX formats. It uses OCR (Tesseract) and NLP techniques to process both text-based and image-based CVs.

## ✨ Features

- Extracts key data from CVs (e.g., name, email, phone, skills)
- Supports scanned/image-based PDFs using Tesseract OCR
- Works with both `.pdf` and `.docx` formats
- Simple API endpoint for integration or testing via Postman

## 🧰 Tech Stack
- Python (FastAPI) – High-performance web framework for building API services.
- PyMuPDF – Used for extracting text and metadata from text-based PDF files.
- Tesseract OCR – Optical Character Recognition engine for parsing scanned (image-based) PDF content.
- Poppler – Backend utility used by pdf2image to convert PDF pages to images for OCR processing.
- pdf2image – Converts PDF pages into image format for use with Tesseract OCR.
- python-docx –  library to extract and manipulate Word documents (.docx format).
- python-multipart – Enables handling of file uploads via multipart forms.
- LangChain – Framework for building AI-driven applications using language models, including chain-based metadata reasoning and extraction.
- GROQ – Integration with GroqCloud for high-speed, low-latency language model inference, especially when used with LangChain.
- PyTesseract – Python wrapper for Tesseract OCR engine.
- dotenv – For managing environment variables securely.
- Uvicorn – ASGI server used to run FastAPI in production or development.

## ⚙️ Setup Instructions

### 1. Clone the Repository
 
```bash
git clone https://github.com/Cogntix/MetaCV.git
cd MetaCV
```

### 2. Configure Environment Variables
  > Update the variables with correct values (like API keys, etc.)


### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```
### 4. Run the Server

```bash
python backend/app.py
```

### 5. API Endpoint

    🔹 POST /extract
    URL: http://localhost:5000/extract
    Method: POST
    Body Type: form-data
    Field: file (Upload your .pdf or .docx file)

    🔹 POST /filterQuestions
    URL: http://localhost:5000/filterQuestions
    Method: POST
    Body Type: JSON
    Body Example:
    {
    "jobPosition": "software-engineer"
    }

    🔹 POST /hybridAnswer
    URL: localhost:5000/hybridAnswer
    Method: POST
    Body Type: JSON
    Body Example:{
    "jobPosition": "software-engineer",
    "extractedText": "extracted text from CV"
    }

    🔹 POST /generateMetadata
    URL: http://localhost:5000/generateMetadata
    Method: POST
    Body Type: JSON
    Body Example:{
    "jobPosition": "Software Engineer",
    "extractedText": "extracted text from CV",
    "answers": [
    {
    "question": "What is your full name?",
    "correct_answer": "Shathurya Paramanathan",
    "metadata_field": "candidate_information.full_name "
    },]
    }

    🔹 POST /upload
    URL: localhost:5000/upload
    Method: POST
      Body Type: form-data
    Field: file (Upload your .pdf or .docx file), "jobPosition" (text)

    🔹 POST /confirm
    URL: http://localhost:5000/confirm
    Method: POST
    Body Type: JSON
    Body Example:{
    "jobPosition": "Software Engineer",
    "extractedText": "extracted text from CV",
    "answers": [
    {
    "question": "What is your full name?",
    "correct_answer": "Shathurya Paramanathan"
    },]
    }


