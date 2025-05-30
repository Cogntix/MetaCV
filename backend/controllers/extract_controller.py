# controllers/extract_controller.py
from fastapi import UploadFile, HTTPException
from fastapi.responses import JSONResponse

from services.extract_service import extract_text_from_file
from middleware.file_handler import save_upload_to_temp_file, cleanup_temp_file

async def extract_text_controller(file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    try:
        temp_file_path = await save_upload_to_temp_file(file)
        extracted_text = extract_text_from_file(temp_file_path)
        cleanup_temp_file(temp_file_path)
        return {"extracted_text": extracted_text}


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
