# Nogizaka46 Member Data ETL Pipeline

## Overview 

This project sets up an ETL (Extract, Transform, Load) pipeline for scraping Nogizaka46 member data from the official website, transforming it, and loading it into Google BigQuery. The pipeline is orchestrated using Apache Airflow, and transformations are managed with Dataform.

## Details of the ETL Pipeline

### 1. DAG (`nogi_dag.py`)

The DAG defines the workflow of the ETL process. It schedules and orchestrates the tasks.

```python
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'nogizaka46_etl',
    default_args=default_args,
    description='ETL pipeline for Nogizaka46 data',
    schedule_interval=timedelta(days=1),
)

fetch_task = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)
fetch_task >> transform_task >> load_task
```

### 2. Fetch Data (`fetch_data.py`)

This script fetches the JSON data from the Nogizaka46 API.

```python

def fetch_data():
    URL = "https://www.nogizaka46.com/s/n46/api/list/member"
    try:
        response = requests.get(URL)
        response.raise_for_status()
        json_str = response.text.strip()[4:-2]  # Remove "res (" and " ); "
        data = json.loads(json_str)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
```

### 3. Transform Data (`transform_data.py`)

This script processes and transforms the fetched data.

```python

def transform_data(data):
    transformed_data = []
    for member in data['data']:
        member_data = {
            'code': member['code'],
            'name': member['name'],
            'english_name': member.get('english_name', ''),
            'kana': member.get('kana', ''),
            'category': member.get('cate', ''),
            'image_url': member.get('img', ''),
            'profile_link': member.get('link', ''),
            'pick': member.get('pick', ''),
            'god': member.get('god', ''),
            'under': member.get('under', ''),
            'birthday': member.get('birthday', ''),
            'blood_type': member.get('blood_type', ''),
            'constellation': member.get('constellation', ''),
            'graduation': member.get('graduation', 'NO'),
            'groupcode': member.get('groupcode', ''),
        }
        transformed_data.append(member_data)
    return transformed_data
```


### 4. Load Data (`load_data.py`)

This script loads the transformed data into BigQuery.

```python
from google.cloud import bigquery
import os

def load_data(data):
    client = bigquery.Client()
    dataset_id = os.getenv('BIGQUERY_DATASET')
    table_id = os.getenv('BIGQUERY_TABLE')
    table_ref = client.dataset(dataset_id).table(table_id)
    errors = client.insert_rows_json(table_ref, data)
    if errors:
        print(f"Errors occurred while inserting rows: {errors}")
    else:
        print("Data successfully loaded to BigQuery")
```

### 5. Dataform (nogizaka46_members.sqlx)

The Dataform script for transforming data in BigQuery.

```sql
config {
  type: "table",
  bigquery: {
    partitionBy: "DATE(_PARTITIONTIME)",
    clusterBy: ["code", "name"],
    labels: {
      env: "production"
    }
  }
}

select
  code,
  name,
  english_name,
  kana,
  category,
  image_url,
  profile_link,
  pick,
  god,
  under,
  birthday,
  blood_type,
  constellation,
  graduation,
  groupcode
from
  ${ref("raw_nogizaka46_members")}
```
