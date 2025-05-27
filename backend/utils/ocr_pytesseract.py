import os
from dotenv import load_dotenv
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import time

# Load variables from .env
load_dotenv()

# Read paths from .env
tesseract_path = os.getenv("TESSERACT_PATH")
poppler_path = os.getenv("POPPLERPATH")

# Set tesseract executable path
pytesseract.pytesseract.tesseract_cmd = tesseract_path

def extract_text_ocr(pdf_path):
    start_time = time.time()
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
    text = ""
    for img in pages:
        text += pytesseract.image_to_string(img)
    end_time = time.time()
    # print (f"Total Time Taken {(end_time-start_time):.3f} seconds")
    return text

# Example usage
ocr_text = extract_text_ocr("../data/CV_Imagebased.pdf")
print("OCR Output:\n", ocr_text)

