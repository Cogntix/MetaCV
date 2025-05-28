import mammoth

def extract_text_from_docx(docx_path):
    with open(docx_path, "rb") as docx_file:
        result = mammoth.extract_raw_text(docx_file)
        text = result.value  # The extracted text
        messages = result.messages  # Any warnings during extraction
    return text

