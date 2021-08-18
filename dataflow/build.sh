# Load config
. ../config

# Build docker container
docker rmi -f dataflow_stream
docker build --tag dataflow_stream . 
