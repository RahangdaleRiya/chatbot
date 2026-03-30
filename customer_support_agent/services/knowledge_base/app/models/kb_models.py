from pydantic import BaseModel
from typing import Dict, Any, Optional

class DocumentCreate(BaseModel):
    title: str
    content: str
    metadata: Optional[Dict[str, Any]] = {}

class SearchQuery(BaseModel):
    query: str
    top_k: Optional[int] = 5