FROM python:3.9-slim

WORKDIR /app

COPY ui/requirements.txt .
RUN pip install -r requirements.txt

COPY ui/app.py .
COPY shared ./shared

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]