import os
import fitz  # PyMuPDF
import mammoth
from pdf2image import convert_from_path
import pytesseract
from docx import Document
# Read paths from .env
tesseract_path = os.getenv("TESSERACT_PATH")
poppler_path = os.getenv("POPPLERPATH")

# Set tesseract executable path
pytesseract.pytesseract.tesseract_cmd = tesseract_path
def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        # Try text-based extraction first
        text = extract_text_from_pdf(filepath)
        if not text.strip():
            # fallback to OCR
            text = extract_text_ocr(filepath)
        return text

    elif ext in [".docx"]:
        return extract_text_from_docx(filepath)

    else:
        raise ValueError(f"Unsupported file type: {ext}")

def extract_text_from_pdf(pdf_path):
    # Use PyMuPDF for text-based extraction
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text() for page in doc])
    doc.close()
    return text

def extract_text_ocr(pdf_path):
    # OCR extraction using pytesseract + pdf2image
    pages = convert_from_path(pdf_path, dpi=300,poppler_path=poppler_path)
    text = ""
    for img in pages:
        text += pytesseract.image_to_string(img)
    return text

def extract_text_from_docx(docx_path):
    # Use mammoth for clean text extraction from docx
    with open(docx_path, "rb") as docx_file:
        result = mammoth.extract_raw_text(docx_file)
        return result.value
