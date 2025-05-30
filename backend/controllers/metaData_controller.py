from services.metaData_answer_service import generate_full_metadata
from models.meta_ai_model import MetadataInput
import logging
from fastapi import HTTPException

def generate_metadata_controller(payload: MetadataInput) -> dict:
    # print("DEbug",payload.answers)
    try:
        metadata = generate_full_metadata(payload.extracted_text, payload.answers)
        return metadata
    except ValueError as ve:
        logging.exception("Invalid data or JSON formatting error")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(ve)}")
    except Exception as e:
        logging.exception("Unexpected error during metadata generation")
        raise HTTPException(status_code=500, detail="Internal server error during metadata generation")
