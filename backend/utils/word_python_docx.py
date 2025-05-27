# word_python_docx.py
from docx import Document

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])
    return text

# Example usage
docx_text = extract_text_from_docx("../data/CV_Textbased_Word.docx")
print("Extracted Text:\n", docx_text)
