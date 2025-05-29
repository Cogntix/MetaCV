from fastapi import HTTPException
from models.hybrid_answer_model import HybridAnswerRequest
from services.hybrid_answer_service import generate_hybrid_answers

async def hybrid_answer_with_user_controller(payload: HybridAnswerRequest):
    if not payload.extractedText or not payload.jobPosition:
        raise HTTPException(status_code=400, detail="Missing extractedText or jobPosition")

    try:
        return await generate_hybrid_answers(payload.extractedText, payload.jobPosition)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hybrid answering failed: {str(e)}")