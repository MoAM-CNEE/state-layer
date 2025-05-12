FROM python:3.12-bookworm

WORKDIR "/state_manager"

COPY state_manager/ .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000
