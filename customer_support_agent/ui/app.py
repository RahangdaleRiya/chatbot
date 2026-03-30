import streamlit as st
import requests
import os
import sys
import yaml

# Handle config loading
config_path = os.path.join(os.path.dirname(__file__), 'shared', 'config.yml')
if not os.path.exists(config_path):
    config_path = os.path.join(os.path.dirname(__file__), '..', 'shared', 'config.yml')

def load_config():
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

config = load_config()

st.title("Customer Support Chat")

session_id = st.text_input("Session ID")
ticket_id = st.text_input("Reference Ticket ID (optional)")
message = st.text_area("Your message")

if st.button("Send"):
    if message:
        chat_url = f"http://{config['services']['chat_agent']['host']}:{config['services']['chat_agent']['port']}/api/v1/chat/"
        payload = {"message": message, "ticket_id": ticket_id, "session_id": session_id}
        response = requests.post(chat_url, json=payload)
        if response.status_code == 200:
            st.write("Agent:", response.json()["response"])
        else:
            st.error("Error communicating with agent")

# Feedback
st.header("Feedback")
rating = st.slider("Rate the response", 1, 5)
comments = st.text_area("Comments")
if st.button("Submit Feedback"):
    feedback_url = f"http://{config['services']['feedback']['host']}:{config['services']['feedback']['port']}/api/v1/feedback/"
    payload = {"session_id": session_id, "user_query": message, "agent_response": "", "rating": rating, "comments": comments}
    requests.post(feedback_url, json=payload)
    st.success("Feedback submitted")