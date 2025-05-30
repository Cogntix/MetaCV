import json
from pathlib import Path
from typing import Dict, Optional
from fastapi import HTTPException
from models.meta_ai_model import MetadataInput
from controllers.metaData_controller import generate_metadata_controller

QUESTIONS_JSON_PATH = Path("data/questions.json")

def load_questions_data(job_position: str) -> Dict:
    """Load the complete questions data for mapping"""
    with open(QUESTIONS_JSON_PATH, "r") as f:
        data = json.load(f)
    
    return data

def find_question_id_by_text(question_text: str, questions_data: Dict, job_position: str) -> Optional[str]:
    """Find question ID by matching question text"""
    question_text = question_text.strip().lower()
    
    # Check common questions
    for q in questions_data.get("commonQuestions", []):
        if q.get("question", "").strip().lower() == question_text:
            return q.get("id")
    
    # Check role-specific questions
    role_questions = questions_data.get("roleQuestions", {}).get(job_position, [])
    for q in role_questions:
        if q.get("question", "").strip().lower() == question_text:
            return q.get("id")
    
    return None

def get_field_mapping(question_id: str, questions_data: Dict, job_position: str) -> str:
    """Get field mapping for a question ID"""
    # Check common questions
    for q in questions_data.get("commonQuestions", []):
        if q.get("id") == question_id:
            return q.get("field", "").strip()
    
    # Check role-specific questions
    role_questions = questions_data.get("roleQuestions", {}).get(job_position, [])
    for q in role_questions:
        if q.get("id") == question_id:
            return q.get("field", "").strip()
    
    return ""

async def confirm_answers_controller(payload: MetadataInput):
    answers = payload.answers
    job_position = payload.jobPosition

    # Load questions data
    questions_data = load_questions_data(job_position)
    
    for answer in answers:
        if answer.metadata_field is None:
            # Get question text from answer
            question_text = getattr(answer, 'question', None)
            
            if question_text:
                # Find question ID by matching text
                question_id = find_question_id_by_text(question_text, questions_data, job_position)
                
                if question_id:
                    # Get field mapping
                    mapped_field = get_field_mapping(question_id, questions_data, job_position)
                    
                    if mapped_field:  # only assign if field is non-empty
                        answer.metadata_field = mapped_field

    try:
        metadata = generate_metadata_controller(payload)
        return {"success": True, "metadata": metadata}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))