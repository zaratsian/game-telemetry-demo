# Load Config
. ./config

# Build Simulator Container
docker rmi -f event_simulator
docker build --tag event_simulator \
--build-arg GCP_PROJECT_ID=${GCP_PROJECT_ID} \
--build-arg PUBSUB_TOPIC=${PUBSUB_TOPIC} \
simulator/.

# Build Dataflow Container
docker rmi -f dataflow_stream
docker build --tag dataflow_stream \
--build-arg GCP_PROJECT_ID=${GCP_PROJECT_ID} \
--build-arg PUBSUB_TOPIC=${PUBSUB_TOPIC} \
--build-arg GCS_DATAFLOW_BUCKET=${GCS_DATAFLOW_BUCKET} \
dataflow/.

