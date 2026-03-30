import sys
import os
from fastapi import FastAPI
from .routes import ticket

# Add parent directory to path to handle relative imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../..')

app = FastAPI(title="Ticket Retrieval Service")

app.include_router(ticket.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Ticket Retrieval Service"}