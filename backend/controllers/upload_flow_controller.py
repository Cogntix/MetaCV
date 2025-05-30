from fastapi import UploadFile
from controllers.extract_controller import extract_text_controller
from controllers.filter_questions_controller import filter_questions_controller
from controllers.answerQuestions_controller import hybrid_answer_with_user_controller
from models.hybrid_answer_model import HybridAnswerRequest
from controllers.filter_questions_controller import FilterRequest

async def upload_cv_full_flow_controller(file: UploadFile, jobPosition: str):
    # print("Started")
    # 1. Extract text from CV
    extract_result = await extract_text_controller(file)
    extracted_text = extract_result["extracted_text"]

    # print("Debug 1")
    # 2. Filter questions for the job
    filtered = await filter_questions_controller(FilterRequest(jobPosition=jobPosition))
    questions = filtered.combinedQuestions

    # print("Debug 2")
    # 3. Get answers using hybrid method
    answer_payload = HybridAnswerRequest(
        jobPosition=jobPosition,
        extractedText=extracted_text  # Correct field name
    )

    hybrid_result = await hybrid_answer_with_user_controller(answer_payload)
    questions_with_answers = hybrid_result["answered"]

    # print("Debug 3")
    # End here - no metadata generation

    return {
        "success": True,
        "qa": questions_with_answers
    }
