# 🎯 L'Oréal Senior Data Engineer — Interview Prep
> **Role:** Senior Data Engineer · Hyderabad · 37 LPA · Michael Page
> **Key Differentiator:** This is an AI-Augmented Engineering role — they explicitly screen for AI tooling fluency

---

## 🔑 What Makes This Interview Unique

L'Oréal explicitly lists AI tooling (Copilot, Cursor, Claude Code) as a **Primary Skill** — not a bonus. This means:

1. **They will ask HOW you use AI in daily engineering**, not just if you know the stack
2. Expect questions framed around: *"How did you use AI to solve X problem?"*
3. Senior = balancing code perfection vs business deadlines (explicitly called out)
4. Reverse ETL + Data Activation is a specialty area — be ready to go deep

---

## 📋 Interview Round Map (Likely)

| Round | Focus | Duration |
|---|---|---|
| R1 (HR/Screening) | Background, AI tooling usage, culture fit | 30-45 min |
| R2 (Technical - DE) | SQL, Python, Airflow, GCP stack | 60-90 min |
| R3 (Tech Lead / Architecture) | System Design, Reverse ETL, pipeline architecture | 60 min |
| R4 (Hiring Manager) | Behavioral, leadership, mentorship | 45 min |

---

## 🤖 Section 1: AI-Augmented Engineering (UNIQUE TO THIS ROLE)

This is the highest-signal differentiator. Most candidates won't have structured answers here.

### Q1: How do you use AI coding assistants in your day-to-day DE work?

**Your Answer (STAR):**
> At Sequoia, I actively used GitHub Copilot and Claude to accelerate complex SQL and Python pipeline development. Specifically: (1) for generating boilerplate Airflow DAG skeletons, I'd describe the orchestration logic and let Copilot scaffold the operators and dependencies, then review and harden; (2) for SQL optimization, I'd paste slow query execution plans into Claude and ask it to identify scan vs join inefficiencies; (3) for test generation — writing data quality checks and schema drift detectors. The key discipline is treating AI output as a first draft that needs expert review, not a final answer.

### Q2: Give an example where AI saved you hours of engineering work.

**Prepare this story:**
> Building a complex ELT pipeline with 15+ transformations and multiple deduplication windows. Used Claude to generate the window function logic for SCD Type 2 merges across 10M+ rows in BigQuery, then reviewed the generated SQL against my knowledge of BigQuery slot economics to optimize partition pruning. What would have taken a day took 2 hours.

### Q3: How do you validate AI-generated code before it goes to production?

**Framework answer:**
1. **Correctness**: Run against a known-good subset of data with expected outputs
2. **Edge cases**: Ask AI itself "what edge cases might this miss?" then verify
3. **Performance**: Check query execution plan / Spark DAG — AI often misses partition skew
4. **Code review**: Treat it like any PR — peer review against team standards

### Q4: What are the limits of AI tools in Data Engineering?

**Show depth:**
- AI doesn't know your specific data shape, volume, or business semantics
- Query plans and cost estimation need domain expertise — AI can suggest, not decide
- Airflow DAG dependencies and failure handling need human judgment for business SLAs
- Schema drift detection rules need business context AI can't infer

---

## 🔄 Section 2: Airflow DAGs — Deep Dive

### Q: How do you design an idempotent Airflow DAG?

```python
# Core principles:
# 1. Use execution_date for partition boundaries, never "today"
# 2. UPSERT instead of INSERT — use MERGE in BigQuery / DELETE+INSERT
# 3. External sensors with mode='reschedule' to free up workers

from airflow import DAG
from airflow.operators.python import PythonOperator

def extract_and_load(execution_date, **kwargs):
    # execution_date guarantees idempotency
    partition = execution_date.strftime('%Y-%m-%d')
    # DELETE + INSERT pattern
    bq_client.query(f"DELETE FROM table WHERE partition_date = '{partition}'")
    bq_client.load_table_from_dataframe(df, f"table${partition.replace('-','')}")

dag = DAG(
    'idempotent_pipeline',
    schedule_interval='@daily',
    catchup=True,   # allows backfill — idempotency makes this safe
    max_active_runs=3,
)
```

### Q: How do you ensure high availability / observability of Airflow schedules?

- **Observability**: `on_failure_callback` → PagerDuty/Slack + SLA miss alerts
- **HA**: Celery executor with Redis broker + multiple workers (not LocalExecutor)
- **Dead letter**: Failed tasks write to error log table with context for replay
- **Monitoring**: Airflow metrics → Prometheus → Grafana (task duration P99, queue depth)

### Q: What's the difference between a Sensor and a trigger rule?

```python
# Sensor: waits for an external condition (S3 file, BQ partition, HTTP endpoint)
from airflow.sensors.external_task import ExternalTaskSensor

wait_for_upstream = ExternalTaskSensor(
    task_id='wait_for_crm_load',
    external_dag_id='crm_pipeline',
    external_task_id='load_to_bq',
    mode='reschedule',  # NOT 'poke' — frees worker slot while waiting
    timeout=3600,
)

# Trigger rules: control when a task runs based on upstream task states
# all_done  → run even if upstream failed (great for cleanup/alerting tasks)
# one_failed → alerting task that fires when any upstream fails
# none_failed → default, runs only if all upstream succeeded
```

---

## ☁️ Section 3: GCP Stack — BigQuery, Dataform, Dataflow

### Q: BigQuery cost optimization strategies?

| Strategy | Impact | How |
|---|---|---|
| Partition pruning | High | Always filter on partition column in WHERE |
| Clustering | Medium | Cluster on columns used in WHERE/JOIN after partition |
| Materialized views | High | Pre-compute expensive aggregations |
| Column selection | High | Never SELECT * in columnar stores |
| Partition expiry | Medium | Set expiry on raw/staging tables |
| Flat-rate slots | High | Commit to flat-rate when usage is predictable |

**BigQuery Query Optimization SQL:**
```sql
-- BAD: Full table scan
SELECT * FROM `project.dataset.events`
WHERE DATE(event_timestamp) = '2024-01-01';

-- GOOD: Partition pruning + column selection
SELECT event_id, customer_id, event_type
FROM `project.dataset.events`
WHERE event_timestamp BETWEEN '2024-01-01' AND '2024-01-02'
  AND event_type = 'purchase';  -- clustering column reduces bytes scanned
```

### Q: Dataform vs dbt — which and when?

| | Dataform | dbt |
|---|---|---|
| Where it runs | Inside BigQuery natively | External, connects to BQ |
| Syntax | SQLX (JS + SQL hybrid) | Jinja + SQL |
| Orchestration | Workflow schedules (GCP native) | dbt Cloud / Airflow |
| Best for | BQ-only shops, GCP-native teams | Multi-warehouse, open-source ecosystem |
| Auth | IAM-based, no extra infra | Service account + secrets management |

### Q: Apache Beam / Dataflow — when do you use it over Spark?

- **Beam/Dataflow:** Unified batch+streaming; GCP-native auto-scaling; best for Pub/Sub → BigQuery event streams
- **Spark/Dataproc:** Complex ML feature engineering, heavy PySpark libraries, existing Spark codebases

```python
# Beam pipeline: Pub/Sub → BigQuery streaming
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

options = PipelineOptions(runner='DataflowRunner', project='my-project', streaming=True)

with beam.Pipeline(options=options) as p:
    (p
     | 'ReadPubSub' >> beam.io.ReadFromPubSub(topic='projects/proj/topics/events')
     | 'ParseJSON' >> beam.Map(lambda msg: json.loads(msg))
     | 'FilterValid' >> beam.Filter(lambda r: r.get('customer_id'))
     | 'WriteBQ' >> beam.io.WriteToBigQuery(
         table='project:dataset.events',
         schema=SCHEMA,
         write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
     )
    )
```

---

## 🔁 Section 4: Reverse ETL — Data Activation (KEY DIFFERENTIATOR)

Most candidates won't go deep here. L'Oréal explicitly mentions Salesforce, Tealium, Braze, Google Ads.

### Q: What is Reverse ETL and how do you design a reliable pipeline?

**Definition:** Moving processed/enriched data FROM the warehouse INTO operational tools (CRM, marketing platforms, ad networks).

**Architecture:**
```
BigQuery Gold Layer
    ↓
Reverse ETL (Python + Airflow)
    ↓
Salesforce | Braze | Google Ads | Tealium
```

**Key Design Concerns:**
1. **Idempotency**: `sync_status` table tracks which records were synced; re-runs are safe
2. **API rate limits**: Salesforce = 150k API calls/day; use batching + exponential backoff
3. **Schema drift**: Versioned sync configs; alerts if BQ schema changes affect downstream
4. **Audit trail**: Every sync writes to `sync_log` with status, timestamp, record counts
5. **Partial sync tracking**: Failed records logged individually, not full re-sync

**Audit table design:**
```sql
CREATE TABLE sync_log (
    sync_id       STRING,
    target_system STRING,   -- 'salesforce', 'braze', 'google_ads', 'tealium'
    sync_started_at   TIMESTAMP,
    sync_completed_at TIMESTAMP,
    records_attempted INT64,
    records_succeeded INT64,
    records_failed    INT64,
    status            STRING,   -- 'SUCCESS', 'PARTIAL', 'FAILED'
    error_details     JSON
)
PARTITION BY DATE(sync_started_at);
```

### Q: How do you handle Salesforce API limits?

```python
class SalesforceSync:
    BATCH_SIZE = 200  # Salesforce composite API limit

    def sync_customers(self, records: list[dict]):
        batches = [records[i:i+self.BATCH_SIZE]
                   for i in range(0, len(records), self.BATCH_SIZE)]
        for batch in batches:
            try:
                self.sf.bulk.Contact.upsert(batch, 'External_ID__c')
            except SalesforceMalformedRequest as e:
                self.write_failed_batch(batch, str(e))
            time.sleep(0.1)  # respect rate limits
```

---

## 🐍 Section 5: Python Excellence

### Q: Custom Airflow Operators — how and why?

```python
from airflow.models import BaseOperator

class BigQueryToSalesforceOperator(BaseOperator):
    """
    Custom operator: syncs BQ query results to Salesforce.
    Encapsulates the pattern to keep DAGs DRY across the team.
    """
    def __init__(self, bq_query: str, sf_object: str, upsert_key: str, **kwargs):
        super().__init__(**kwargs)
        self.bq_query = bq_query
        self.sf_object = sf_object
        self.upsert_key = upsert_key

    def execute(self, context):
        bq_hook = BigQueryHook()
        records = bq_hook.get_pandas_df(self.bq_query).to_dict('records')

        sf_hook = SalesforceHook()
        result = sf_hook.bulk_upsert(self.sf_object, records, self.upsert_key)

        self.log.info(f"Synced {len(records)} records to {self.sf_object}")
        return result

# Usage in DAG — completely DRY, any DE can understand it
sync_to_crm = BigQueryToSalesforceOperator(
    task_id='sync_customers_to_salesforce',
    bq_query='SELECT * FROM gold.customer_segments WHERE segment_date = {{ ds }}',
    sf_object='Contact',
    upsert_key='External_ID__c',
)
```

### Q: Python generators for large dataset processing?

```python
def stream_bq_results(query: str, chunk_size: int = 10_000):
    """
    Generator — memory stays constant regardless of dataset size.
    Critical for Reverse ETL where we process millions of records.
    """
    client = bigquery.Client()
    job = client.query(query)

    chunk = []
    for row in job.result():
        chunk.append(dict(row))
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []

    if chunk:   # yield remaining rows
        yield chunk

# Usage — processes 10M rows with fixed memory footprint
for batch in stream_bq_results("SELECT * FROM gold.customer_segments"):
    sync_to_braze(batch)
```

---

## 🔍 Section 6: SQL — L'Oréal Specific Patterns

### Q: Latest valid record per customer (multi-tier tie-breaking)

> This is the Dubai Data R1 pattern — L'Oréal will likely have a similar question given the customer data focus.

```sql
-- Latest valid record: event_time → updated_at → ingestion_time as tie-breakers
WITH ranked AS (
    SELECT
        customer_id,
        event_id,
        updated_at,
        ingestion_time,
        event_time,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY
                event_time      DESC,
                updated_at      DESC,
                ingestion_time  DESC
        ) AS rn
    FROM customer_events
)
SELECT customer_id, event_id, updated_at, ingestion_time, event_time
FROM ranked
WHERE rn = 1;
```

### Q: SCD Type 2 in BigQuery using MERGE

```sql
-- Step 1: Expire changed records
MERGE INTO dim_customers AS target
USING staging_customers AS source
    ON target.customer_id = source.customer_id AND target.is_current = TRUE
WHEN MATCHED AND (target.email != source.email OR target.phone != source.phone)
THEN UPDATE SET is_current = FALSE, valid_to = CURRENT_TIMESTAMP();

-- Step 2: Insert new current versions
INSERT INTO dim_customers (customer_id, email, phone, valid_from, valid_to, is_current)
SELECT source.customer_id, source.email, source.phone,
       CURRENT_TIMESTAMP(), NULL, TRUE
FROM staging_customers source
JOIN dim_customers target
    ON source.customer_id = target.customer_id
    AND target.is_current = FALSE
    AND target.valid_to = CURRENT_TIMESTAMP();
```

### Q: Window functions they'll likely test

```sql
SELECT
    customer_id,
    sale_date,
    amount,
    SUM(amount)     OVER (PARTITION BY customer_id ORDER BY sale_date) AS running_total,
    LAG(amount)     OVER (PARTITION BY customer_id ORDER BY sale_date) AS prev_sale,
    LEAD(amount)    OVER (PARTITION BY customer_id ORDER BY sale_date) AS next_sale,
    PERCENT_RANK()  OVER (PARTITION BY region       ORDER BY amount DESC) AS pct_rank,
    NTILE(4)        OVER (ORDER BY amount DESC) AS quartile
FROM sales;
```

---

## 🏗️ Section 7: System Design

### Q: Design L'Oréal's Customer 360 Data Activation Pipeline

```
Web/App Events ──→  Pub/Sub ──→  Dataflow (Beam)  ──→  BQ Raw Layer
Salesforce CRM ──→  Cloud Storage (batch) ──→  Airflow  ──→  BQ Raw Layer
Google Ads     ──→  BQ Data Transfer Service  ──→  BQ Raw Layer
                                │
                    Airflow DAG Orchestration
                                │
                    Dataform: Raw → Silver
                    (dedup, validate, normalize)
                                │
                    Dataform: Silver → Gold
                    (Customer 360, Segments, Features)
                                │
                    Reverse ETL (Python + Airflow)
                    ├── Gold → Salesforce (contact enrichment)
                    ├── Gold → Braze (audience segments)
                    ├── Gold → Google Ads (customer match lists)
                    └── Gold → Tealium (tag management / CDP)
```

**Design decisions to articulate:**
- **Why Dataform over dbt?** GCP-native, no extra infra, IAM-based auth, SQLX flexibility
- **Why Airflow for orchestration?** Proven DAG dependencies, external sensors, audit-grade logging
- **Why batch Reverse ETL?** API rate limits on Salesforce/Braze constrain real-time; batch is reliable and auditable
- **Idempotency everywhere:** Partition-based pipelines, UPSERT patterns, sync_log audit trail

---

## 🎭 Section 8: Behavioral Stories (STAR Format)

### "Tell me about a complex pipeline you built"

> **S:** At Sequoia, we needed to ingest and activate customer behavioral data across 5 downstream marketing systems for 10M+ customers.
> **T:** I was responsible for designing and delivering the full ELT → Reverse ETL pipeline within 6 weeks.
> **A:** Built a Dataflow pipeline for streaming ingest from app events, Airflow-orchestrated BigQuery transformations for Customer 360 views, and a custom Python Reverse ETL library with per-system rate limiting and audit logging. Used GitHub Copilot to accelerate Airflow DAG scaffolding and Claude for complex MERGE SQL patterns.
> **R:** Delivered on time, 99.7% sync reliability, pipeline ran 40% cheaper than estimate due to BigQuery partition optimization.

### "Tell me about mentoring junior engineers"

> **S:** A junior DE joined with strong Python but no Airflow or BigQuery experience.
> **T:** They needed to be productive within 4 weeks for an active project deadline.
> **A:** Created a structured ramp plan: Week 1 — read existing DAGs + architecture walkthrough. Week 2 — small tasks with my code review. Week 3 — own a feature with daily check-in. Week 4 — solo delivery. I also used Claude Code to generate annotated examples for concepts they struggled with.
> **R:** They delivered their first production DAG independently in week 4. Still maintained in production today.

### "Tell me about balancing code quality with deadlines"

> **S:** A marketing campaign deadline required data activation to Braze 48 hours before launch.
> **T:** Pipeline had tech debt — no proper error handling, no idempotency.
> **A:** Made a pragmatic call: ship with idempotency (non-negotiable for data correctness) and basic alerting, defer the full audit log table and schema drift detection to the following sprint. Documented the tech debt explicitly in the PR.
> **R:** Campaign launched on time, zero data issues. Cleanup shipped the following sprint as planned.

---

## 🧠 Questions to Ask the Interviewer

1. *"How does the team currently use AI tools — is there a standardization strategy the Tech Lead has defined, or is it team-member driven?"*
2. *"Which downstream activation systems (Salesforce, Braze, etc.) are live vs planned? What's the current Reverse ETL maturity?"*
3. *"What does the CI/CD pipeline for data — DAGs, Dataform models — look like today?"*
4. *"How is the squad structured — dedicated Tech Lead, data analysts, and engineers?"*
5. *"What's the biggest pipeline reliability challenge the team is facing right now?"*

---

## ✅ Pre-Interview Checklist

- [ ] Refresh Airflow: DAG, Sensor (reschedule vs poke), Operator, Hook, XCom, Executor types
- [ ] Revise BigQuery MERGE, partitioning, clustering syntax
- [ ] Prepare 2-3 concrete AI tooling stories (Copilot/Claude in real work)
- [ ] Review Apache Beam: PCollection, PTransform, windowing, watermarks, Dataflow runner
- [ ] Practice the Customer 360 system design out loud — draw and explain
- [ ] Prep Reverse ETL architecture: rate limiting, audit trail, idempotency
- [ ] Know your Sequoia project details — most behavioral answers draw from there
- [ ] Know L'Oréal Beauty Tech context: 2000+ tech professionals, 150 countries, €42B sales

---

## 📅 Quick Reference Card

| Topic | Key Terms to Drop |
|---|---|
| Airflow | Idempotent, catchup, execution_date, reschedule mode sensors, custom operators, XCom |
| BigQuery | Partition pruning, clustering, materialized views, slot utilization, MERGE, INFORMATION_SCHEMA |
| Dataform | SQLX, workflow schedules, assertions, ref(), IAM-native, no extra infra |
| Dataflow/Beam | PCollection, PTransform, windowing, watermarks, Pub/Sub source, unified batch+stream |
| Reverse ETL | Data Activation, sync_log audit, API rate limiting, idempotency, upsert key |
| AI Tooling | First-draft mindset, expert review discipline, execution plan analysis, test generation |
| Python | Generators, custom operators, DRY principle, internal shared libraries |
| SCD Type 2 | is_current, valid_from/valid_to, MERGE statement, slowly changing dimensions |
