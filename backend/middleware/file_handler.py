# backend/middleware/file_handler.py
import os
import tempfile

async def save_upload_to_temp_file(upload_file):
    suffix = os.path.splitext(upload_file.filename)[1]
    file_data = await upload_file.read() 

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(file_data)
        return temp_file.name

def cleanup_temp_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
