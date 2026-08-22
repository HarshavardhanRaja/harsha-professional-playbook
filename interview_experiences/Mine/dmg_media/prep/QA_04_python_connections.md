# Python - Connections, APIs & GCP - Most Asked Interview Questions & Answers

---

## Q1. How do you connect to Google Cloud Storage (GCS) from Python?

**Answer:**

```python
from google.cloud import storage

# Method 1: Uses Application Default Credentials (ADC) automatically
# Works in Cloud Composer, Cloud Run, GCE, or if GOOGLE_APPLICATION_CREDENTIALS is set
client = storage.Client(project='my-project')

# Method 2: Explicit service account key file
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file('/path/to/key.json')
client = storage.Client(credentials=credentials, project='my-project')

# Core operations
bucket = client.bucket('my-bucket')

# Upload
bucket.blob('data/file.csv').upload_from_filename('/local/file.csv')
bucket.blob('data/file.txt').upload_from_string('hello world', content_type='text/plain')

# Download
bucket.blob('data/file.csv').download_to_filename('/local/output.csv')
content = bucket.blob('data/file.csv').download_as_text()

# List objects
for blob in client.list_blobs('my-bucket', prefix='data/2024/'):
    print(blob.name, blob.size)

# Check existence
if bucket.blob('data/file.csv').exists():
    print("Found!")
```

**Real-world pattern — read CSV from GCS into Pandas:**
```python
import io
import pandas as pd
from google.cloud import storage

def read_gcs_csv(bucket: str, path: str) -> pd.DataFrame:
    client = storage.Client()
    blob = client.bucket(bucket).blob(path)
    return pd.read_csv(io.BytesIO(blob.download_as_bytes()))
```

---

## Q2. What is Application Default Credentials (ADC)? How does authentication work in GCP?

**Answer:**

ADC is GCP's **automatic credential discovery mechanism**. When you call `storage.Client()` without explicit credentials, it looks for credentials in this order:

1. **`GOOGLE_APPLICATION_CREDENTIALS` env var** → path to a service account JSON key
2. **`gcloud auth application-default login`** → developer's personal credentials (local dev)
3. **Attached service account** → if running on GCE/Cloud Run/Cloud Functions/Composer, automatically uses the instance's service account

```bash
# Local development setup
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# OR (preferred for local dev)
gcloud auth application-default login
```

**Best practices:**
- ✅ On GCP services (Composer, Cloud Run) → use attached service account (no key file needed)
- ✅ Local dev → `gcloud auth application-default login`
- ✅ CI/CD → set `GOOGLE_APPLICATION_CREDENTIALS` to a key file (stored in secrets manager)
- ❌ Never hardcode credentials in code
- ❌ Never commit key files to git

---

## Q3. How do you connect to BigQuery from Python and run a query?

**Answer:**

```python
from google.cloud import bigquery

client = bigquery.Client(project='my-project')

# Simple query
query = "SELECT COUNT(*) as total FROM `project.dataset.events` WHERE DATE(ts) = '2024-01-15'"
result = client.query(query).result()
for row in result:
    print(row.total)

# Parameterized query (prevents SQL injection)
query = """
    SELECT user_id, email FROM `project.dataset.users`
    WHERE country = @country AND created_at > @since
"""
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter('country', 'STRING', 'UK'),
        bigquery.ScalarQueryParameter('since', 'TIMESTAMP', '2024-01-01T00:00:00'),
    ]
)
df = client.query(query, job_config=job_config).to_dataframe()

# Load DataFrame to BigQuery
job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    autodetect=True,
)
load_job = client.load_table_from_dataframe(df, 'project.dataset.target', job_config=job_config)
load_job.result()  # blocks until done
print(f"Loaded {load_job.output_rows} rows")
```

---

## Q4. How do you connect to an external REST API from Python? How do you handle errors and rate limits?

**Answer:**

```python
import requests
import time
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

def call_api(
    url: str,
    headers: Optional[Dict] = None,
    params: Optional[Dict] = None,
    max_retries: int = 3,
    backoff_factor: float = 2.0
) -> Dict[str, Any]:
    """
    Robust API caller with retry logic and exponential backoff.
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30           # important: always set timeout
            )

            if response.status_code == 429:
                # Rate limited - respect Retry-After header if present
                wait = float(response.headers.get('Retry-After', backoff_factor ** attempt))
                logger.warning(f"Rate limited. Waiting {wait}s before retry {attempt+1}")
                time.sleep(wait)
                continue

            response.raise_for_status()   # raises HTTPError for 4xx/5xx
            return response.json()

        except requests.exceptions.Timeout:
            logger.error(f"Timeout on attempt {attempt+1}")
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error on attempt {attempt+1}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code < 500:
                raise   # 4xx are client errors, don't retry
            logger.error(f"Server error {e.response.status_code} on attempt {attempt+1}")

        if attempt < max_retries - 1:
            sleep_time = backoff_factor ** attempt
            logger.info(f"Retrying in {sleep_time}s...")
            time.sleep(sleep_time)

    raise Exception(f"API call failed after {max_retries} attempts: {url}")
```

---

## Q5. How do you handle pagination when fetching data from an API?

**Answer:**

Most APIs paginate large result sets. Common patterns:

**Pattern 1: Offset/Page number**
```python
def fetch_all_users(base_url: str, token: str) -> list:
    headers = {'Authorization': f'Bearer {token}'}
    all_users = []
    page = 1

    while True:
        response = requests.get(
            f"{base_url}/users",
            headers=headers,
            params={'page': page, 'per_page': 100}
        )
        response.raise_for_status()
        data = response.json()

        users = data.get('data', [])
        all_users.extend(users)

        # Check if we've reached the last page
        if page >= data['meta']['total_pages']:
            break
        page += 1

    return all_users
```

**Pattern 2: Cursor/next_page_token**
```python
def fetch_all_events(base_url: str, token: str) -> list:
    headers = {'Authorization': f'Bearer {token}'}
    all_events = []
    next_cursor = None

    while True:
        params = {'limit': 500}
        if next_cursor:
            params['cursor'] = next_cursor

        response = requests.get(f"{base_url}/events", headers=headers, params=params)
        data = response.json()
        all_events.extend(data['events'])

        next_cursor = data.get('next_cursor')  # None when last page
        if not next_cursor:
            break

    return all_events
```

**Pattern 3: Link Header (RFC 5988)**
```python
response = requests.get(url, headers=headers)
while True:
    data = response.json()
    results.extend(data)
    # GitHub-style: Link header contains next URL
    if 'next' not in response.links:
        break
    response = requests.get(response.links['next']['url'], headers=headers)
```

---

## Q6. How do you securely store and access secrets (API keys, DB passwords) in Python?

**Answer:**

**Never do this:**
```python
# ❌ NEVER hardcode secrets
API_KEY = "sk_live_abcdef123456"
DB_PASSWORD = "mypassword123"
```

**Do this instead:**

**Option 1: Environment variables** (simplest)
```python
import os
API_KEY = os.environ['THIRD_PARTY_API_KEY']
if not API_KEY:
    raise ValueError("THIRD_PARTY_API_KEY environment variable not set")
```

**Option 2: Google Secret Manager** (recommended for GCP)
```python
from google.cloud import secretmanager

def get_secret(secret_id: str, project_id: str = 'my-project') -> str:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

api_key = get_secret('third-party-api-key')
```

**Option 3: Airflow Connections/Variables** (for pipeline secrets)
```python
from airflow.hooks.base import BaseHook
conn = BaseHook.get_connection('my_api_conn')
api_key = conn.password
api_url = conn.host
```

**Option 4: python-dotenv** (local dev only)
```bash
# .env file (never commit this!)
API_KEY=sk_live_abc123
```
```python
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ['API_KEY']
```

---

## Q7. How do you connect to a PostgreSQL database from Python?

**Answer:**

```python
import os
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# Method 1: psycopg2 (raw)
conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    port=5432,
    database=os.environ['DB_NAME'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
)
try:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM users WHERE created_at > %s",
            ('2024-01-01',)   # always use parameterized queries!
        )
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=columns)
    conn.commit()
finally:
    conn.close()

# Method 2: SQLAlchemy (better for Pandas)
engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
)
df = pd.read_sql("SELECT * FROM users WHERE status = %(s)s", engine, params={'s': 'active'})
df.to_sql('users_backup', engine, if_exists='replace', index=False, chunksize=1000)
```

**Cloud SQL connection:** Same as above, but connect via:
1. Cloud SQL Proxy (preferred, secure)
2. Public IP with SSL
3. Private IP (VPC peering)

---

## Q8. How do you write data from GCS to BigQuery in Python? What are the different ways?

**Answer:**

**Method 1: Load from GCS URI (best for large files)**
```python
from google.cloud import bigquery

client = bigquery.Client()
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,               # skip header
    autodetect=True,                   # auto-detect schema
    write_disposition='WRITE_TRUNCATE',  # overwrite
)
load_job = client.load_table_from_uri(
    'gs://my-bucket/data/2024-01-15/*.csv',
    'project.dataset.table',
    job_config=job_config
)
load_job.result()  # wait for completion
print(f"Loaded {client.get_table('project.dataset.table').num_rows} rows")
```

**Method 2: Load from DataFrame (for transformed data)**
```python
from google.cloud import storage, bigquery
import pandas as pd
import io

# Read from GCS
storage_client = storage.Client()
content = storage_client.bucket('my-bucket').blob('data/file.csv').download_as_bytes()
df = pd.read_csv(io.BytesIO(content))

# Transform
df['loaded_at'] = pd.Timestamp.now()
df['source'] = 'api'

# Write to BQ
bq_client = bigquery.Client()
job = bq_client.load_table_from_dataframe(
    df,
    'project.dataset.table',
    job_config=bigquery.LoadJobConfig(write_disposition='WRITE_APPEND')
)
job.result()
```

**Method 3: Streaming insert (real-time, small batches)**
```python
errors = client.insert_rows_json('project.dataset.table', [
    {"id": 1, "name": "Alice", "ts": "2024-01-15T10:00:00"},
    {"id": 2, "name": "Bob", "ts": "2024-01-15T10:01:00"},
])
if errors:
    raise RuntimeError(f"Streaming insert errors: {errors}")
```

| Method | Latency | Cost | Best for |
|--------|---------|------|---------|
| GCS URI load | Minutes | Low | Large batches |
| DataFrame load | Minutes | Low | Transformed data |
| Streaming insert | Seconds | Higher | Real-time events |

---

## Q9. How would you design a Python script to ingest data from a REST API into BigQuery daily?

**Answer:**

```python
import os
import requests
import pandas as pd
from datetime import date
from google.cloud import bigquery, secretmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_api_token() -> str:
    """Get API token from Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{os.environ['GCP_PROJECT']}/secrets/api-token/versions/latest"
    return client.access_secret_version(request={"name": name}).payload.data.decode()

def fetch_data(run_date: date, token: str) -> list[dict]:
    """Fetch all pages from the API for the given date."""
    headers = {'Authorization': f'Bearer {token}'}
    all_records = []
    page = 1

    while True:
        response = requests.get(
            'https://api.example.com/events',
            headers=headers,
            params={'date': run_date.isoformat(), 'page': page, 'per_page': 500},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        records = data.get('events', [])
        all_records.extend(records)
        logger.info(f"Fetched page {page}, {len(records)} records")

        if not data.get('has_more'):
            break
        page += 1

    return all_records

def load_to_bigquery(records: list[dict], run_date: date):
    """Load records into BigQuery."""
    if not records:
        raise ValueError(f"No records for {run_date}")

    df = pd.DataFrame(records)
    df['run_date'] = run_date
    df['loaded_at'] = pd.Timestamp.now(tz='UTC')

    client = bigquery.Client()

    # Delete existing data for this date (idempotent)
    client.query(
        f"DELETE FROM `project.dataset.api_events` WHERE run_date = '{run_date}'"
    ).result()

    # Load fresh data
    job = client.load_table_from_dataframe(
        df,
        'project.dataset.api_events',
        job_config=bigquery.LoadJobConfig(write_disposition='WRITE_APPEND')
    )
    job.result()
    logger.info(f"Loaded {len(df)} rows for {run_date}")

def main(run_date: date = None):
    run_date = run_date or date.today()
    logger.info(f"Starting ingestion for {run_date}")

    token = get_api_token()
    records = fetch_data(run_date, token)
    load_to_bigquery(records, run_date)

    logger.info("Ingestion complete")

if __name__ == '__main__':
    import sys
    d = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else None
    main(d)
```

---

## Q10. What is the difference between streaming insert and batch load in BigQuery? When would you use each?

**Answer:**

### Batch Load (recommended for most cases)
- Data is loaded via a **load job** — asynchronous, runs in the background
- Data becomes available when the job completes (minutes)
- **Free** (no charge for loading)
- Can load from GCS, local files, DataFrames
- Supports large files (TB scale)
- Immediately available for DML (UPDATE/DELETE/MERGE)

### Streaming Insert
- Data is inserted **immediately** using the BigQuery Storage Write API
- Available for queries within seconds
- **Costs extra** (~$0.01 per 200MB)
- Max 10MB per request, 500 rows per request
- Has a brief **deduplication window** but NOT fully dedup safe
- Inserted data is not immediately DML-able for a few minutes

```python
# Streaming insert
errors = client.insert_rows_json('project.dataset.table', rows)

# Batch load (preferred)
load_job = client.load_table_from_uri('gs://bucket/file.csv', table_ref, job_config=...)
load_job.result()
```

**When to use streaming:** Real-time dashboards, IoT telemetry, event tracking where you need fresh data instantly.
**When to use batch:** ETL pipelines, daily/hourly loads, large file ingestion — vastly cheaper and simpler.

---

## Q11. How do you handle errors when loading data to BigQuery?

**Answer:**

```python
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError
import logging

def safe_load_to_bq(df, table_ref: str):
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(write_disposition='WRITE_APPEND')

    try:
        load_job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        load_job.result()  # raises on failure
        logger.info(f"Loaded {load_job.output_rows} rows to {table_ref}")

    except GoogleAPIError as e:
        # GCP API-level errors (auth, quota, not found)
        logger.error(f"BQ API error: {e.message}")
        raise

    except Exception as e:
        # Unexpected errors
        logger.error(f"Unexpected error loading to BQ: {str(e)}", exc_info=True)
        raise

    # Check for partial failures (streaming insert)
    finally:
        if hasattr(load_job, 'errors') and load_job.errors:
            logger.error(f"Load job errors: {load_job.errors}")
```

**Common BQ errors and solutions:**

| Error | Cause | Fix |
|-------|-------|-----|
| `403 Access Denied` | Missing IAM permission | Add `bigquery.dataEditor` role |
| `404 Not found: Table` | Table/dataset doesn't exist | Create it first, check project/dataset name |
| `Schema mismatch` | DataFrame has different columns | Align schema, use `autodetect=True` |
| `Quota exceeded` | Too many concurrent jobs | Add retry with backoff |
| `invalid: too large` | Row > 100MB | Reduce row size |
