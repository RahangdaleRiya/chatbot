FROM python:3.9-slim

WORKDIR /app

COPY services/knowledge_base/requirements.txt .
RUN pip install -r requirements.txt

COPY services/knowledge_base/app ./app
COPY shared ./shared

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]