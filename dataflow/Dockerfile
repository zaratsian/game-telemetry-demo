FROM apache/beam_python3.7_sdk:2.25.0

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "main.py", "--gcp_project", ${GCP_PROJECT_ID}, "--region", "us-central1", "--job_name", "game-events", "--gcp_staging_location", "${GCS_DATAFLOW_BUCKET}/staging", "--gcp_tmp_location", "${GCS_DATAFLOW_BUCKET}/tmp", "--batch_size", "10", "--pubsub_topic", "projects/${GCP_PROJECT_ID}/topics/${PUBSUB_TOPIC}", "--runner", "DirectRunner" ]


