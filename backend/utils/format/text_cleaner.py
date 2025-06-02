import re
from typing import Dict, List, Tuple

def clean_extracted_text(text: str) -> str:
    if not text:
        return ""

    cleaned = re.sub(r"\s+", " ", text)

    # Normalize emails by removing extra spaces
    cleaned = re.sub(
        r"\b([A-Za-z0-9._%+-]+)[\s]*@[\s]*([A-Za-z0-9.-]+)[\s]*\.[\s]*([A-Za-z]{2,})\b",
        r"\1@\2.\3",
        cleaned,
    )

    # Replace bullet points and quotes with normalized chars
    cleaned = (
        cleaned.replace("•", "• ")
        .replace("●", "• ")
        .replace("○", "• ")
        .replace("◆", "• ")
        .replace("◇", "• ")
        .replace("■", "• ")
        .replace("□", "• ")
        .replace("▪", "• ")
        .replace("▫", "• ")
    )

    cleaned = re.sub(r"[\u2018\u2019\u201A\u201B\u2032\u2035]", "'", cleaned)
    cleaned = re.sub(r"[\u201C\u201D\u201E\u201F\u2033\u2036]", '"', cleaned)

    replacements = {
        "EDUCATION": r"\b(EDUCATION|Education|education)\b\s*:?",
        "EXPERIENCE": r"\b(EXPERIENCE|Experience|experience|WORK EXPERIENCE|Work Experience)\b\s*:?",
        "SKILLS": r"\b(SKILLS|Skills|skills|TECHNICAL SKILLS|Technical Skills)\b\s*:?",
        "PROJECTS": r"\b(PROJECTS|Projects|projects)\b\s*:?",
        "LANGUAGES": r"\b(LANGUAGES|Languages|languages)\b\s*:?",
        "CERTIFICATIONS": r"\b(CERTIFICATIONS|Certifications|certifications|CERTIFICATES|Certificates)\b\s*:?",
    }

    for key, pattern in replacements.items():
        cleaned = re.sub(pattern, f"{key}:", cleaned)

    return cleaned.strip()

def clean_sensitive_data(text: str) -> Tuple[str, Dict[str, List[str]]]:
    email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z]{2,}\b", re.I)
    phone_regex = re.compile(
        r"\b(?:\+?\d{1,3})?[\s.-]?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,5}[\s.-]?\d{3,5}\b"
    )

    placeholders = {"emails": [], "phones": []}

    def email_replacer(match):
        placeholders["emails"].append(match.group(0))
        return f"[EMAIL_{len(placeholders['emails']) - 1}]"

    def phone_replacer(match):
        placeholders["phones"].append(match.group(0))
        return f"[PHONE_{len(placeholders['phones']) - 1}]"

    cleaned_text = email_regex.sub(email_replacer, text)
    cleaned_text = phone_regex.sub(phone_replacer, cleaned_text)

    return cleaned_text, placeholders

def enrich_text_with_links(text, links):
    enriched_text = text
    used_links = set()

    for link in links:
        link_text = link["text"]
        url = link["url"]
        
        # Escape regex special chars
        safe_text = re.escape(link_text)
        
        # Find and append URL once
        pattern = rf"({safe_text})(?!\s*\(https?://)"
        enriched_text, count = re.subn(pattern, rf"\1 ({url})", enriched_text, count=1)
        
        if count > 0:
            used_links.add(url)
    
    return enriched_text
