from pydantic import BaseModel
from typing import List, Dict

class AIAnswerRequest(BaseModel):
    extractedText: str
    jobPosition: str

class AnswerItem(BaseModel):
    id: str
    question: str
    answer: str

class AIAnswerResponse(BaseModel):
    jobPosition: str
    answered: List[AnswerItem]
