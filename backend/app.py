# app.py
from fastapi import FastAPI
from routes.extract_route import router as extract  # Note: renamed to router (FastAPI convention)

app = FastAPI()

# Register Routers
app.include_router(extract)

# This is only for local development; in production, use: `uvicorn app:app --reload`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)