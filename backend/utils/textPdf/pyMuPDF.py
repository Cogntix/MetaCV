# PyMuPDF
import fitz  

def extract_text_and_links_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = []
    links_info = []

    for page_num, page in enumerate(doc):
        # Extract full text
        full_text.append(page.get_text())

        # Extract links
        links = page.get_links()
        for link in links:
            uri = link.get("uri")
            if uri:
                rect = fitz.Rect(link["from"])
                words = page.get_text("words")  
                linked_text = " ".join(word[4] for word in words if fitz.Rect(word[:4]).intersects(rect))

                links_info.append({
                    "page": page_num + 1,
                    "text": linked_text,
                    "url": uri
                })

    doc.close()
    return {
        "text": "\n".join(full_text),
        "links": links_info
    }
