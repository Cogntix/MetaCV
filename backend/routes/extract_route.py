# routes/extract_route.py
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from controllers.filter_questions_controller import filter_questions_controller
from controllers.extract_controller import extract_text_controller
from controllers.answerQuestions_controller import hybrid_answer_with_user_controller
from models.hybrid_answer_model import HybridAnswerRequest

router = APIRouter()

@router.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    return await extract_text_controller(file)

class FilterRequest(BaseModel):
    jobPosition: str

@router.post("/filterQuestions")
async def filter_questions(payload: FilterRequest):
    return await filter_questions_controller(payload)

@router.post("/hybridAnswer")
async def hybrid_answer_route(payload: HybridAnswerRequest):
    return await hybrid_answer_with_user_controller(payload)
