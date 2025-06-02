#python-docx
from docx import Document

def extract_text_from_docx(docx_path):
    document = Document(docx_path)
    full_text = []
    links_info = []

    rels = document.part.rels
    NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

    for para in document.paragraphs:
        full_text.append(para.text)

        for child in para._element.findall(f".//{{{NS_W}}}hyperlink"):
            rel_id = child.get(f"{{{NS_R}}}id")
            if rel_id and rel_id in rels:
                url = rels[rel_id].target_ref

                link_text = ""
                for r in child.findall(f".//{{{NS_W}}}t"):
                    link_text += r.text or ""

                if link_text.strip():
                    links_info.append({
                        "text": link_text.strip(),
                        "url": url
                    })

    return {
        "text": "\n".join(full_text),
        "links": links_info
    }
