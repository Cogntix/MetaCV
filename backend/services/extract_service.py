import os
from utils.textPdf.pyMuPDF import extract_text_from_pdf
from utils.imagePdf.ocr_pytesseract import extract_text_ocr
from utils.word.word_mammoth import extract_text_from_docx

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

