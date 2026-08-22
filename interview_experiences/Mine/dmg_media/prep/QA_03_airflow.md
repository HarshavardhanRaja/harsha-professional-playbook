# Airflow - Most Asked Interview Questions & Answers

---

## Q1. What is Apache Airflow? What problem does it solve?

**Answer:**

Apache Airflow is an open-source **workflow orchestration platform** used to programmatically author, schedule, and monitor data pipelines.

**Problem it solves:** Before Airflow, pipelines were often run via cron jobs — simple but brittle. With Airflow:
- Pipelines are **code** (Python), so they're version-controlled, testable, reviewable
- Dependencies between tasks are explicit (task A must succeed before B starts)
- **Visibility** — you can see DAG status, task logs, history, and failure reasons in a UI
- **Retries, alerting, backfill** — built-in
- **Scheduling** — cron expressions, but also catchup, depends_on_past, etc.

**Key components:**
- **Scheduler** — parses DAGs, decides what to run and when
- **Executor** — actually runs tasks (Local, Celery, Kubernetes)
- **Web server** — UI for monitoring
- **Metadata DB** — stores task state, logs, XComs (Postgres/MySQL)
- **Workers** — processes that execute tasks

---

## Q2. What is a DAG? What makes something a valid DAG?

**Answer:**

A **DAG (Directed Acyclic Graph)** is a collection of tasks with defined dependencies, where:
- **Directed** = dependencies flow in one direction (task A → task B)
- **Acyclic** = no cycles (task B cannot depend on task A if A depends on B)

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    dag_id='my_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='0 6 * * *',    # daily at 6 AM
    catchup=False,
    default_args={
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
        'email_on_failure': True,
    }
) as dag:

    task_a = PythonOperator(task_id='extract', python_callable=extract_fn)
    task_b = PythonOperator(task_id='transform', python_callable=transform_fn)
    task_c = PythonOperator(task_id='load', python_callable=load_fn)

    # Dependencies: extract → transform → load
    task_a >> task_b >> task_c
```

**Valid DAG rules:**
- No circular dependencies
- All tasks must have a `task_id` unique within the DAG
- `start_date` must be in the past (or Airflow won't schedule it)
- DAG file must be importable without errors

---

## Q3. What is `catchup` and why would you set it to False?

**Answer:**

When `catchup=True` (default), if your DAG has a `start_date` of 1 Jan and you deploy it in March, Airflow will **backfill all missed runs** from January to now — potentially hundreds of runs.

**When to set `catchup=False`:**
- You don't want historical runs (e.g., a report that's only meaningful today)
- You're deploying a new DAG and don't want it to flood with old runs
- You process only "current" data (e.g., today's API pull)

```python
with DAG(
    dag_id='daily_report',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,            # ← only run from NOW onwards
) as dag: ...
```

**When to keep `catchup=True`:**
- You need to process historical data (e.g., loading last 6 months into BQ)
- Your pipeline is truly idempotent and re-running old dates is correct behavior

---

## Q4. How do you pass data between tasks in Airflow? What are XComs?

**Answer:**

**XCom (Cross-communication)** is Airflow's mechanism for tasks to share small pieces of data. XComs are stored in the Airflow metadata database.

```python
# Task 1: Push to XCom
def extract(**kwargs):
    data = fetch_from_api()
    # Method 1: Return value (auto-pushed with key='return_value')
    return {'row_count': len(data), 'file_path': 'gs://bucket/file.csv'}

# Task 2: Pull from XCom
def transform(**kwargs):
    ti = kwargs['ti']  # task instance
    # Pull from specific task
    result = ti.xcom_pull(task_ids='extract')  # key='return_value' by default
    file_path = result['file_path']
    row_count = result['row_count']

    # Or explicit key push/pull:
    ti.xcom_push(key='output_path', value='gs://bucket/transformed.parquet')

def load(**kwargs):
    ti = kwargs['ti']
    path = ti.xcom_pull(task_ids='transform', key='output_path')
```

**XCom limitations:**
- Stored in the metadata DB → keep payloads **small** (< a few KB)
- **NEVER** pass DataFrames, large lists, or file contents via XCom
- For large data: write to GCS → pass the GCS path via XCom

---

## Q5. What's the difference between poke and reschedule mode in sensors?

**Answer:**

Sensors wait for a condition (file exists, partition ready, API response) before proceeding.

### Poke Mode (default)
- Worker **holds the slot** and checks every `poke_interval` seconds
- Uses up a worker slot for the entire wait duration
- OK for short waits (< few minutes)

### Reschedule Mode
- Worker **releases the slot** between checks
- Scheduler re-queues the sensor task on each check
- No slot wastage during the wait
- Best for long waits (waiting hours for a file)

```python
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor

wait_for_file = GCSObjectExistenceSensor(
    task_id='wait_for_file',
    bucket='my-bucket',
    object='data/{{ ds }}/input.csv',
    timeout=7200,          # fail if not found within 2 hours
    poke_interval=120,     # check every 2 minutes
    mode='reschedule',     # ← recommended for long waits
    gcp_conn_id='google_cloud_default',
)
```

---

## Q6. A task is failing. Walk me through how you debug it.

**Answer:**

**Step 1: Check the UI**
- Go to Airflow UI → your DAG → click the failing task → View Log
- Look for the actual Python traceback / error message

**Step 2: Common error patterns**
```
ModuleNotFoundError      → missing Python package, wrong environment
FileNotFoundError        → wrong file path, GCS path doesn't exist
KeyError                 → XCom value not found, dict key missing
ConnectionError          → Airflow connection misconfigured
Operator.execute failed  → look at the root cause in the stack trace
```

**Step 3: Test the task locally**
```bash
# Run task without marking it as run in DB
airflow tasks test my_dag_id my_task_id 2024-01-15
```

**Step 4: Check the DAG itself**
```bash
# Check for import errors
python /path/to/dag.py
airflow dags list-import-errors
```

**Step 5: Add debug logging**
```python
import logging
logger = logging.getLogger(__name__)

def my_task(**kwargs):
    logger.info(f"Input: {kwargs['ds']}")
    logger.info(f"XCom value: {kwargs['ti'].xcom_pull(task_ids='prev_task')}")
```

**Step 6: Clear and retry**
- From UI: Task Instance → Clear → re-runs the specific task
- Or: `airflow tasks clear my_dag my_task -s 2024-01-15`

---

## Q7. What happens when an upstream task fails?

**Answer:**

If task A fails and B depends on A, then B gets status `upstream_failed` and is **skipped** — it doesn't even attempt to run. The same propagates downstream.

```
extract (FAILED) → transform (upstream_failed) → load (upstream_failed)
```

**Controlling this behavior:**

```python
# Make a task run even if upstream failed (e.g., cleanup or alert task)
from airflow.utils.trigger_rule import TriggerRule

notify = PythonOperator(
    task_id='send_failure_alert',
    python_callable=send_alert,
    trigger_rule=TriggerRule.ONE_FAILED,  # run if at least one upstream failed
)

# TriggerRule options:
# ALL_SUCCESS (default) - run only if ALL upstreams succeeded
# ALL_FAILED           - run only if ALL upstreams failed
# ALL_DONE             - run when ALL upstreams are done (any state)
# ONE_FAILED           - run as soon as ONE upstream fails
# ONE_SUCCESS          - run as soon as ONE upstream succeeds
# NONE_FAILED          - run if no upstream failed (including skipped)
```

---

## Q8. How does Airflow handle retries? How do you configure them?

**Answer:**

```python
from datetime import timedelta

default_args = {
    'retries': 3,                              # retry up to 3 times
    'retry_delay': timedelta(minutes=5),       # wait 5 min between retries
    'retry_exponential_backoff': True,          # 5min, 10min, 20min...
    'max_retry_delay': timedelta(hours=1),     # cap backoff at 1 hour
    'email_on_retry': False,                   # don't email on every retry
    'email_on_failure': True,                  # email only on final failure
}

# Or per-task override:
risky_task = PythonOperator(
    task_id='call_flaky_api',
    python_callable=fetch_api_data,
    retries=5,
    retry_delay=timedelta(minutes=2),
    retry_exponential_backoff=True,
)
```

**Behavior:** After each retry, task state = `up_for_retry` → then attempts again. After all retries exhausted, state = `failed`.

---

## Q9. What is the Airflow execution date and how does it differ from the actual run time?

**Answer:**

This is one of Airflow's most confusing concepts.

- **Execution date** = the **logical date** of the DAG run (when the interval started)
- **Actual run time** = when the DAG actually started running (always later)

**Example:** For a daily DAG with `schedule_interval='@daily'` and `start_date=2024-01-01`:
- Run for Jan 1 data → execution_date = `2024-01-01`, but it **runs on Jan 2** (at the end of the interval)

```python
def my_task(**kwargs):
    execution_date = kwargs['ds']           # '2024-01-01' (logical date)
    execution_datetime = kwargs['ts']       # full ISO timestamp
    prev_ds = kwargs['prev_ds']            # '2023-12-31'
    next_ds = kwargs['next_ds']            # '2024-01-02'
    data_interval_start = kwargs['data_interval_start']  # Airflow 2.2+
    data_interval_end = kwargs['data_interval_end']
```

**Why it matters:** When you query `WHERE DATE(ts) = '{{ ds }}'`, you're getting the data for the logical day, not the day the pipeline ran. This is usually what you want.

---

## Q10. How do you handle dynamic DAGs (generating tasks from config)?

**Answer:**

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Config-driven: one task per source
SOURCES = [
    {'name': 'users', 'table': 'dim_users', 'key_col': 'user_id'},
    {'name': 'orders', 'table': 'fact_orders', 'key_col': 'order_id'},
    {'name': 'products', 'table': 'dim_products', 'key_col': 'product_id'},
]

def load_source(source_config: dict, **kwargs):
    print(f"Loading {source_config['name']} into {source_config['table']}")

with DAG(
    dag_id='dynamic_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
) as dag:

    start = PythonOperator(task_id='start', python_callable=lambda: print('Starting'))
    end = PythonOperator(task_id='end', python_callable=lambda: print('Done'))

    for source in SOURCES:
        task = PythonOperator(
            task_id=f"load_{source['name']}",
            python_callable=load_source,
            op_kwargs={'source_config': source},
        )
        start >> task >> end
```

**Best practices for dynamic DAGs:**
- Keep the config file/list static (or loaded from a Variable) — avoid DB queries at DAG parse time
- DAG parsing happens frequently — keep it fast (no API calls at top level)
- Use `dag_id` naming conventions to identify dynamic DAGs

---

## Q11. How do you trigger a DAG with parameters (conf)?

**Answer:**

```python
# In the DAG, access triggered parameters via kwargs['dag_run'].conf
def my_task(**kwargs):
    conf = kwargs['dag_run'].conf or {}
    run_date = conf.get('run_date', kwargs['ds'])  # fall back to scheduled date
    env = conf.get('environment', 'prod')
    print(f"Processing {run_date} in {env}")
```

**Trigger with conf from CLI:**
```bash
airflow dags trigger my_dag_id --conf '{"run_date": "2024-01-15", "environment": "staging"}'
```

**Trigger from Python:**
```python
from airflow.api.client.local_client import Client
client = Client(None, None)
client.trigger_dag('my_dag_id', conf={'run_date': '2024-01-15'})
```

**Via REST API (Airflow 2.0+):**
```bash
curl -X POST "http://airflow:8080/api/v1/dags/my_dag_id/dagRuns" \
  -H "Content-Type: application/json" \
  -d '{"conf": {"run_date": "2024-01-15"}}'
```

---

## Q12. What is the difference between LocalExecutor, CeleryExecutor, and KubernetesExecutor?

**Answer:**

| Executor | How it works | Best for |
|----------|-------------|---------|
| **SequentialExecutor** | One task at a time in same process | Dev/testing only |
| **LocalExecutor** | Multiple tasks using multiprocessing on one machine | Small-medium workloads |
| **CeleryExecutor** | Distributes tasks to Celery workers (multiple machines) | Large-scale, multi-worker |
| **KubernetesExecutor** | Each task runs in its own Kubernetes Pod | Full isolation, scaling |

**Cloud Composer** uses **CeleryExecutor** (or KubernetesExecutor in Composer 2) behind the scenes.

**For interviews:** Say CeleryExecutor is the most common in production — Celery queue + Redis/RabbitMQ broker distributes tasks to multiple workers. KubernetesExecutor is ideal when tasks have different dependencies (each Pod can have its own environment).

---

## Q13. How do you implement a backfill in Airflow?

**Answer:**

Backfill = run a DAG for historical dates (useful when adding a new pipeline or fixing a bug in old runs).

```bash
# Backfill specific date range
airflow dags backfill my_dag_id \
  --start-date 2024-01-01 \
  --end-date 2024-01-31

# Backfill with parallelism
airflow dags backfill my_dag_id \
  --start-date 2024-01-01 \
  --end-date 2024-01-31 \
  --max-active-runs 5   # run 5 days in parallel
```

**Considerations:**
- Make sure the DAG is **idempotent** before backfilling (safe to rerun)
- Set `catchup=True` or backfill will skip historical dates
- For very large backfills, consider running in batches to avoid overwhelming the source

---

## Q14. How would you design a DAG to load GCS data to BigQuery daily?

**Answer:**

```python
from airflow import DAG
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def validate_data(**kwargs):
    """Run data quality checks after load."""
    from google.cloud import bigquery
    client = bigquery.Client()
    result = client.query(f"""
        SELECT COUNT(*) as cnt
        FROM `project.dataset.staging`
        WHERE DATE(loaded_at) = '{kwargs["ds"]}'
    """).result()
    count = list(result)[0]['cnt']
    if count == 0:
        raise ValueError(f"No data loaded for {kwargs['ds']}")

with DAG(
    dag_id='gcs_to_bq_daily',
    start_date=datetime(2024, 1, 1),
    schedule_interval='0 7 * * *',    # 7 AM daily
    catchup=False,
    default_args={'retries': 2, 'retry_delay': timedelta(minutes=5)},
) as dag:

    # 1. Wait for source file to land in GCS
    wait_for_file = GCSObjectExistenceSensor(
        task_id='wait_for_file',
        bucket='my-data-bucket',
        object='raw/{{ ds_nodash }}/events.csv',
        timeout=3600,
        poke_interval=300,
        mode='reschedule',
        gcp_conn_id='google_cloud_default',
    )

    # 2. Load GCS → BQ staging
    load_to_staging = GCSToBigQueryOperator(
        task_id='load_to_staging',
        bucket='my-data-bucket',
        source_objects=['raw/{{ ds_nodash }}/events.csv'],
        destination_project_dataset_table='project.dataset.events_staging',
        source_format='CSV',
        skip_leading_rows=1,
        write_disposition='WRITE_TRUNCATE',
        autodetect=True,
        gcp_conn_id='google_cloud_default',
    )

    # 3. Validate loaded data
    validate = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
    )

    # 4. Merge staging → production
    merge_to_prod = BigQueryInsertJobOperator(
        task_id='merge_to_production',
        configuration={
            "query": {
                "query": """
                    MERGE `project.dataset.events` T
                    USING `project.dataset.events_staging` S
                    ON T.event_id = S.event_id
                    WHEN MATCHED THEN UPDATE SET T.value = S.value
                    WHEN NOT MATCHED THEN INSERT ROW
                """,
                "useLegacySql": False,
            }
        },
        gcp_conn_id='google_cloud_default',
    )

    # Define pipeline order
    wait_for_file >> load_to_staging >> validate >> merge_to_prod
```

---

## Q15. What is depends_on_past and when would you use it?

**Answer:**

`depends_on_past=True` means a task will **only run if the same task in the previous DAG run succeeded**.

```python
default_args = {
    'depends_on_past': True,   # each run depends on previous run's success
}
```

**Use case:** Incremental pipelines where today's load depends on yesterday's being correct. E.g., rolling aggregations, cumulative totals, sequential processing.

**Gotcha:** If a task fails and you have `depends_on_past=True`, ALL subsequent runs will be blocked. You must manually mark the failed instance as success or clear it before future runs will proceed.

**`wait_for_downstream`**: Similar but stricter — the task waits for the immediately downstream tasks (not just itself) from the previous run to also succeed.
