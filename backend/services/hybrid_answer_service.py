# services/hybrid_answer_service.py
from typing import List, Dict, Any
from controllers.filter_questions_controller import get_filtered_questions
from utils.format.text_cleaner import clean_extracted_text,clean_sensitive_data
from services.keyword_answer_service import generate_keyword_answers
from services.ai_answer_service import generate_ai_answers

def restore_placeholders(answer: str, placeholders: Dict[str, List[str]]) -> str:
    for i, email in enumerate(placeholders.get("emails", [])):
        answer = answer.replace(f"[EMAIL_{i}]", email)
    for i, phone in enumerate(placeholders.get("phones", [])):
        answer = answer.replace(f"[PHONE_{i}]", phone)
    return answer

async def generate_hybrid_answers(extractedText: str, jobPosition: str) -> Dict[str, Any]:
    combinedQuestions = get_filtered_questions(jobPosition)
    baseCleanedText = clean_extracted_text(extractedText)

    keywordQuestions = [q for q in combinedQuestions if q["answerSource"] == "keywords"]
    aiQuestions = [q for q in combinedQuestions if q["answerSource"] == "ai"]
    userQuestions = [q for q in combinedQuestions if q["answerSource"] == "user"]
    keywordResponse = generate_keyword_answers(baseCleanedText,keywordQuestions)
    keywordResults = [
        {
            "id": a.id,
            "question": a.question,
            "answer": a.answer or "N/A",
            "source": "keywords",
        }
        for a in keywordResponse.answered
        if any(q["id"] == a.id for q in keywordQuestions)  # filter only keyword ones
    ]
    baseCleanedText = clean_sensitive_data(baseCleanedText)

    # AI answers
    aiAnswers = []
    if aiQuestions:
        aiResponse = generate_ai_answers(
            baseCleanedText,
            jobPosition,
            [{"id": q["id"], "question": q["question"]} for q in aiQuestions]
        )

        for a in aiResponse.answered:
            aiAnswers.append({
                "id": a.id,
                "question": a.question,
                "answer": a.answer,
                "source": "ai",
            })


    # User-only questions
    userResults = [
        {"id": q["id"], "question": q["question"], "answer": "N/A", "source": "user"}
        for q in userQuestions
    ]

    finalAnswers = keywordResults + aiAnswers + userResults

    allAnswers = []
    for q in combinedQuestions:
        match = next((a for a in finalAnswers if a["id"] == q["id"]), None)
        if match:
            allAnswers.append(match)
        else:
            allAnswers.append({
                "id": q["id"],
                "question": q["question"],
                "answer": "N/A",
                "source": q["answerSource"],
            })

    return {
        "jobPosition": jobPosition,
        "answered": allAnswers,
        "stats": {
            "total": len(combinedQuestions),
            "keywords": len(keywordResults),
            "ai": len(aiAnswers),
            "user": len(userResults),
        },
    }
