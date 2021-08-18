# Stop and remove Simulator process
docker stop event_simulator 
docker rm -f event_simulator

# Stop and remove Dataflow process
docker stop dataflow_stream
docker rm -f dataflow_stream

