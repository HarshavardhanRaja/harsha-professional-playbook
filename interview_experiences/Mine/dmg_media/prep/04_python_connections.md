# Python - API Connections, GCS, Data Sources - Interview Prep

---

## 1. Google Cloud Storage (GCS)

### Setup
```bash
pip install google-cloud-storage
```

### Basic Operations
```python
from google.cloud import storage

# Initialize client (uses ADC or service account)
client = storage.Client(project='my-project')

# OR with explicit service account
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file('key.json')
client = storage.Client(credentials=credentials, project='my-project')

# List buckets
for bucket in client.list_buckets():
    print(bucket.name)

# Get bucket
bucket = client.bucket('my-bucket')

# Upload file
blob = bucket.blob('data/2024/file.csv')
blob.upload_from_filename('/local/path/file.csv')

# Upload from string/bytes
blob.upload_from_string('col1,col2\n1,2\n3,4', content_type='text/csv')

# Download file
blob.download_to_filename('/local/path/output.csv')

# Download as string
content = blob.download_as_text()

# List blobs in a prefix
blobs = client.list_blobs('my-bucket', prefix='data/2024/')
for blob in blobs:
    print(blob.name)

# Delete blob
blob.delete()

# Check if blob exists
blob = bucket.blob('data/file.csv')
if blob.exists():
    print("File exists")

# Generate signed URL (temporary access)
import datetime
url = blob.generate_signed_url(
    version='v4',
    expiration=datetime.timedelta(hours=1),
    method='GET'
)
```

### Pattern: Read CSV from GCS into Pandas
```python
import pandas as pd
from google.cloud import storage
import io

def read_gcs_csv(bucket_name: str, blob_path: str) -> pd.DataFrame:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    content = blob.download_as_bytes()
    return pd.read_csv(io.BytesIO(content))
```

### Pattern: Write DataFrame to GCS as Parquet
```python
def write_df_to_gcs_parquet(df: pd.DataFrame, bucket_name: str, blob_path: str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    blob.upload_from_file(buffer, content_type='application/octet-stream')
```

---

## 2. BigQuery - Python Client

```python
from google.cloud import bigquery

client = bigquery.Client(project='my-project')

# Run a query
query = """
    SELECT user_id, COUNT(*) as events
    FROM `project.dataset.events`
    WHERE DATE(created_at) = @run_date
    GROUP BY user_id
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter('run_date', 'DATE', '2024-01-15')
    ]
)

query_job = client.query(query, job_config=job_config)
results = query_job.result()   # waits for completion

# Convert to DataFrame
df = query_job.to_dataframe()

# Load DataFrame to BigQuery
job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    schema=[
        bigquery.SchemaField("id", "INTEGER"),
        bigquery.SchemaField("name", "STRING"),
    ]
)
load_job = client.load_table_from_dataframe(df, 'project.dataset.table', job_config=job_config)
load_job.result()  # wait for completion

# Insert rows (streaming insert - small batches)
errors = client.insert_rows_json('project.dataset.table', [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
])
if errors:
    print(f"Errors: {errors}")
```

---

## 3. REST API Connections

### Basic REST API with requests
```python
import requests
import time
from typing import Optional, Dict, Any

def get_api_data(
    url: str,
    headers: Optional[Dict] = None,
    params: Optional[Dict] = None,
    retries: int = 3,
    backoff: float = 2.0
) -> Dict[str, Any]:
    """Fetch data from REST API with retry logic."""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()   # raises for 4xx/5xx
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # rate limited
                wait = backoff ** attempt
                print(f"Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            elif e.response.status_code >= 500:  # server error, retry
                time.sleep(backoff ** attempt)
            else:
                raise   # 4xx errors don't retry
        except requests.exceptions.ConnectionError:
            time.sleep(backoff ** attempt)
    raise Exception(f"Failed after {retries} attempts")
```

### Pagination pattern
```python
def fetch_all_pages(base_url: str, headers: dict) -> list:
    """Fetch all pages from a paginated API."""
    results = []
    url = base_url
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        results.extend(data['items'])
        url = data.get('next_page_url')   # None if last page
    return results
```

### OAuth2 Bearer Token
```python
import requests

def get_access_token(client_id: str, client_secret: str, token_url: str) -> str:
    response = requests.post(token_url, data={
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    response.raise_for_status()
    return response.json()['access_token']

token = get_access_token(CLIENT_ID, CLIENT_SECRET, TOKEN_URL)
headers = {'Authorization': f'Bearer {token}'}
```

---

## 4. Authentication - GCP

### Application Default Credentials (ADC)
```python
# Automatically picks up credentials in this order:
# 1. GOOGLE_APPLICATION_CREDENTIALS env var
# 2. gcloud auth application-default login
# 3. Attached service account (on GCE/Cloud Run/etc.)

from google.cloud import storage
client = storage.Client()  # no credentials needed if ADC is set up
```

### Service Account Key File
```python
from google.oauth2 import service_account
from google.cloud import bigquery

credentials = service_account.Credentials.from_service_account_file(
    'path/to/key.json',
    scopes=['https://www.googleapis.com/auth/bigquery']
)
client = bigquery.Client(credentials=credentials, project='my-project')
```

### Environment Variables (Best Practice)
```python
import os
from google.cloud import storage

# Set GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
# Then:
client = storage.Client()  # auto-picks up from env
```

---

## 5. Database Connections

### PostgreSQL / Cloud SQL
```python
import psycopg2
import sqlalchemy

# Direct psycopg2
conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    database=os.environ['DB_NAME'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    port=5432
)
cur = conn.cursor()
cur.execute("SELECT * FROM users WHERE created_at > %s", ('2024-01-01',))
rows = cur.fetchall()
conn.close()

# SQLAlchemy (better for Pandas integration)
engine = sqlalchemy.create_engine(
    f"postgresql+psycopg2://{user}:{password}@{host}/{database}"
)
df = pd.read_sql("SELECT * FROM users", engine)
df.to_sql('users_copy', engine, if_exists='replace', index=False)
```

### MySQL
```python
import mysql.connector
conn = mysql.connector.connect(
    host=host, user=user, password=password, database=db
)
```

---

## 6. Secret Management

### Google Secret Manager
```python
from google.cloud import secretmanager

def get_secret(project_id: str, secret_name: str, version: str = 'latest') -> str:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

db_password = get_secret('my-project', 'db-password')
```

---

## 7. Context Managers & Best Practices

```python
# Always use context managers for connections
with psycopg2.connect(...) as conn:
    with conn.cursor() as cur:
        cur.execute(query)

# Use environment variables, never hardcode credentials
import os
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")

# Use sessions in requests for connection pooling
session = requests.Session()
session.headers.update({'Authorization': f'Bearer {token}'})
for url in urls:
    response = session.get(url)
```

---

## 8. GCS → BigQuery Full Pattern

```python
from google.cloud import storage, bigquery
import pandas as pd
import io
from datetime import date

def gcs_to_bigquery_pipeline(
    run_date: date,
    gcs_bucket: str,
    gcs_prefix: str,
    bq_table: str
):
    # 1. Read from GCS
    storage_client = storage.Client()
    bq_client = bigquery.Client()

    blob_path = f"{gcs_prefix}/{run_date.strftime('%Y%m%d')}/data.csv"
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(blob_path)

    content = blob.download_as_bytes()
    df = pd.read_csv(io.BytesIO(content))

    # 2. Transform
    df['run_date'] = run_date
    df['loaded_at'] = pd.Timestamp.now()

    # 3. Load to BigQuery
    job_config = bigquery.LoadJobConfig(
        write_disposition='WRITE_APPEND',
        autodetect=True
    )
    load_job = bq_client.load_table_from_dataframe(df, bq_table, job_config=job_config)
    load_job.result()
    print(f"Loaded {len(df)} rows to {bq_table}")
```

---

## ❓ Likely Interview Questions

1. How do you connect to GCS from Python? Show me the code.
2. How do you authenticate to GCP from a Python script?
3. What is ADC and how does it work?
4. How do you handle API rate limiting in Python?
5. How do you read a CSV from GCS into a Pandas DataFrame?
6. How do you load data from Python to BigQuery?
7. How do you handle sensitive credentials (API keys, DB passwords)?
8. How would you implement pagination for an API that returns 100 records per page?
9. What's the difference between streaming insert and load job in BigQuery?
10. How do you connect to a Cloud SQL (Postgres) database from Python?
