FROM python:3.10-slim-buster

RUN python -m pip install --upgrade pip

WORKDIR /SOCIAL_NETWORKING_BACKEND

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
