FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV GCP_PROJECT_ID=${GCP_PROJECT_ID}
ENV GCP_PROJECT_ID=${GCP_PROJECT_ID}
ENV GCP_PROJECT_ID=${GCP_PROJECT_ID}

ENTRYPOINT [ "python3", "event_simulator.py"]

#ZEND
