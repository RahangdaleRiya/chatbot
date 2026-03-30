import sys
import os
from fastapi import FastAPI
from .routes import feedback

# Add parent directory to path to handle relative imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../..')

app = FastAPI(title="Feedback Service")

app.include_router(feedback.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Feedback Service"}