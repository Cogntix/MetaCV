from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.extract_route import router as extract

app = FastAPI()

# ✅ Allow frontend (e.g., React) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origin like ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(extract)

# Local dev server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
