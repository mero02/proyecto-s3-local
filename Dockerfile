FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
COPY frontend/ ./frontend

EXPOSE 5000

CMD ["python", "app.py"]