################################################################################################################
#
#   Google Cloud Dataflow
#
#   References:
#   https://cloud.google.com/dataflow/docs/
#
#   Usage:
'''
python main.py \
    --gcp_project dz-apps \
    --region us-central1 \
    --job_name 'data-stream' \
    --gcp_staging_location "gs://dz-apps-dataflow/staging" \
    --gcp_tmp_location "gs://dz-apps-dataflow/tmp" \
    --batch_size 10 \
    --pubsub_topic projects/dz-apps/topics/data-stream \
    --runner DirectRunner

python3 main.py \
    --gcp_project $GCP_PROJECT_ID \
    --region $GCP_REGION \
    --job_name game-telemetry \
    --gcp_staging_location $GCS_DATAFLOW_BUCKET/staging \
    --gcp_tmp_location $GCS_DATAFLOW_BUCKET/tmp \
    --batch_size 10 \
    --pubsub_topic "projects/$GCP_PROJECT_ID/topics/$PUBSUB_TOPIC" \
    --bq_dataset_name "dataflow_test" \
    --bq_table_name "test_table" \
    --runner DirectRunner


# Example payload to send to PubSub Topic
{
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


'''
#
################################################################################################################


from __future__ import absolute_import
import os
import logging
import argparse
import json
import apache_beam as beam
from apache_beam import window
from apache_beam.transforms import trigger
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from past.builtins import unicode

################################################################################################################
#
#   BQ Schema
#
################################################################################################################

bq_schema = {'fields': [
    {'name': "eventid", 'type': 'STRING', 'mode': 'NULLABLE'},
    {'name': "eventtype", 'type': 'STRING', 'mode': 'NULLABLE'},
    {'name': "timestamp", 'type': 'INTEGER', 'mode': 'NULLABLE'},
    {'name': "playerid", 'type': 'STRING', 'mode': 'NULLABLE'},
    {'name': "label", 'type': 'STRING', 'mode': 'NULLABLE'},
    {'name': "xcoord", 'type': 'FLOAT', 'mode': 'NULLABLE'},
    {'name': "ycoord", 'type': 'FLOAT', 'mode': 'NULLABLE'},
    {'name': "zcoord", 'type': 'FLOAT', 'mode': 'NULLABLE'},
    {'name': "dow", 'type': 'INTEGER', 'mode': 'NULLABLE'},
    {'name': "hour", 'type': 'INTEGER', 'mode': 'NULLABLE'},
    {'name': "score", 'type': 'FLOAT', 'mode': 'NULLABLE'},
    {'name': "minutesplayed", 'type': 'FLOAT', 'mode': 'NULLABLE'},
    {'name': "timeinstore", 'type': 'FLOAT', 'mode': 'NULLABLE'},
    {'name': "ml", 'type': 'STRING', 'mode': 'NULLABLE'},
]}

################################################################################################################
#
#   Functions
#
################################################################################################################

def parse_pubsub(event):
    return json.loads(event)


def preprocess_event(event):
    return ([event['playerid'],event['label']], event['minutesplayed'])


def sum_by_group(GroupByKey_tuple):
      (word, list_of_ones) = GroupByKey_tuple
      return {"name":word, "sum":sum(list_of_ones)}


def avg_by_group(GroupByKey_tuple):
    (k,v) = GroupByKey_tuple
    return {"playerid":k[0], "label": k[1], "avgMinutesPlayed": (sum(v) / len(v)) }


def print_event(event):
    print('{}'.format(event))


def run(argv=None):
    """Build and run the pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--gcp_project',          required=True,    default='gaming-demos',       help='GCP Project ID')
    parser.add_argument('--region',               required=True,    default='us-central1',        help='GCP Region')
    parser.add_argument('--job_name',             required=True,    default='antidote-ensemble',  help='Dataflow Job Name')
    parser.add_argument('--gcp_staging_location', required=True,    default='gs://xxxxx/staging', help='Dataflow Staging GCS location')
    parser.add_argument('--gcp_tmp_location',     required=True,    default='gs://xxxxx/tmp',     help='Dataflow tmp GCS location')
    parser.add_argument('--batch_size',           required=True,    default=10,                   help='Dataflow Batch Size')
    parser.add_argument('--pubsub_topic',         required=True,    default='',                   help='Input PubSub Topic: projects/<project_id>/topics/<topic_name>')#parser.add_argument('--bq_dataset_name',      required=True,   default='',                   help='Output BigQuery Dataset')
    parser.add_argument('--bq_dataset_name',      required=True,    default='',                   help='BigQuery Dataset, used as data sink')
    parser.add_argument('--bq_table_name',        required=True,    default='',                   help='BigQuery Table, used as data sink')
    parser.add_argument('--runner',               required=True,    default='DirectRunner',       help='Dataflow Runner - DataflowRunner or DirectRunner (local)')

    known_args, pipeline_args = parser.parse_known_args(argv)
    
    pipeline_args.extend([
          '--runner={}'.format(known_args.runner),                          # DataflowRunner or DirectRunner (local)
          '--project={}'.format(known_args.gcp_project),
          '--staging_location={}'.format(known_args.gcp_staging_location),  # Google Cloud Storage gs:// path
          '--temp_location={}'.format(known_args.gcp_tmp_location),         # Google Cloud Storage gs:// path
          '--job_name=' + str(known_args.job_name),
      ])
    
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(StandardOptions).streaming = True
    
    print('[ INFO ] GCP PROJECT ID: {}'.format(known_args.gcp_project))
    os.environ['GOOGLE_CLOUD_PROJECT'] = known_args.gcp_project
    ###################################################################
    #   DataFlow Pipeline
    ###################################################################
    
    with beam.Pipeline(options=pipeline_options) as p:
        
        # Get PubSub Topic
        logging.info('Ready to process events from PubSub topic: {}'.format(known_args.pubsub_topic)) 
        events = ( 
                 p  | 'raw events' >> beam.io.ReadFromPubSub(known_args.pubsub_topic) 
        )
        
        # Parse events
        parsed_events = (
            events  | 'parsed events' >> beam.Map(parse_pubsub)
        )
        
        # Event Window Transform
        '''
        event_window = (
            parsed_events | 'window' >> beam.Map(preprocess_event)
                           | beam.WindowInto(window.SlidingWindows(60, 10)) # Window is 60 seconds in length, and a new window begins every 10 seconds
                           | beam.GroupByKey()
                           | beam.Map(avg_by_group)
        )
        '''
        
        # Print results to console (for testing/debugging)
        parsed_events | 'print event'   >> beam.Map(print_event)
        
        # Sink/Persist to BigQuery
        parsed_events | 'Write to bq' >> beam.io.gcp.bigquery.WriteToBigQuery(
                        project=known_args.gcp_project,
                        dataset=known_args.bq_dataset_name,
                        table=known_args.bq_table_name,
                        schema=bq_schema,
                        batch_size=int(known_args.batch_size)
                        )

        # Sink data to PubSub
        #output | beam.io.WriteToPubSub(known_args.output_topic)


################################################################################################################
#
#   Main
#
################################################################################################################

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()

