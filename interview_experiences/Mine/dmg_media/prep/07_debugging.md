# Debugging & Troubleshooting - Interview Prep

---

## 1. Debugging BigQuery Queries

### Slow Query
```sql
-- Step 1: Check query plan
-- Click "Explain" in BQ UI → look for:
-- - Large "Input" rows at early stages
-- - Shuffle operations (data movement between workers)
-- - HIGH ratio of output vs input in joins (cartesian?)

-- Step 2: Check bytes processed
SELECT
  job_id,
  total_bytes_processed / POW(10,9) AS gb_processed,
  total_bytes_billed / POW(10,9) AS gb_billed,
  query
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE job_id = 'YOUR_JOB_ID';

-- Step 3: Check if partition pruning is working
-- Ensure WHERE clause uses partition column correctly
-- Bad: WHERE EXTRACT(YEAR FROM event_date) = 2024
-- Good: WHERE event_date BETWEEN '2024-01-01' AND '2024-12-31'
```

### Query Failing
- `Not found: Table` → check project/dataset/table name, check region
- `Quota exceeded` → reduce concurrency or request quota increase
- `Resources exceeded` → query too complex, break into parts or use intermediate tables
- `Invalid value` → data type mismatch, use CAST()
- `Syntax error` → use BQ SQL validator, check legacy vs standard SQL

---

## 2. Debugging Airflow DAGs

### DAG Not Showing in UI
```bash
# Check for import errors
airflow dags list-import-errors

# Try importing manually
python /path/to/dag.py

# Check scheduler logs
# Cloud Composer: Cloud Logging → Airflow Scheduler
```

### Task Stuck in Queued
- Check if worker is running: `airflow celery worker`
- Check executor: `airflow config get-value core executor`
- Check slot availability: `airflow pools list`
- Check for zombie tasks: `airflow tasks clear dag_id -s 2024-01-01 -e 2024-01-02`

### Task Failing
```python
# Add detailed logging in tasks
import logging
logger = logging.getLogger(__name__)

def my_task(**kwargs):
    logger.info(f"Starting task with execution_date: {kwargs['ds']}")
    try:
        result = do_something()
        logger.info(f"Result: {result}")
        return result
    except Exception as e:
        logger.error(f"Task failed: {str(e)}", exc_info=True)
        raise  # re-raise so Airflow marks as failed
```

### Test Task Without Running Full DAG
```bash
# Test task locally (doesn't store state in DB)
airflow tasks test my_dag_id my_task_id 2024-01-15

# Run task with specific date
airflow tasks run my_dag_id my_task_id 2024-01-15
```

---

## 3. Debugging Python Data Pipelines

### Common Issues

```python
# 1. Memory issues with large DataFrames
# Instead of:
df = pd.read_csv('huge_file.csv')  # loads all into memory

# Use chunking:
for chunk in pd.read_csv('huge_file.csv', chunksize=100_000):
    process(chunk)

# 2. Encoding issues
df = pd.read_csv('file.csv', encoding='utf-8-sig')  # handles BOM
# or
df = pd.read_csv('file.csv', encoding='latin-1')

# 3. Timezone issues
import pandas as pd
# Always store timestamps as UTC
df['created_at'] = pd.to_datetime(df['created_at'], utc=True)

# 4. Null handling
df['value'].fillna(0, inplace=True)
df = df.dropna(subset=['required_column'])

# 5. Type conversion errors
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')  # NaN for invalid
```

### Profiling Python Code
```python
import cProfile
import time

# Simple timing
start = time.time()
do_something()
print(f"Elapsed: {time.time() - start:.2f}s")

# cProfile
cProfile.run('my_function()', sort='cumulative')

# Memory profiling
from memory_profiler import memory_usage
mem = memory_usage(my_function)
print(f"Max memory: {max(mem):.1f} MB")
```

---

## 4. Debugging API Connections

```python
import requests
import logging

# Enable request/response logging
logging.basicConfig(level=logging.DEBUG)

# Check response details before parsing
response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print(f"Body preview: {response.text[:500]}")

# Handle different error types
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.ConnectionError:
    print("Connection failed")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error {e.response.status_code}: {e.response.text}")
except ValueError:  # json decode error
    print(f"Invalid JSON response: {response.text[:200]}")
```

---

## 5. GCP Monitoring & Debugging

### Cloud Logging
```python
from google.cloud import logging as gcp_logging

client = gcp_logging.Client()
logger = client.logger('my-pipeline')
logger.log_text('Pipeline started', severity='INFO')
logger.log_struct({'status': 'error', 'message': str(e)}, severity='ERROR')
```

### Key Log Filters (Cloud Console)
```
# Airflow task errors
resource.type="cloud_composer_environment"
textPayload=~"ERROR"
textPayload=~"Task failed"

# BigQuery job errors
resource.type="bigquery_resource"
severity="ERROR"

# Dataflow errors
resource.type="dataflow_step"
severity="ERROR"
```

---

## 6. Common Data Pipeline Failure Patterns

| Scenario | Symptom | Debugging Steps |
|----------|---------|-----------------|
| Missing data | Row count < expected | Check source, check date filter, check null values |
| Duplicate data | Row count > expected | Check if pipeline ran twice, check merge logic |
| Stale data | Data not updated | Check if DAG ran, check success status, check data source |
| Wrong data | Values incorrect | Trace back transform steps, check data types, check JOIN keys |
| Pipeline slow | High runtime | Profile each step, check partition/clustering, optimize queries |
| Out of memory | Worker OOM killed | Use chunking, increase machine size, stream instead of batch |

---

## 7. Idempotency in Pipelines

```python
# Always make pipelines idempotent (safe to run multiple times)

# BAD: append-only without dedup
def load_data(date):
    data = extract(date)
    append_to_table(data)  # creates duplicates if run twice!

# GOOD: delete-then-insert
def load_data(date):
    data = extract(date)
    delete_from_table(where_date=date)  # clean slate
    insert_into_table(data)             # safe to repeat

# GOOD: MERGE (upsert)
def load_data(date):
    data = extract(date)
    merge_into_table(data, key='id')    # updates or inserts
```

---

## ❓ Likely Interview Questions

1. How do you debug a BigQuery query that is running slowly?
2. A DAG is stuck and tasks are queued but not running — how do you debug?
3. How do you ensure a pipeline is idempotent?
4. A task is failing silently (no error visible) — how do you investigate?
5. How do you handle a pipeline that produces duplicate records?
6. How do you monitor a production data pipeline?
7. What do you check first when a pipeline hasn't produced data for the expected time?
8. How do you debug a Python script that's running out of memory?
9. A third-party API returns inconsistent data — how do you handle this?
10. How do you roll back a bad data load in BigQuery?
