# Load config
. ./config

# Create GCP PubSub Topics
gcloud pubsub topics create ${PUBSUB_TOPIC}

# Create GCP PubSub Subscriptions
gcloud pubsub subscriptions create ${PUBSUB_TOPIC}-sub --topic ${PUBSUB_TOPIC}

# Dataflow Setup
gsutil mkdir ${GCS_DATAFLOW_BUCKET}

