FROM python:3.12-bookworm

WORKDIR "/app"

COPY src/* .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000
