# models/hybrid_answer_model.py
from pydantic import BaseModel

class HybridAnswerRequest(BaseModel):
    extractedText: str
    jobPosition: str
