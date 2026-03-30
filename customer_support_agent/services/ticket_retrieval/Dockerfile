FROM python:3.9-slim

WORKDIR /app

COPY services/ticket_retrieval/requirements.txt .
RUN pip install -r requirements.txt

COPY services/ticket_retrieval/app ./app
COPY shared ./shared

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]