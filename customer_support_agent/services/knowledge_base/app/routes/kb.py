import sys
import os
# Ensure the parent directory is in sys.path for shared import
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from shared.database import get_db
from shared.models import Document, Embedding
from ..models.kb_models import DocumentCreate, SearchQuery
from ..utils.embeddings import generate_embedding, search_similar, split_text
from ..utils.pdf_loader import load_pdf_from_bytes
import json
from fastapi import APIRouter

router = APIRouter()

@router.post("/documents/")
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    db_doc = Document(title=doc.title, content=doc.content, doc_metadata=json.dumps(doc.metadata))
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)


    # Use langchain_text_splitters for long documents
    from ..utils.embeddings import split_text, generate_embedding

    chunks = split_text(doc.content)
    for chunk in chunks:
        chunk_embedding = generate_embedding(chunk)
        db_embedding = Embedding(document_id=db_doc.id, vector=chunk_embedding)
        db.add(db_embedding)

    db.commit()
    return {"id": db_doc.id}

@router.get("/documents/{doc_id}")
def get_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"id": doc.id, "title": doc.title, "content": doc.content, "metadata": json.loads(doc.doc_metadata)}

@router.post("/search/")
def search_documents(query: SearchQuery, db: Session = Depends(get_db)):
    query_embedding = generate_embedding(query.query)
    similar_docs = search_similar(query_embedding, db, top_k=query.top_k)
    results = []
    for doc_id, score in similar_docs:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        results.append({"id": doc.id, "title": doc.title, "content": doc.content, "score": score})
    return {"results": results}

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload and process a PDF file"""
    try:
        file_content = await file.read()
        full_text, _ = load_pdf_from_bytes(file_content)
        
        # Create document
        db_doc = Document(
            title=file.filename,
            content=full_text,
            doc_metadata=json.dumps({"source": "pdf", "filename": file.filename})
        )
        db.add(db_doc)
        db.commit()
        db.refresh(db_doc)
        
        # Split and embed
        chunks = split_text(full_text)
        for chunk in chunks:
            chunk_embedding = generate_embedding(chunk)
            db_embedding = Embedding(document_id=db_doc.id, vector=chunk_embedding)
            db.add(db_embedding)
        
        db.commit()
        return {"id": db_doc.id, "filename": file.filename, "chunks": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing PDF: {str(e)}")