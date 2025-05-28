import os
from dotenv import load_dotenv
from pdf2image import convert_from_path
import pytesseract
from PIL import Image


# Load variables from .env
load_dotenv()

# Read paths from .env
tesseract_path = os.getenv("TESSERACT_PATH")
poppler_path = os.getenv("POPPLERPATH")

# Set tesseract executable path
pytesseract.pytesseract.tesseract_cmd = tesseract_path

def extract_text_ocr(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
    text = ""
    for img in pages:
        text += pytesseract.image_to_string(img)
    return text

