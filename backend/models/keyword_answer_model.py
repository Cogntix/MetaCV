from pydantic import BaseModel
from typing import List

class AnswerItem(BaseModel):
    id: str
    question: str
    answer: str

class KeywordAnswerResponse(BaseModel):
    answered: List[AnswerItem]
