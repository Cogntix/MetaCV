# pdfPlumper.py
import pdfplumber

def extract_text_pdfplumber(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

if __name__ == "__main__":
    path = "../data/CV_TextBased.pdf"  # Change to your PDF path
    extracted_text = extract_text_pdfplumber(path)
    print("=== pdfplumber Output ===\n")
    print(extracted_text)  
