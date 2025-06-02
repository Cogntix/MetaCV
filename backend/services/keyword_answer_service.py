import re
from typing import List, Dict
from models.keyword_answer_model import KeywordAnswerResponse, AnswerItem


def preprocess_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(
        r"\b([A-Za-z0-9._%+-]+)[\s]*@[\s]*([A-Za-z0-9.-]+)[\s]*\.[\s]*([A-Za-z]{2,})\b",
        r"\1@\2.\3", text
    )
    text = re.sub(r"[•●○◆◇■□▪▫]", "•", text)
    return text.strip()


def get_keyword_based_answer(
    question: str,
    text: str,
    keywords: List[str],
    answer_type: str = "text"
) -> str:
    """
    Extracts answer from text based on keywords.
    Returns a boolean, text, or specific pattern depending on answer_type.
    """
    if not text or not keywords:
        return "N/A"

    text = preprocess_text(text).lower()
    question = question.lower()
    # Direct pattern extractions
    if "email" in question or answer_type == "email":
        match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", text)
        return match.group(0) if match else "N/A"

    if "phone" in question or answer_type == "phone":
        match = re.search(r"(\+\d{1,3}[-\s]?)?(\(?\d{3,4}\)?[-\s]?\d{3,4}[-\s]?\d{3,4}|\d{10})", text)
        return match.group(0) if match else "N/A"

    if "linkedin" in question or answer_type == "linkedin":
        match = re.search(r"(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9-]+", text)
        return match.group(0) if match else "N/A"

    if "behance" in question or answer_type == "behance":
        match = re.search(r"(https?://)?(www\.)?behance\.net/[a-zA-Z0-9_-]+", text)
        return match.group(0) if match else "N/A"

    if "portfolio" in question or answer_type == "portfolio":
        match = re.search(
            r"(https?://)?(www\.)?([a-zA-Z0-9_-]+\.)*(vercel\.app|netlify\.app|github\.io|portfolio|myportfolio|wixsite|webflow|carrd)\.[a-z]{2,}(/[a-zA-Z0-9_/?=-]*)?",
            text
        )
        return match.group(0) if match else "N/A"
  
    # Sentence-based keyword matching
    sentences = re.split(r"(?<=[.!?\n])\s+|•", text)
    matched_sentences = []

    for sentence in sentences:
        if any(keyword.lower() in sentence for keyword in keywords):
            matched_sentences.append(sentence.strip())

    if not matched_sentences:
        return "No" if answer_type == "boolean" else "N/A"

    return "Yes" if answer_type == "boolean" else matched_sentences[0]

def generate_keyword_answers(cleaned_text: str, questions: List[Dict]) -> KeywordAnswerResponse:
    answered: List[AnswerItem] = []

    for q in questions:
        answer = get_keyword_based_answer(
            question=q["question"],
            text=cleaned_text,
            keywords=q.get("keywords", []),
            answer_type=q.get("type", "text")
        )
        answered.append(AnswerItem(
            id=q["id"],
            question=q["question"],
            answer=answer
        ))

    return KeywordAnswerResponse(
        answered=answered
    )
