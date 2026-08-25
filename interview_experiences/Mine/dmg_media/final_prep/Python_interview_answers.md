# Python for Data Engineering — Pre-Interview Reference & Complete Answers
# Sharp, skimmable, complete. Read this before your interview.

---

# PART 1 — GCP AUTHENTICATION (ADC & SERVICE ACCOUNTS)

## 1. How Python Authenticates in GCP (Application Default Credentials - ADC)
1. **Local Development:** Run `gcloud auth application-default login`. Python SDKs (`google.cloud.storage`, `google.cloud.bigquery`) automatically find credentials in `~/.config/gcloud/`. No API keys or JSON files needed in code.
2. **Production (Cloud Composer / GKE / Cloud Run / VMs):** Use **Attached Service Accounts** or **Workload Identity**. GCP infrastructure injects OAuth access tokens automatically.
3. **External Systems (AWS / On-Prem / GitHub Actions):** Use Workload Identity Federation or set `export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"`.

## Golden Rule
Never hardcode API keys or service account `.json` files in Python code or Git repositories.

```python
from google.cloud import bigquery, storage

# Clean initialization — ADC handles authentication seamlessly
bq_client = bigquery.Client(project="dmg-prod")
gcs_client = storage.Client()
```

---

# PART 2 — GOOGLE CLOUD STORAGE (GCS) WITH PYTHON

## 1. In-Memory Parquet Upload (Zero Disk I/O)
```python
import io
from google.cloud import storage
import pandas as pd


def upload_df_to_gcs_parquet(
    df: pd.DataFrame, bucket_name: str, blob_name: str
):
  client = storage.Client()
  bucket = client.bucket(bucket_name)
  blob = bucket.blob(blob_name)

  # Use BytesIO buffer to avoid writing temporary files to local disk
  buffer = io.BytesIO()
  df.to_parquet(buffer, index=False, engine="pyarrow")
  buffer.seek(0)

  blob.upload_from_file(buffer, content_type="application/octet-stream")
  print(f"Uploaded: gs://{bucket_name}/{blob_name}")
```

## 2. Listing & Streaming Download from GCS
```python
def download_gcs_parquet_to_df(bucket_name: str, blob_name: str) -> pd.DataFrame:
  client = storage.Client()
  bucket = client.bucket(bucket_name)
  blob = bucket.blob(blob_name)

  data_bytes = blob.download_as_bytes()
  return pd.read_parquet(io.BytesIO(data_bytes))
```

---

# PART 3 — BIGQUERY PYTHON SDK

## 1. Parameterized Queries (SQL-Injection Safe)
```python
from google.cloud import bigquery

client = bigquery.Client()

query = """
    SELECT article_id, category, SUM(pageviews) as total_views
    FROM `dmg-prod.analytics.article_events`
    WHERE event_date = @run_date AND country = @country
    GROUP BY 1, 2
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("run_date", "DATE", "2024-01-15"),
        bigquery.ScalarQueryParameter("country", "STRING", "UK"),
    ],
    maximum_bytes_billed=10 * 1024**3,  # Guardrail: Fail if >10GB
)

query_job = client.query(query, job_config=job_config)
df = query_job.to_dataframe()  # Uses fast BigQuery Storage Read API
```

## 2. Batch Loading Parquet from GCS (FREE & IDEMPOTENT)
```python
def load_gcs_parquet_to_bq(
    gcs_uri: str, target_table: str, write_disposition="WRITE_TRUNCATE"
):
  client = bigquery.Client()

  job_config = bigquery.LoadJobConfig(
      source_format=bigquery.SourceFormat.PARQUET,
      write_disposition=write_disposition,
      autodetect=True,
  )

  load_job = client.load_table_from_uri(
      gcs_uri, target_table, job_config=job_config
  )
  load_job.result()  # Blocks until load completes
  print(f"Loaded {load_job.output_rows} rows into {target_table}")
```

---

# PART 4 — REST APIS: PAGINATION, RATE LIMITS & BACKOFF

## 1. Production API Client (Exponential Backoff + 429 Handling)
```python
import time
import requests


def fetch_api_with_backoff(url: str, headers: dict, max_retries: int = 5):
  for attempt in range(max_retries):
    try:
      response = requests.get(url, headers=headers, timeout=30)

      # 429: Rate Limited
      if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 2**attempt))
        print(f"Rate limited (429). Sleeping for {retry_after}s...")
        time.sleep(retry_after)
        continue

      # 5xx: Temporary Server Errors
      if response.status_code >= 500:
        sleep_time = 2**attempt
        print(
            f"Server Error ({response.status_code}). Retrying in"
            f" {sleep_time}s..."
        )
        time.sleep(sleep_time)
        continue

      response.raise_for_status()
      return response.json()

    except requests.exceptions.RequestException as e:
      if attempt == max_retries - 1:
        raise
      time.sleep(2**attempt)

  raise Exception(f"Max retries exceeded for {url}")
```

## 2. Cursor/Page-Token Pagination
```python
def fetch_all_paginated_records(base_url: str, api_key: str):
  headers = {"Authorization": f"Bearer {api_key}"}
  all_data = []
  next_token = None

  while True:
    params = {"limit": 100}
    if next_token:
      params["page_token"] = next_token

    data = fetch_api_with_backoff(base_url, headers)
    records = data.get("items", [])
    all_data.extend(records)

    next_token = data.get("next_page_token")
    if not next_token or len(records) == 0:
      break

  return all_data
```

---

# PART 5 — RELATIONAL DATABASES (POSTGRESQL / MYSQL)

## SQLAlchemy Connection Pooling & Chunked Extraction
```python
import pandas as pd
from sqlalchemy import create_engine

# Connection string
engine = create_engine(
    "postgresql+psycopg2://user:password@db-host:5432/analytics",
    pool_size=5,
    max_overflow=10,
    pool_recycle=1800,
)


def extract_table_chunked_to_gcs(
    query: str, bucket_name: str, prefix: str, chunk_size: int = 100_000
):
  # Chunking prevents Out-Of-Memory (OOM) errors on multi-gigabyte extractions
  for idx, df_chunk in enumerate(
      pd.read_sql(query, con=engine, chunksize=chunk_size)
  ):
    blob_path = f"{prefix}/part_{idx:04d}.parquet"
    upload_df_to_gcs_parquet(df_chunk, bucket_name, blob_path)
```

---

# PART 6 — PYTHON INTERVIEW ANSWERS (READ BEFORE INTERVIEW)

## How do Python clients authenticate to GCP services?
In local development, the SDK uses Application Default Credentials (ADC) populated via `gcloud auth application-default login`. In production (Cloud Composer, GKE, Cloud Functions), authentication is automatic through Workload Identity or attached Service Account IAM roles. Never hardcode credentials or commit JSON keys to source control.

---

## How do you handle API Rate Limiting (HTTP 429)?
When an API responds with status code 429, inspect the `Retry-After` response header to determine how long to pause. If absent, apply exponential backoff (e.g. `2 ** attempt` seconds sleep: 1s, 2s, 4s, 8s, 16s) up to a maximum retry threshold. If calling APIs in parallel (e.g. Airflow tasks), use an Airflow Pool to restrict concurrent worker tasks.

---

## How do you avoid Out-Of-Memory (OOM) crashes when extracting large datasets in Python?
1. Use **chunked processing** (`pd.read_sql(..., chunksize=100_000)` or `pd.read_csv(..., chunksize=100_000)`).
2. Avoid saving intermediate files to disk; use `io.BytesIO()` memory buffers to stream directly to GCS.
3. Use **PyArrow / Parquet** formats instead of JSON/CSV to minimize memory footprint and benefit from column pruning.
4. For database queries, use server-side cursors or streaming queries instead of loading the entire result set into Python memory at once.

---

## What is the difference between BigQuery QueryJob, LoadJob, and Streaming Insert in the Python SDK?
- **QueryJob:** Executes a SQL query (`client.query()`) and returns row results or writes to a destination table. Billed by bytes processed.
- **LoadJob:** Ingests external files (Parquet/CSV/Avro) from GCS into a BigQuery table (`client.load_table_from_uri()`). **Completely free** and handles TBs of data asynchronously.
- **Streaming Insert (`insert_rows_json`):** Pushes individual JSON records in near-real-time. Costs extra (~$0.01 per 200MB) and rows cannot be modified by DML immediately.

---

## Why should you use Parameterized Queries in BigQuery Python scripts?
Parameterized queries (`bigquery.ScalarQueryParameter`) pass parameters separately from the query text. This eliminates SQL injection risks and ensures data types (like `DATE` or `TIMESTAMP`) are formatted properly without messy string concatenation or quoting errors.
