import fitz  # PyMuPDF

def extract_text_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text() for page in doc])
    doc.close()
    return text

# Example usage
pdf_text = extract_text_pymupdf("../data/CV_TextBased.pdf")
print("PyMuPDF Output:\n", pdf_text)
