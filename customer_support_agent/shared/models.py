from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from pgvector.sqlalchemy import Vector
from .database import Base
import datetime

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    doc_metadata = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, index=True)
    vector = Column(Vector(1024))  # pgvector with 1024 dimensions (mxbai-embed-large)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_query = Column(Text)
    agent_response = Column(Text)
    rating = Column(Float)  # 1-5
    comments = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)