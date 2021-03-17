FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT FLASK_APP=/app/test_api.py flask run --host=0.0.0.0 --port=5001