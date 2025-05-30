from pydantic import BaseModel
from typing import List, Optional

class AnswerItem(BaseModel):
    question: str
    auto_answer: Optional[str] = None
    correct_answer: Optional[str] = None
    metadata_field: Optional[str] = None  # Optional field for metadata mapping 

class AIAnswerResponse(BaseModel):
    answers: List[AnswerItem]

class MetadataInput(BaseModel):
    extracted_text: str
    answers: List[AnswerItem]
