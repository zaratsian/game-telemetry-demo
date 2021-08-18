# Google Cloud - Data Streaming

**Dependenies:**

* [Docker](https://docs.docker.com/get-docker/) must be installed.

**Update Config File**

Before you begin, update the [config](./config) file based on your GCP project settings and desired naming convensions. 

**Initial GCP Setup:**
```
01-setup.sh
```

**Build the containers (one for the simulator and the other for dataflow/beam)**

```
./02-build-containers.sh
```

**To start real-time Dataflow processing:**

Run the following command to start the dataflow/beam processing engine. It will run in interactive mode (DirectRunner). All processed events will be written to the terminal so that results can be viewed in real-time.

```
./03-demo-start-dataflow.sh
```

**To start the simulator:**

In a new terminal, run the following command to start the simulated event stream:

```
./04-demo-start-simulated-event-stream.sh
```

---

**Stop / shutdown all containers**

```
./stop-demo.sh
```
