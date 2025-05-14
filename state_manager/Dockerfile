FROM python:3.12-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY state_manager ./state_manager

EXPOSE 8000

CMD ["uvicorn", "state_manager.main:app", "--host", "0.0.0.0", "--port", "8000"]
