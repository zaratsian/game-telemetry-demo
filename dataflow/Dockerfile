FROM apache/beam_python3.7_sdk:2.25.0

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ARG GCP_PROJECT_ID
ARG PUBSUB_TOPIC
ARG GCS_DATAFLOW_BUCKET

ENV GCP_PROJECT_ID=${GCP_PROJECT_ID}
ENV PUBSUB_TOPIC=${PUBSUB_TOPIC}
ENV GCS_DATAFLOW_BUCKET=${GCS_DATAFLOW_BUCKET}

RUN echo "GCP_PROJECT_ID: ${GCP_PROJECT_ID}"
RUN echo "PUBSUB_TOPIC:   ${PUBSUB_TOPIC}"
RUN echo "GCS_DATAFLOW_BUCKET: ${GCS_DATAFLOW_BUCKET}"

ARG pubsub_topic_path="projects/$GCP_PROJECT_ID/topics/$PUBSUB_TOPIC"
RUN echo "pubsub_topic_path: $pubsub_topic_path"

#ENTRYPOINT [ "python3", "main.py", "--gcp_project", "zproject201807", "--region", "us-central1", "--job_name", "game-events", "--gcp_staging_location", "gs://zproject201807-game-events/staging", "--gcp_tmp_location", "gs://zproject201807-game-events/tmp", "--batch_size", "10", "--pubsub_topic", "projects/zproject201807/topics/game-events", "--runner", "DirectRunner" ]
ENTRYPOINT python3 main.py --gcp_project $GCP_PROJECT_ID --region us-central1 --job_name game-events --gcp_staging_location $GCS_DATAFLOW_BUCKET/staging --gcp_tmp_location $GCS_DATAFLOW_BUCKET/tmp --batch_size 10 --pubsub_topic "projects/$GCP_PROJECT_ID/topics/$PUBSUB_TOPIC" --runner DirectRunner
