from fastapi import UploadFile
from controllers.extract_controller import extract_text_controller
from controllers.answerQuestions_controller import hybrid_answer_with_user_controller
from models.hybrid_answer_model import HybridAnswerRequest
from utils.format.text_cleaner import clean_extracted_text,enrich_text_with_links

async def upload_cv_full_flow_controller(file: UploadFile, jobPosition: str):
    # 1. Extract text (and possibly links) from CV
    extract_result = await extract_text_controller(file)
    raw_text = extract_result.get("extracted_text", {}).get("text", "")
    links = extract_result.get("extracted_text", {}).get("links", "")

    # 2. Append the links with text and Clean extracted text before question answering   
    appendText = enrich_text_with_links(raw_text,links)
    cleaned_text = clean_extracted_text(appendText)
     
    # 3. Prepare payload for hybrid answer
    answer_payload = HybridAnswerRequest(
        jobPosition=jobPosition,
        extractedText=cleaned_text
    )
    
    # 4. Get answers using hybrid method
    hybrid_result = await hybrid_answer_with_user_controller(answer_payload)
    questions_with_answers = hybrid_result.get("answered", [])
    
    return {
        "success": True,
        "qa": questions_with_answers,
        "extracted_text": cleaned_text
    }
