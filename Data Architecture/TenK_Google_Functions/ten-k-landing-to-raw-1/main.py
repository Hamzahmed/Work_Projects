import os
from google.cloud import storage
from google.cloud import bigquery
from flask import request
from google.cloud import pubsub_v1
import multiprocessing
import json

def run_query(query_name, dataset_name=None):
    bq_client = bigquery.Client(project='methodologysandbox')
    gs = storage.Client()
    path = os.path.join('LANDING_TO_RAW_SQL', f'{query_name}.sql')
    bucket_name = 'data-warehouse-tables-transformations'
    bucket = gs.get_bucket(bucket_name)
    blob = bucket.blob(path)
    query_bytes = blob.download_as_bytes()
    query_content = query_bytes.decode('utf-8')
    query_job = bq_client.query(query_content)  # API request
    rows = query_job.result()  # Waits for the query to finish
    for row in rows:
        print(row.name)
    return rows

def run_query_parallel(query_name):
    try:
        print(f'{query_name} started')
        run_query(query_name)
        print(f'{query_name} completed')
    except:
        print(f'{query_name} failed')

def run_landing_to_raw(request):
    data = request.get_json()  # JSON data
        
    try:
        # Acknowledge the message
        subscriber = pubsub_v1.SubscriberClient()
        ack_request = pubsub_v1.AcknowledgeRequest(
            subscription=data['subscription'],
            ack_ids=[data['message']['message_id']],
        )
        
        try:
            subscriber.acknowledge(ack_request)
        except Exception as e:
            print(f'WARN: Exception raised - {e}')
            print("No subscription to acknowledge")
    except Exception as e:
        print(f'WARN: Exception raised - {e}')
        print("Non-standard message format received")
        print(f"Message content:\n{data}")
    
    print(data)
    gs = storage.Client()
    bucket_name = 'data-warehouse-tables-transformations'
    path = os.path.join('LANDING_TO_RAW_SQL', 'LANDING_TO_RAW_query_names.txt')
    bucket = gs.get_bucket(bucket_name)
    blob = bucket.blob(path)
    bytes = blob.download_as_bytes()
    content = bytes.decode('utf-8')
    query_names = content.split(',\n')
    print('Executing Queries:')
    print(query_names)
    
    # Parallelize query execution using multiprocessing
    pool = multiprocessing.Pool()
    pool.map(run_query_parallel, query_names)
    pool.close()
    pool.join()
    
    def publish_message(project_id, topic_id, message):
        # Initialize the PublisherClient
        publisher = pubsub_v1.PublisherClient()

        # Create the topic path
        topic_path = publisher.topic_path(project_id, topic_id)

        # Convert the message to a JSON string
        message_json = json.dumps(message)

        # Convert the message string to bytes
        message_bytes = message_json.encode('utf-8')

        # Publish the message to the topic
        future = publisher.publish(topic_path, data=message_bytes)

        # Get the message ID from the future object
        message_id = future.result()

        # Print the message ID
        print(f"Published message: {message_id}")
        
    project_id = 'methodologysandbox'
    topic_id = 'TenK_Orchestration_RAW_TO_REFINED'
    message = {'command': 'RAW_TO_REFINED_GO'}

    publish_message(project_id, topic_id, message)

    return "Landing to raw queries completed"
