# GCP Data Engineering Tools - Interview Prep

---

## 1. GCP Data Stack Overview

```
Data Sources → Ingestion → Storage → Processing → Serving → Analytics
    APIs         Pub/Sub     GCS      Dataflow    BigQuery   Looker
    DBs          Datastream  BigQuery  Dataproc    Bigtable   Data Studio
    Files        Transfer    Bigtable  Cloud Run   Spanner
               Service
```

---

## 2. Cloud Storage (GCS)

- Object storage (not a filesystem)
- Storage classes: **Standard, Nearline, Coldline, Archive** (access frequency → cost)
- **Buckets** are globally unique; objects within have paths (prefixes)
- No limit on object size (max 5TB per object)
- Lifecycle rules: auto-delete or transition to cheaper class
- **Versioning**: keep history of object changes

```bash
# Common gsutil commands
gsutil ls gs://my-bucket/data/
gsutil cp local_file.csv gs://my-bucket/data/
gsutil mv gs://my-bucket/old/ gs://my-bucket/new/
gsutil rm gs://my-bucket/data/file.csv
gsutil -m cp -r local_dir/ gs://my-bucket/data/   # parallel, recursive
```

---

## 3. Cloud Pub/Sub

- **Asynchronous messaging** (publisher → topic → subscription → subscriber)
- Push vs Pull subscriptions
- **At-least-once delivery** (handle deduplication)
- Message ordering with ordering keys
- Retention: up to 7 days

```python
from google.cloud import pubsub_v1

# Publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('my-project', 'my-topic')
data = b'{"event": "page_view", "user": "123"}'
future = publisher.publish(topic_path, data=data, attribute='value')
print(f"Published: {future.result()}")

# Subscriber (pull)
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('my-project', 'my-sub')

def callback(message):
    print(f"Received: {message.data}")
    message.ack()

streaming_pull = subscriber.subscribe(subscription_path, callback=callback)
```

**When to use Pub/Sub**: Real-time event streaming, decoupling microservices, triggering downstream pipelines.

---

## 4. Dataflow (Apache Beam)

- Fully managed **stream and batch processing**
- Write once in Apache Beam, run on Dataflow
- Auto-scales workers
- **Windowing** for streaming: tumbling, sliding, session windows

```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

options = PipelineOptions([
    '--runner=DataflowRunner',
    '--project=my-project',
    '--region=us-central1',
    '--temp_location=gs://my-bucket/temp/',
])

with beam.Pipeline(options=options) as p:
    (
        p
        | 'Read from GCS' >> beam.io.ReadFromText('gs://my-bucket/input/*.csv')
        | 'Parse CSV' >> beam.Map(parse_csv_line)
        | 'Filter' >> beam.Filter(lambda row: row['value'] > 0)
        | 'Write to BQ' >> beam.io.WriteToBigQuery(
            'project:dataset.table',
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
        )
    )
```

**When to use**: Large-scale ETL, real-time streaming pipelines, complex transformations.

---

## 5. Dataproc (Managed Hadoop/Spark)

- Managed **Apache Spark, Hadoop, Hive, Presto**
- Create clusters on-demand, run job, delete cluster (cost-efficient)
- Use **Dataproc Serverless** for Spark without managing clusters

```bash
# Create cluster
gcloud dataproc clusters create my-cluster \
  --region=us-central1 \
  --num-workers=2 \
  --master-machine-type=n1-standard-4

# Submit Spark job
gcloud dataproc jobs submit pyspark \
  --cluster=my-cluster \
  --region=us-central1 \
  my_spark_job.py -- --input=gs://bucket/data --output=gs://bucket/output
```

**When to use**: Existing Spark/Hadoop workloads, Spark MLlib, Hive queries on large datasets.

---

## 6. Cloud Composer (Managed Airflow)

- GKE-based managed Airflow
- DAGs stored in GCS bucket
- Auto-scales
- Integrated with Cloud Logging, Cloud Monitoring

```bash
# List environments
gcloud composer environments list --locations=us-central1

# Upload DAG
gcloud composer environments storage dags import \
  --environment=my-env --location=us-central1 --source=my_dag.py

# Get Airflow UI URL
gcloud composer environments describe my-env --location=us-central1 \
  --format='value(config.airflowUri)'
```

---

## 7. BigQuery Transfer Service

- Scheduled data transfers from external sources to BigQuery
- Sources: Google Ads, Google Analytics, YouTube, S3, Redshift
- No code needed — configure via UI or API

---

## 8. Cloud Functions / Cloud Run

### Cloud Functions (serverless, event-driven)
```python
# Triggered by Pub/Sub message
def process_pubsub(event, context):
    import base64, json
    data = base64.b64decode(event['data']).decode('utf-8')
    payload = json.loads(data)
    # process payload
```

### Cloud Run (containerized microservices)
- Deploy Docker containers
- Auto-scales to zero
- Use for longer-running jobs, HTTP APIs, or heavy dependencies

---

## 9. Data Catalog

- Metadata management for GCP data assets
- Auto-discovers BigQuery, GCS, Pub/Sub schemas
- Tag templates for business metadata
- Search across all data assets

---

## 10. IAM for Data Engineering

```bash
# Key roles
roles/bigquery.dataEditor       # Read/write BQ tables
roles/bigquery.jobUser          # Run BQ queries
roles/storage.objectAdmin       # Read/write GCS objects
roles/pubsub.publisher          # Publish to Pub/Sub
roles/pubsub.subscriber         # Subscribe to Pub/Sub
roles/dataflow.developer        # Run Dataflow jobs
roles/composer.worker           # Cloud Composer task runner
```

---

## 11. GCP Comparison Table

| Service | Use Case | Managed? | Language |
|---------|----------|----------|----------|
| BigQuery | Analytics / DW | ✅ Fully | SQL |
| Dataflow | Streaming/Batch ETL | ✅ Fully | Python/Java (Beam) |
| Dataproc | Spark/Hadoop | ✅ (cluster) | PySpark/Scala |
| Pub/Sub | Event streaming | ✅ Fully | Any |
| Composer | Workflow orchestration | ✅ Managed | Python (Airflow) |
| Cloud Functions | Event-driven compute | ✅ Serverless | Python/Node/Go |
| Cloud Run | Containerized services | ✅ Serverless | Any (Docker) |
| GCS | Object storage | ✅ Fully | Any |

---

## ❓ Likely Interview Questions

1. What GCP services have you used for data engineering?
2. When would you use Dataflow vs Dataproc?
3. What is Pub/Sub and how does it fit into a data pipeline?
4. How do you schedule and orchestrate pipelines on GCP?
5. What is Cloud Composer and how is it different from self-hosted Airflow?
6. How do you handle data ingestion from external APIs into GCP?
7. What GCS storage class would you use for archival data?
8. How do you monitor GCP data pipelines?
9. How do you control costs in BigQuery?
10. What is the role of IAM in securing data pipelines?
