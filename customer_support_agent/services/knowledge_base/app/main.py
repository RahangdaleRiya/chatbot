import sys
import os
from fastapi import FastAPI
from .routes import kb

# Add parent directory to path to handle relative imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../..')

app = FastAPI(title="Knowledge Base Service")

app.include_router(kb.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Knowledge Base Service"}