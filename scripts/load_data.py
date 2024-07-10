from google.cloud import bigquery
import json
import os

def load_data():
    client = bigquery.Client()

    dataset_id = os.getenv('BIGQUERY_DATASET')
    table_id = os.getenv('BIGQUERY_TABLE')

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    with open('/tmp/transformed_nogizaka46_data.json') as infile:
        rows_to_insert = json.load(infile)

    errors = client.insert_rows_json(table_ref, rows_to_insert)
    if errors == []:
        print("Data successfully loaded into BigQuery")
    else:
        print(f"Errors occurred: {errors}")