FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ARG GCP_PROJECT_ID
ARG PUBSUB_TOPIC

ENV GCP_PROJECT_ID=${GCP_PROJECT_ID}
ENV PUBSUB_TOPIC=${PUBSUB_TOPIC}

ENTRYPOINT [ "python3", "event_simulator.py"]

