from fastapi import UploadFile
from controllers.extract_controller import extract_text_controller
from controllers.answerQuestions_controller import hybrid_answer_with_user_controller
from models.hybrid_answer_model import HybridAnswerRequest
from utils.format.text_cleaner import clean_extracted_text
async def upload_cv_full_flow_controller(file: UploadFile, jobPosition: str):
    # 1. Extract text from CV
    extract_result = await extract_text_controller(file)
    extracted_text = extract_result["extracted_text"]
    # 2. Get answers using hybrid method
    answer_payload = HybridAnswerRequest(
        jobPosition=jobPosition,
        extractedText=extracted_text 
    )
    hybrid_result = await hybrid_answer_with_user_controller(answer_payload)
    questions_with_answers = hybrid_result["answered"]

    extractedText = clean_extracted_text(extracted_text)
    return {
        "success": True,
        "qa": questions_with_answers,
        "extracted_text":extractedText
    }
