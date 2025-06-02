import os
from utils.textPdf.pyMuPDF import extract_text_and_links_from_pdf
from utils.imagePdf.ocr_pytesseract import extract_text_ocr
from utils.word.word_python_docx import extract_text_from_docx

def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        # Try text-based extraction with links
        result = extract_text_and_links_from_pdf(filepath)

        if not result["text"].strip():
            return extract_text_ocr(filepath)

        return result

    elif ext == ".docx":
        # Return the full dictionary from the docx extractor
        return extract_text_from_docx(filepath)

    else:
        raise ValueError(f"Unsupported file type: {ext}")
