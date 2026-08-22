# Airflow - Interview Prep

---

## 1. Core Concepts

- **DAG** (Directed Acyclic Graph): Collection of tasks with dependencies
- **Task**: A single unit of work (an operator instance)
- **Operator**: Defines what a task does (BashOperator, PythonOperator, etc.)
- **Scheduler**: Parses DAGs, schedules task instances
- **Executor**: Runs tasks (LocalExecutor, CeleryExecutor, KubernetesExecutor)
- **Metadata DB**: Stores state of DAGs, tasks (Postgres/MySQL)
- **Worker**: Process that executes tasks

---

## 2. DAG Anatomy

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'harsha',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email': ['alerts@company.com'],
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='my_pipeline',
    default_args=default_args,
    schedule_interval='0 6 * * *',   # daily at 6 AM
    catchup=False,                    # don't run missed historical runs
    max_active_runs=1,                # prevent parallel DAG runs
    tags=['data-engineering', 'bigquery'],
) as dag:

    def extract_data(**kwargs):
        # kwargs contains context: execution_date, task_instance, etc.
        execution_date = kwargs['ds']   # 'YYYY-MM-DD'
        print(f"Extracting for {execution_date}")
        return {'row_count': 1000}     # pushed to XCom automatically

    extract = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    transform = BashOperator(
        task_id='transform_data',
        bash_command='python /opt/scripts/transform.py --date {{ ds }}',
    )

    # Task dependencies
    extract >> transform
```

---

## 3. Key Operators

### PythonOperator
```python
from airflow.operators.python import PythonOperator

def my_func(param1, **kwargs):
    ti = kwargs['ti']
    # pull xcom
    data = ti.xcom_pull(task_ids='previous_task', key='my_key')
    return "result"

task = PythonOperator(
    task_id='run_python',
    python_callable=my_func,
    op_kwargs={'param1': 'value'},
)
```

### BigQueryOperator
```python
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

load_to_bq = BigQueryInsertJobOperator(
    task_id='load_to_bigquery',
    configuration={
        "query": {
            "query": """
                INSERT INTO `project.dataset.table`
                SELECT * FROM `project.dataset.staging`
                WHERE DATE(created_at) = '{{ ds }}'
            """,
            "useLegacySql": False,
        }
    },
    gcp_conn_id='google_cloud_default',
)
```

### GCS Operators
```python
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator

# List files in GCS
list_files = GCSListObjectsOperator(
    task_id='list_gcs_files',
    bucket='my-bucket',
    prefix='data/2024/',
    gcp_conn_id='google_cloud_default',
)

# Load GCS → BigQuery
gcs_to_bq = GCSToBigQueryOperator(
    task_id='gcs_to_bq',
    bucket='my-bucket',
    source_objects=['data/{{ ds_nodash }}/file.csv'],
    destination_project_dataset_table='project.dataset.table',
    schema_fields=[
        {'name': 'id', 'type': 'INTEGER'},
        {'name': 'name', 'type': 'STRING'},
    ],
    write_disposition='WRITE_TRUNCATE',  # or WRITE_APPEND, WRITE_EMPTY
    gcp_conn_id='google_cloud_default',
)
```

### BranchPythonOperator
```python
from airflow.operators.python import BranchPythonOperator

def decide_branch(**kwargs):
    row_count = kwargs['ti'].xcom_pull(task_ids='extract', key='row_count')
    if row_count > 0:
        return 'process_data'
    else:
        return 'skip_processing'

branch = BranchPythonOperator(
    task_id='check_data',
    python_callable=decide_branch,
)
```

---

## 4. XComs (Cross-communication)

```python
# Push XCom explicitly
def push_xcom(**kwargs):
    kwargs['ti'].xcom_push(key='my_key', value={'count': 100, 'status': 'ok'})

# Pull XCom
def pull_xcom(**kwargs):
    result = kwargs['ti'].xcom_pull(task_ids='push_task', key='my_key')
    print(result)  # {'count': 100, 'status': 'ok'}

# Implicit push - return value is auto-pushed with key='return_value'
def implicit_push():
    return "some_value"

def implicit_pull(**kwargs):
    val = kwargs['ti'].xcom_pull(task_ids='implicit_push_task')  # key defaults to 'return_value'
```

> ⚠️ XComs are stored in Airflow DB — keep them small (< few KB). Don't pass DataFrames through XCom, use GCS instead.

---

## 5. Scheduling

```
# Cron syntax
'0 6 * * *'       # Every day at 6 AM
'0 */4 * * *'     # Every 4 hours
'0 9 * * 1'       # Every Monday at 9 AM
'@daily'          # Same as '0 0 * * *'
'@hourly'         # Every hour
'None'            # Don't schedule (trigger manually)
```

### Execution Date vs Logical Date
- `{{ ds }}` = execution date (YYYY-MM-DD)
- `{{ ds_nodash }}` = 20240115
- `{{ ts }}` = full timestamp
- `{{ prev_ds }}` = previous execution date
- `{{ next_ds }}` = next execution date

---

## 6. Task Lifecycle / States

```
none → scheduled → queued → running → success
                                    → failed → up_for_retry → running...
                                    → up_for_reschedule
```

- **upstream_failed**: upstream task failed
- **skipped**: BranchOperator skipped this path
- **removed**: task removed from DAG definition

---

## 7. Connections & Variables

```python
# Using connections (stored in Airflow UI)
from airflow.hooks.base import BaseHook

conn = BaseHook.get_connection('my_postgres_conn')
host = conn.host
password = conn.password

# Using Variables
from airflow.models import Variable

bucket_name = Variable.get("gcs_bucket_name")
config = Variable.get("pipeline_config", deserialize_json=True)
```

---

## 8. Sensors

```python
from airflow.sensors.filesystem import FileSensor
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor

# Wait for file in GCS
wait_for_file = GCSObjectExistenceSensor(
    task_id='wait_for_file',
    bucket='my-bucket',
    object='data/{{ ds }}/input.csv',
    timeout=3600,          # fail after 1 hour
    poke_interval=60,      # check every minute
    mode='poke',           # or 'reschedule' (releases slot between checks)
    gcp_conn_id='google_cloud_default',
)
```

---

## 9. Debugging Failed DAGs

### Common Issues & Fixes

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| DAG not showing in UI | Syntax error or import error | Check scheduler logs |
| Task stuck in `queued` | No workers available | Check executor/worker status |
| `Broken DAG` error | Python import error | Fix imports, check `airflow dags list` |
| Connection refused | Wrong connection config | Verify connection in UI |
| XCom too large | Returning DataFrame/large obj | Store in GCS, pass path via XCom |
| Task fails silently | Exception swallowed | Add try/except with logging |

### Debugging Commands
```bash
# List DAGs
airflow dags list

# Test a specific task (doesn't mark as run)
airflow tasks test my_dag_id my_task_id 2024-01-15

# Run a DAG manually
airflow dags trigger my_dag_id

# Check task logs
airflow tasks logs my_dag_id my_task_id 2024-01-15T06:00:00

# Backfill
airflow dags backfill my_dag_id --start-date 2024-01-01 --end-date 2024-01-31

# Check scheduler logs
# Cloud Composer: View in Cloud Logging
```

---

## 10. Dynamic DAGs

```python
# Generate tasks dynamically
pipeline_configs = [
    {'source': 'users', 'table': 'dim_users'},
    {'source': 'orders', 'table': 'fact_orders'},
]

with DAG('dynamic_dag', ...):
    for config in pipeline_configs:
        task = PythonOperator(
            task_id=f"process_{config['source']}",
            python_callable=process_table,
            op_kwargs=config,
        )
```

---

## 11. Cloud Composer (GCP Managed Airflow)

- Managed Airflow on GKE
- DAGs stored in **GCS bucket** (`dags/` folder)
- Environment variables set via UI or `gcloud`
- Connections managed via Airflow UI or Secret Manager
- Monitoring via **Cloud Logging** and **Cloud Monitoring**

```bash
# Upload DAG to Composer
gcloud composer environments storage dags import \
  --environment=my-env \
  --location=us-central1 \
  --source=my_dag.py
```

---

## ❓ Likely Interview Questions

1. What is a DAG and how do you define task dependencies?
2. How do you pass data between tasks in Airflow?
3. What is the difference between `poke` and `reschedule` mode in sensors?
4. How do you handle a task that fails intermittently?
5. What is `catchup` and when would you disable it?
6. How do you trigger a DAG with parameters?
7. How do you debug a DAG that isn't showing in the Airflow UI?
8. What's the difference between `LocalExecutor` and `CeleryExecutor`?
9. How would you load data from GCS to BigQuery using Airflow?
10. How do you implement conditional branching in a DAG?
11. What happens if an upstream task fails?
12. How do you schedule a DAG to run on the last day of every month?
