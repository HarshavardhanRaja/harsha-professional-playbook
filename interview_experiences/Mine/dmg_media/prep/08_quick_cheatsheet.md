# ⚡ Quick Cheatsheet - DMG Media Round 2
## Review this the morning of the interview

---

## BigQuery One-Liners

```sql
-- Partition pruning (MUST use this form)
WHERE DATE(event_time) = '2024-01-15'

-- Deduplicate
SELECT * EXCEPT(rn) FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC) rn FROM t
) WHERE rn = 1

-- MERGE (upsert)
MERGE target T USING source S ON T.id = S.id
WHEN MATCHED THEN UPDATE SET T.val = S.val
WHEN NOT MATCHED THEN INSERT (id, val) VALUES (S.id, S.val)

-- Stored procedure
CREATE OR REPLACE PROCEDURE ds.proc(IN dt DATE) BEGIN ... END;
CALL ds.proc('2024-01-15');

-- Error handling in procedure
BEGIN ... EXCEPTION WHEN ERROR THEN INSERT INTO error_log VALUES(@@error.message, NOW()); END;

-- Check job cost
SELECT total_bytes_billed/1e9 AS gb_billed, query
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT ORDER BY total_bytes_billed DESC LIMIT 10;
```

---

## Airflow One-Liners

```python
# DAG skeleton
with DAG('dag_id', schedule_interval='0 6 * * *', catchup=False, default_args={...}) as dag:
    task1 = PythonOperator(task_id='t1', python_callable=fn)
    task2 = BashOperator(task_id='t2', bash_command='echo {{ ds }}')
    task1 >> task2

# XCom push/pull
ti.xcom_push(key='k', value=v)
v = ti.xcom_pull(task_ids='task_id', key='k')

# Test task
airflow tasks test dag_id task_id 2024-01-15

# Debug: check import errors
airflow dags list-import-errors
```

---

## Python GCS One-Liners

```python
from google.cloud import storage
client = storage.Client()
bucket = client.bucket('my-bucket')

# Upload
bucket.blob('path/file.csv').upload_from_filename('local.csv')

# Download to string
content = bucket.blob('path/file.csv').download_as_text()

# Read GCS CSV into Pandas
import io, pandas as pd
df = pd.read_csv(io.BytesIO(bucket.blob('file.csv').download_as_bytes()))

# Write DataFrame to GCS parquet
buf = io.BytesIO(); df.to_parquet(buf); buf.seek(0)
bucket.blob('file.parquet').upload_from_file(buf)
```

---

## Python BigQuery One-Liners

```python
from google.cloud import bigquery
client = bigquery.Client()

# Query → DataFrame
df = client.query("SELECT * FROM dataset.table WHERE id = @id",
    job_config=bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter('id', 'INT64', 123)]
    )).to_dataframe()

# Load DataFrame → BQ
client.load_table_from_dataframe(df, 'project.dataset.table',
    job_config=bigquery.LoadJobConfig(write_disposition='WRITE_APPEND')).result()
```

---

## Key Concepts to Nail

### BigQuery
- **Partitioning** = prune data at scan time (date columns)
- **Clustering** = sort within partition (high-cardinality cols)
- **Stored procedure** = `CREATE OR REPLACE PROCEDURE ... BEGIN ... END`
- **Cost control** = filter on partition col, avoid SELECT *

### Airflow
- **DAG** = collection of tasks + dependencies
- **XCom** = pass data between tasks (keep small!)
- **Sensor** = wait for condition (poke vs reschedule)
- **catchup=False** = don't run historical missed runs
- **`{{ ds }}`** = execution date string in templates

### Python Connections
- **ADC** = Application Default Credentials (auto-picks up service account)
- **GCS** = `google-cloud-storage` → `storage.Client()`
- **BQ** = `google-cloud-bigquery` → `bigquery.Client()`
- **Retry logic** = always add for APIs (with backoff)

### Data Warehousing
- **SCD Type 2** = add new row with `is_current`, `valid_from`, `valid_to`
- **Star schema** = flat dims, fewer JOINs (best for BQ)
- **ELT** = load raw first, transform in BQ (modern approach)
- **Idempotent** = safe to run multiple times (delete+insert or MERGE)

---

## Questions to Ask Them

1. What's the current data stack and what are the main pain points?
2. How large are the typical datasets you work with in BigQuery?
3. What does the Airflow DAG lifecycle look like — who owns scheduling vs development?
4. How do you handle data quality checks in the pipeline?
5. What's the team structure around data engineering?

---

## Mindset Tips

- **Talk through your thinking** — interviewers want to see how you debug/approach
- **Ask clarifying questions** before solving SQL/coding problems
- **Mention trade-offs** (e.g., "I'd use SCD Type 2 here, but it adds query complexity")
- **Bring real examples** from your experience when possible
- Be confident with BigQuery — it's their main tool
