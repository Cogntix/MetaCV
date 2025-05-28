from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile

from backend.routes.extractCVData import extract_text_from_file

router = APIRouter()

@router.post("/extract")
async def extract(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    try:
        # Create a temporary file with the same extension
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        # Extract text
        extracted_text = extract_text_from_file(temp_file_path)

        # Clean up
        os.remove(temp_file_path)

        return JSONResponse(content={"extracted_text": extracted_text})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
