from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    session_id: str
    user_query: str
    agent_response: str
    rating: float
    comments: str = ""