FROM python:3.10

WORKDIR .

ENV PYTHONPATH "${PYTHONPATH}:/app"


COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .


CMD alembic upgrade head && uvicorn app.main:app --host "0.0.0.0" --port 8000 --workers 4 --reload