# routes/extract_route.py
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List
from controllers.filter_questions_controller import filter_questions_controller
from controllers.extract_controller import extract_text_controller
from controllers.answerQuestions_controller import hybrid_answer_with_user_controller
from controllers.metaData_controller import generate_metadata_controller
from models.hybrid_answer_model import HybridAnswerRequest
from models.meta_ai_model import AnswerItem
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

class MetadataInput(BaseModel):
    extracted_text: str
    answers: List[AnswerItem]

@router.post("/generateMetadata")
async def generate_metadata_route(payload: MetadataInput):
    return {"success": True, "metadata": generate_metadata_controller(payload)}
