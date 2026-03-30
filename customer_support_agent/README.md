# Customer Support Agent

A microservices-based customer support AI agent using Langchain, FastAPI, PostgreSQL, and Streamlit.

## Architecture

- **Knowledge Base Service**: Stores and searches knowledge base documents with embeddings.
- **Ticket Retrieval Service**: Retrieves ticket details from Jira.
- **Chat Agent Service**: Main AI agent that handles customer queries.
- **Feedback Service**: Collects user feedback on responses.
- **UI**: Streamlit app for user interaction.

## Setup

1. Update `shared/config.yml` with your API keys and settings.
2. Run `docker-compose up --build` to start all services.
3. Initialize the database: `docker-compose exec postgres psql -U postgres -d customer_support -c "CREATE EXTENSION IF NOT EXISTS vector;"` (if using pgvector, but not implemented).
4. Run init script: `python shared/init_db.py`

## Usage

- Access UI at http://localhost:8501
- APIs at respective ports (8001-8004)