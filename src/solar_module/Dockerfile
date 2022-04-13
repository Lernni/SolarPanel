FROM python:3.7 as base
WORKDIR /app
ARG CACHEBUST=1
RUN echo "$CACHEBUST"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_ENV="docker"

# https://dev.to/pacheco/dockerize-a-flask-app-and-debug-with-vscode-34i1
FROM base as debug
RUN pip install debugpy
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_DEBUG 1
ENTRYPOINT python -m debugpy --listen 0.0.0.0:5678 -m app --wait-for-client --multiprocess -m flask run

FROM base as prod
ENTRYPOINT python -m app --wait-for-client --multiprocess -m flask run