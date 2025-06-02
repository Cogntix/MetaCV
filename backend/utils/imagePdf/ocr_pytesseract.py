import re
import os
from dotenv import load_dotenv
from pdf2image import convert_from_path
import pytesseract

load_dotenv()

tesseract_path = os.getenv("TESSERACT_PATH")
poppler_path = os.getenv("POPPLERPATH")

pytesseract.pytesseract.tesseract_cmd = tesseract_path

URL_REGEX = re.compile(
    r"(https?://[^\s]+)"
)

def extract_text_ocr(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
    full_text = ""
    for img in pages:
        full_text += pytesseract.image_to_string(img)
    
    # Find URLs inside the OCR extracted text
    urls = URL_REGEX.findall(full_text)
    links = [{"text": url, "url": url} for url in urls]

    return {
        "text": full_text,
        "links": links
    }
