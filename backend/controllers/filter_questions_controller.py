from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os

class FilterRequest(BaseModel):
    jobPosition: str

class FilterResponse(BaseModel):
    combinedQuestions: List[Dict[str, Any]]

def load_questions_data():
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data["commonQuestions"], data["roleQuestions"]

def get_filtered_questions(job_position: str) -> List[Dict[str, Any]]:
    common_questions, role_questions = load_questions_data()
    job_key = job_position.lower()

    specific_questions = role_questions.get(job_key, [])
    if not specific_questions:
        specific_questions = role_questions.get(job_position, [])  

    return common_questions + specific_questions

async def filter_questions_controller(payload: FilterRequest) -> FilterResponse:
    if not payload.jobPosition:
        raise ValueError("Missing jobPosition")

    combined_questions = get_filtered_questions(payload.jobPosition)

    return FilterResponse(
        combinedQuestions=combined_questions
    )
