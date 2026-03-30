import sys
import os
# Ensure the parent directory is in sys.path for shared import
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from fastapi import APIRouter, HTTPException
import requests
import yaml

router = APIRouter()

def load_config():
    config_path = os.path.join(parent_dir, 'shared', 'config.yml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

config = load_config()

@router.get("/ticket/{ticket_id}")
def get_ticket(ticket_id: str):
    url = f"{config['jira']['url']}/rest/api/3/issue/{ticket_id}"
    auth = (config['jira']['username'], config['jira']['api_token'])
    response = requests.get(url, auth=auth)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Ticket not found")
    return response.json()