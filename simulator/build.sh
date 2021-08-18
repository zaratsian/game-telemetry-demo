# Load config
. ../config

# Build docker container
docker rmi -f event_simulator
docker build --tag event_simulator .
