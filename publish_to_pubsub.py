# Simple script to publish payload to PubSub Topic

from google.cloud import pubsub_v1
import json

# Configuration
project_id = "my_gcp_project_id"
topic_id = "game_telemetry_topic"

# Payload
payload = {
    "eventid": "eventid_123",
    "eventtype": "spawn",
    "timestamp": 1701177119,
    "playerid": "player1001",
    "label": "no label",
    "xcoord": 1.1,
    "ycoord": 2.2,
    "zcoord": 3.3,
    "dow": 4,
    "hour": 12,
    "score": 33,
    "minutesplayed": 30,
    "timeinstore": 15,
    "ml": "",
}

# Initialize a Publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Publish the message
future = publisher.publish(topic_path, json.dumps(payload).encode("utf-8"))
print(f"Published message ID: {future.result()}")

