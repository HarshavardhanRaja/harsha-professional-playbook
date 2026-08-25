# Airflow — Pre-Interview Reference & Complete Answers
# Sharp, skimmable, complete. Read this before your interview.

---

# PART 1 — CORE ARCHITECTURE & COMPONENTS

## The 4 Core Components
1. **Webserver (UI):** Renders DAG runs, task status, execution logs, and connections.
2. **Metadata Database (PostgreSQL):** Stores the state of all DAGs, TaskInstances, connections, variables, and XComs.
3. **Scheduler:** The daemon/heartbeat that monitors DAG definitions, resolves task dependencies, creates DAG Runs when intervals finish, and sends tasks to the executor queue.
4. **Executor & Workers:** 
   - **Executor:** Mechanism deciding HOW work is allocated (Local, Celery, Kubernetes).
   - **Workers:** The actual processes/containers that execute the task logic.

---

## Executors Comparison

| Executor | How it works | Best For |
|---|---|---|
| **SequentialExecutor** | Runs 1 task at a time with SQLite | Local debugging only |
| **LocalExecutor** | Multiprocessing on a single server | Small/single-VM deployments |
| **CeleryExecutor** | Distributed worker nodes picking tasks from Redis/RabbitMQ queue | Standard production (**Cloud Composer 1**) |
| **KubernetesExecutor** | Dynamically spins up an isolated Kubernetes Pod per task | Dynamic auto-scaling & dependency isolation (**Cloud Composer 2/3**) |

---

## Operators vs Tasks vs TaskInstances
- **Operator:** The template class defining what to do (e.g. `PythonOperator`, `GCSToBigQueryOperator`).
- **Task:** An instantiated operator configured inside a DAG with a `task_id` and parameters.
- **TaskInstance (TI):** A specific execution of a task for a specific execution date/interval. Has states: `queued`, `running`, `success`, `failed`, `up_for_retry`, `skipped`.

---

# PART 2 — SCHEDULING & CATCHUP

## Scheduling Logic (The Interval Rule)
Airflow runs a DAG at the **END** of its scheduled period, not the beginning.
- Daily DAG with `start_date = 2024-01-01` scheduled at `@daily` (`0 0 * * *`).
- The run for interval `2024-01-01 -> 2024-01-02` executes on **2024-01-02 00:00:00**.
- Reason: Airflow waits for the full day's data to be recorded before extracting it.

## Template Variables (`{{ ds }}`)
- `{{ ds }}` = `YYYY-MM-DD` (Start of data interval / logical date).
- `{{ ds_nodash }}` = `YYYYMMDD`.
- `{{ prev_ds }}` = Previous execution date.
- `{{ next_ds }}` = Next execution date.
- Always use `{{ ds }}` in SQL queries and file paths so backfills and retries process the exact correct historical date slice.

## `catchup=False` vs `catchup=True`
- **`catchup=True` (Default in older versions):** Airflow automatically runs all missed historical intervals between `start_date` and today.
- **`catchup=False`:** Airflow only schedules the current interval and ignores historical backlog.
- **Production rule:** Set `catchup=False` in DAG definitions to prevent accidental cluster overload. If historical runs are needed, use manual CLI backfill.

## Manual Backfill Command
```bash
airflow dags backfill \
    --start-date 2024-01-01 \
    --end-date 2024-01-07 \
    --reset-dagruns \
    my_dag_id
```

---

# PART 3 — SENSORS: POKE VS RESCHEDULE

## What a Sensor is
A sensor is a task that waits for an external condition to be met (file arrival in GCS, table partition updated in BQ, HTTP endpoint returning 200) before downstream tasks execute.

## `mode='poke'` vs `mode='reschedule'` (Crucial Interview Question)

- **`mode='poke'` (Default):**
  - Worker executes the check, sleeps for `poke_interval` seconds, and checks again.
  - **Problem:** Occupies a worker slot/thread continuously during sleep.
  - Causes worker pool starvation if files are delayed.
- **`mode='reschedule'`:**
  - Worker runs the check once. If condition not met, task state becomes `up_for_reschedule` and **releases the worker slot**.
  - Scheduler spins it back up when `poke_interval` elapses.
  - **Rule:** Always use `mode='reschedule'` for any sensor expecting to wait more than 2 minutes.

```python
wait_for_gcs = GCSObjectExistenceSensor(
    task_id="wait_for_file",
    bucket="dmg-media-raw",
    object="events/{{ ds }}/data.parquet",
    poke_interval=300,
    timeout=3600 * 4,
    mode="reschedule",  # Frees worker slot between checks
)
```

---

# PART 4 — XCOMS (CROSS-COMMUNICATION)

## What it is
Airflow's mechanism for passing small metadata between tasks within the same DAG run.

```python
# Task 1: Returns value (automatically pushed to XCom key='return_value')
def extract(**context):
  return "gs://dmg-bucket/20240115/data.parquet"


# Task 2: Pulls value from upstream task
def load(**context):
  file_uri = context["ti"].xcom_pull(task_ids="extract")
  print(f"Loading {file_uri}")
```

## The XCom Limit & Anti-Pattern
- XCom values are serialized (JSON/Pickle) and stored in the **Metadata Database (PostgreSQL)**.
- Size limit is ~48KB.
- **Anti-pattern:** Passing DataFrames, large query outputs, or raw file contents through XCom. This crashes the metadata DB.
- **Best Practice:** Store data in **GCS / BigQuery**, and pass only the URI path or table reference via XCom.

---

# PART 5 — TRIGGER RULES & BRANCHING

## Branching with `BranchPythonOperator`
Routes execution down one specific branch based on runtime evaluation:

```python
from airflow.operators.python import BranchPythonOperator


def evaluate_branch(**context):
  row_count = context["ti"].xcom_pull(task_ids="check_source")
  if row_count == 0:
    return "skip_processing_task"
  return "run_etl_pipeline_task"


branch = BranchPythonOperator(task_id="branch", python_callable=evaluate_branch)
```

## Trigger Rules
By default, downstream tasks have `trigger_rule='all_success'`. In branching or error handling pipelines:
- `all_success`: Default. All direct upstream tasks must have succeeded.
- `all_done`: Runs when all upstreams finish, regardless of success/failure (great for cleanup & tear-down tasks).
- `none_failed_min_one_success`: Ideal after a branch; runs if at least one branch succeeded and none failed.
- `one_failed`: Triggers error notification tasks.

---

# PART 6 — CROSS-DAG DEPENDENCIES & ADVANCED PATTERNS

## 1. Cross-DAG Dependencies (3 Patterns)
- **`TriggerDagRunOperator` (Push):** Upstream DAG explicitly triggers downstream DAG upon completion.
  ```python
  TriggerDagRunOperator(
      task_id="trigger_downstream",
      trigger_dag_id="downstream_dag_id",
      conf={"execution_date": "{{ ds }}"},
  )
  ```
- **`ExternalTaskSensor` (Pull):** Downstream DAG pauses and waits for upstream task/DAG execution.
  ```python
  ExternalTaskSensor(
      task_id="wait_for_upstream",
      external_dag_id="upstream_dag_id",
      external_task_id=None,  # Waits for whole DAG
      mode="reschedule",
  )
  ```
- **Data-Aware Scheduling / `Datasets` (Airflow 2.4+ - Modern):** Downstream DAG triggers as soon as upstream writes to a defined `Dataset("gcs://bucket/file.parquet")`.

---

## 2. `depends_on_past` vs `wait_for_downstream`
- **`depends_on_past=True`:** Task for today (`2024-01-15`) will NOT run if the same task failed on yesterday (`2024-01-14`). Used for stateful cumulative pipelines.
- **`wait_for_downstream=True`:** Task for today will not run until the entire downstream dependency chain from yesterday has completed.

---

## 3. `TaskGroup` vs `SubDAG`
- `SubDAG` is deprecated (caused deadlocks and resource contention).
- `TaskGroup` is a lightweight UI abstraction to group tasks visually with zero scheduling overhead.

---

## 4. Pools & Concurrency Control
- **Pools:** Used to limit concurrent connections to external systems (e.g. rate-limited REST APIs or production DBs).
- Define a pool in UI with `limit=5`, then set `pool="crm_api_pool"` on tasks. Airflow restricts concurrent executions across all DAGs to 5.

---

## 5. Dynamic Task Mapping (`.expand()`)
Airflow 2.3+ feature to create tasks dynamically at runtime based on upstream list outputs:
```python
@task
def get_files():
  return ["f1.csv", "f2.csv", "f3.csv"]


@task
def process_file(filename):
  return f"Processed {filename}"


files = get_files()
process_file.expand(filename=files)  # Spawns 3 tasks in parallel
```

---

# PART 7 — PRODUCTION GCP AIRFLOW DAG PATTERN

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryInsertJobOperator,
)
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)

default_args = {
    "owner": "data_engineering",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "email_on_failure": True,
}

with DAG(
    dag_id="daily_dmg_media_ingestion",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="0 5 * * *",  # 5 AM UTC daily
    catchup=False,
    max_active_runs=1,
) as dag:

  # 1. Wait for file in GCS
  wait_for_file = GCSObjectExistenceSensor(
      task_id="wait_for_gcs_file",
      bucket="dmg-media-raw",
      object="articles/{{ ds_nodash }}/feed.parquet",
      poke_interval=180,
      timeout=3600 * 2,
      mode="reschedule",
  )

  # 2. Batch load to Staging BigQuery Table (FREE)
  load_staging = GCSToBigQueryOperator(
      task_id="load_gcs_to_staging",
      bucket="dmg-media-raw",
      source_objects=["articles/{{ ds_nodash }}/feed.parquet"],
      destination_project_dataset_table="dmg-prod.staging.article_feed",
      source_format="PARQUET",
      write_disposition="WRITE_TRUNCATE",  # Idempotent
      autodetect=True,
  )

  # 3. Quality Validation Check
  def run_quality_check(**context):
    from google.cloud import bigquery

    client = bigquery.Client()
    query = "SELECT COUNT(*) as cnt FROM `dmg-prod.staging.article_feed`"
    rows = list(client.query(query).result())
    if rows[0]["cnt"] == 0:
      raise ValueError("Quality Check Failed: 0 rows found in staging table!")

  quality_check = PythonOperator(
      task_id="validate_staging_data",
      python_callable=run_quality_check,
  )

  # 4. Merge staging data into Partitioned Production Table
  merge_to_prod = BigQueryInsertJobOperator(
      task_id="execute_merge_to_production",
      configuration={
          "query": {
              "query": """
                    CALL `dmg-prod.analytics.sp_merge_articles`('{{ ds }}');
                """,
              "useLegacySql": False,
          }
      },
  )

  wait_for_file >> load_staging >> quality_check >> merge_to_prod
```

---

# PART 8 — AIRFLOW INTERVIEW ANSWERS (READ BEFORE INTERVIEW)

## Airflow Architecture & Component Roles
Airflow operates via 4 decoupled services: Webserver (visual UI), PostgreSQL Metadata Database (state storage), Scheduler (heartbeat checking cron intervals and DAG dependencies), and Executor/Workers (running the task processes). In Cloud Composer (GCP), this runs on a managed GKE cluster where Celery or Kubernetes executor dynamically runs tasks.

---

## Difference between `execution_date` (`logical_date`) and actual start time
Airflow schedules at the **end** of a period. A daily DAG with interval `2024-01-01` runs on `2024-01-02 00:00:00`. The `{{ ds }}` variable represents the start of that data window (`2024-01-01`), ensuring that queries extract data for the exact historical slice rather than runtime clock time.

---

## How Cross-DAG Dependencies Work
1. **TriggerDagRunOperator (Push):** Upstream DAG finishes and fires an API call to start the downstream DAG.
2. **ExternalTaskSensor (Pull):** Downstream DAG uses a sensor (with `mode='reschedule'`) to wait until the upstream task/DAG is marked success in the metadata database.
3. **Datasets (Data-aware):** Airflow 2.4+ native feature where downstream DAG schedules on `schedule=[Dataset("...")]`, triggering automatically whenever an upstream DAG produces that dataset.

---

## What is `depends_on_past` and when do you use it?
`depends_on_past=True` enforces that a task cannot run for date `T` unless the same task succeeded for date `T-1`. Use it for stateful historical pipelines (like cumulative financial balances) where missing yesterday's run will produce corrupt calculations today. For standard stateless daily ELT, keep it `False` so failures don't block subsequent dates.

---

## Why `mode='reschedule'` is mandatory for long-running sensors
In `poke` mode, the worker thread sits idle in a sleep loop while checking for file arrival, locking up a worker slot. In `reschedule` mode, the task checks once, and if unmet, releases the worker back to the pool and reschedules for later. This avoids worker starvation across the entire cluster.

---

## The Danger of Top-Level Code in DAG Files
The Airflow Scheduler parses every `.py` file in the DAG directory every 30 seconds. If you place API calls, heavy database queries, or file I/O outside of operator callables (top-level code), the scheduler runs that heavy logic every 30 seconds, causing severe CPU spikes, metadata DB lockups, and scheduler lag.

---

## How to Handle Data Sharing without Breaking XCom
XCom stores data in PostgreSQL with strict size constraints (<48KB). Passing dataframes or large JSONs causes metadata DB bloat and crashes. Best practice: Write intermediate datasets to GCS / BigQuery staging tables and pass only the object URI or table identifier through XCom.

---

## How to Prevent Overloading Downstream APIs (Pools)
Define a **Pool** in the Airflow UI with a concurrency limit (e.g. 5 slots). Attach `pool="api_pool"` to all tasks calling that API. Airflow limits simultaneous active tasks in that pool across the entire environment to 5, preventing rate-limit throttling (HTTP 429).

---

## How to Debug a Failed Airflow Task
1. Open the Airflow UI Grid View, click the failed task, and inspect **Logs**.
2. Examine the bottom of the stack trace for exception types (Python `KeyError`/`ValueError`, BigQuery schema mismatch, GCS 404, or K8s `OOMKilled`).
3. Check the **Rendered Template** tab to verify that `{{ ds }}` and connection parameters evaluated correctly.
4. Test and fix the failing SQL or Python function locally or in staging.
5. In the UI, click **Clear** on the failed TaskInstance to trigger a clean retry with upstream/downstream dependencies intact.

---

## Making DAGs Idempotent and Retry-Safe
A pipeline is idempotent if running it multiple times produces the exact same result as running it once. For Airflow:
- In BigQuery loads: Use `write_disposition='WRITE_TRUNCATE'` for staging or `DELETE + INSERT` on partition dates (`event_date = '{{ ds }}'`).
- In GCS outputs: Use deterministic file paths (`events/{{ ds }}/data.parquet`) rather than timestamped paths.
- In updates: Use `MERGE` statements with explicit unique keys.
