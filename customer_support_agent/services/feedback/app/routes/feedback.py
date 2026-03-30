import sys
import os
# Ensure the parent directory is in sys.path for shared import
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from shared.database import get_db
from shared.models import Feedback
from ..models.feedback_models import FeedbackCreate

router = APIRouter()

@router.post("/feedback/")
def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return {"id": db_feedback.id}

@router.get("/feedback/{session_id}")
def get_feedback(session_id: str, db: Session = Depends(get_db)):
    feedbacks = db.query(Feedback).filter(Feedback.session_id == session_id).all()
    return [{"id": f.id, "rating": f.rating, "comments": f.comments} for f in feedbacks]