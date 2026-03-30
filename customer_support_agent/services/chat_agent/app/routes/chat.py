import sys
import os
# Ensure the parent directory is in sys.path for shared import
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from shared.database import get_db
from shared.models import Feedback
from ..agents.support_agent import SupportAgent

router = APIRouter()

def load_config():
    config_path = os.path.join(parent_dir, 'config.yml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

config = load_config()

agent = SupportAgent(config)

@router.post("/chat/")
def chat(message: str, ticket_id: str = None, session_id: str = None, db: Session = Depends(get_db)):
    # Retrieve ticket if provided
    ticket_info = None
    if ticket_id:
        ticket_url = f"http://{config['services']['ticket_retrieval']['host']}:{config['services']['ticket_retrieval']['port']}/api/v1/ticket/{ticket_id}"
        try:
            response = requests.get(ticket_url)
            if response.status_code == 200:
                ticket_info = response.json()
        except:
            pass

    # Search knowledge base
    kb_url = f"http://{config['services']['knowledge_base']['host']}:{config['services']['knowledge_base']['port']}/api/v1/search/"
    kb_response = requests.post(kb_url, json={"query": message, "top_k": 3})
    kb_results = kb_response.json().get("results", []) if kb_response.status_code == 200 else []

    # Generate response
    response = agent.generate_response(message, ticket_info, kb_results)

    # Save feedback placeholder
    if session_id:
        feedback = Feedback(session_id=session_id, user_query=message, agent_response=response)
        db.add(feedback)
        db.commit()

    return {"response": response}