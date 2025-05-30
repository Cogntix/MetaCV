from pydantic import BaseModel
from typing import List, Optional

class AnswerItem(BaseModel):
    question: str
    auto_answer: Optional[str] = None #optional
    correct_answer: Optional[str] = None

class AIAnswerResponse(BaseModel):
    answers: List[AnswerItem]

class MetadataInput(BaseModel):
    extracted_text: str
    answers: List[AnswerItem]
