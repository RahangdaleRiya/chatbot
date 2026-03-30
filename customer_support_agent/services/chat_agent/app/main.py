import sys
import os
from fastapi import FastAPI
from .routes import chat

# Add parent directory to path to handle relative imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../..')

app = FastAPI(title="Chat Agent Service")

app.include_router(chat.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Chat Agent Service"}