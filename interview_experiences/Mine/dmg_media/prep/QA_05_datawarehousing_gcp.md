# Data Warehousing & GCP Tools - Most Asked Interview Questions & Answers

---

## Q1. What is the difference between a Data Warehouse, Data Lake, and Lakehouse?

**Answer:**

### Data Warehouse (e.g., BigQuery, Snowflake, Redshift)
- Stores **structured, processed data** optimized for SQL analytics
- Schema-on-write (define schema before loading)
- Fast query performance for business users
- High cost for raw storage
- **BigQuery** is a serverless data warehouse

### Data Lake (e.g., GCS, S3)
- Stores **raw data in any format** (CSV, JSON, Parquet, images, logs)
- Schema-on-read (interpret structure when querying)
- Cheap storage, but slow queries on raw data
- Requires data engineers to process before use

### Lakehouse (e.g., Databricks Delta Lake, BigLake on GCS)
- Combines the best of both: **cheap lake storage + warehouse query performance**
- ACID transactions on lake storage
- Supports both SQL analysts and data scientists (ML, Python)
- Uses open formats (Delta, Iceberg, Hudi)

**In GCP context:**
- **Data Lake**: Raw files in GCS
- **Data Warehouse**: BigQuery
- **Lakehouse**: BigQuery + GCS with BigLake, or Dataproc Metastore + GCS

---

## Q2. What is ETL vs ELT? Which do modern cloud data platforms prefer?

**Answer:**

### ETL (Extract → Transform → Load)
- Transform data **before** loading into the warehouse
- Transformation done in a separate tool (Informatica, SSIS, Spark)
- The warehouse only gets clean, structured data
- Traditional pattern — used when the warehouse couldn't handle transformation at scale

### ELT (Extract → Load → Transform)
- Load **raw data first** into the warehouse → transform inside using SQL
- Modern pattern, enabled by powerful cloud warehouses (BigQuery, Snowflake)
- Cheaper: cloud storage is cheap, load raw then transform as needed
- More flexible: raw data preserved, can re-transform as requirements change
- Tools: **dbt**, Dataform, BigQuery stored procedures

```
ELT Flow in GCP:
API/DB → (raw CSV/JSON) → GCS → BQ staging table → BQ transformed tables (via SQL/dbt)
```

**Modern cloud platforms prefer ELT** because:
1. Storage is cheap (GCS/BQ storage ~ $0.02/GB/month)
2. BigQuery can handle massive transformations in seconds
3. You keep raw data as a source of truth — great for re-processing
4. Separation of concerns: data engineers own the loading, analysts own the transformations (dbt)

---

## Q3. Explain Star Schema vs Snowflake Schema. Which would you use in BigQuery?

**Answer:**

### Star Schema
```
                   dim_date
                      |
dim_customer — fact_orders — dim_product
                      |
                  dim_region
```
- Fact table at center, **denormalized flat dimension tables** around it
- Fewer JOINs → faster queries
- More storage (repeated data across dim tables)
- Best for **query performance**

### Snowflake Schema
```
dim_country
    |
dim_region — fact_orders — dim_product — dim_category — dim_department
    |
dim_customer
```
- Dimension tables are **normalized** (broken into sub-dimensions)
- More JOINs needed
- Less storage (normalized, no repetition)
- Best for **storage efficiency and data integrity**

**In BigQuery: use Star Schema** because:
- BigQuery compute is expensive, storage is cheap → opposite trade-off to traditional DBs
- BigQuery handles JOINs across large tables well, but reducing JOINs still helps
- Simpler schema = faster analyst queries
- Or go even flatter using BigQuery's **nested/repeated fields** (ARRAY/STRUCT) to embed related data in one table

---

## Q4. What are Slowly Changing Dimensions (SCD)? Explain Types 1, 2, and 3.

**Answer:**

SCD handles how dimension data changes over time (e.g., a customer changes their email or address).

### SCD Type 1 — Overwrite (no history)
```sql
UPDATE dim_customer
SET email = 'new@email.com', updated_at = CURRENT_TIMESTAMP()
WHERE customer_id = 123;
```
✅ Simple | ❌ No history preserved | Use when: history doesn't matter

### SCD Type 2 — Track full history (most common)
```
customer_id | email           | is_current | valid_from  | valid_to
123         | old@email.com   | FALSE      | 2022-01-01  | 2024-01-14
123         | new@email.com   | TRUE       | 2024-01-15  | NULL
```
✅ Full history | ❌ Queries need to filter on `is_current = TRUE` or date range
Use when: need to reconstruct the state at any point in time

### SCD Type 3 — Previous value column
```
customer_id | email         | prev_email
123         | new@email.com | old@email.com
```
✅ Simple | ❌ Only 1 historical value | Use when: only "current vs previous" matters

**BigQuery SCD Type 2 MERGE:**
```sql
-- Step 1: Expire old records
UPDATE dim_customer
SET is_current = FALSE, valid_to = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
WHERE customer_id IN (
  SELECT c.customer_id FROM staging s
  JOIN dim_customer c ON s.customer_id = c.customer_id AND c.is_current = TRUE
  WHERE s.email != c.email
);

-- Step 2: Insert new records
INSERT INTO dim_customer (customer_id, email, is_current, valid_from, valid_to)
SELECT customer_id, email, TRUE, CURRENT_DATE(), NULL
FROM staging s
WHERE NOT EXISTS (
  SELECT 1 FROM dim_customer c
  WHERE c.customer_id = s.customer_id AND c.email = s.email AND c.is_current = TRUE
);
```

---

## Q5. What is a Fact Table vs a Dimension Table? Give examples.

**Answer:**

### Fact Table
- Stores **measurable business events** (transactions, clicks, page views, orders)
- Contains **numeric measures** (revenue, quantity, duration)
- Contains **foreign keys** to dimension tables
- Usually very large (millions to billions of rows)
- Examples: `fact_orders`, `fact_page_views`, `fact_ad_impressions`

```
fact_orders:
| order_id | customer_id (FK) | product_id (FK) | date_id (FK) | revenue | quantity |
```

### Dimension Table
- Stores **descriptive attributes** about the entities in fact tables
- Contains **text/categorical data** (names, categories, locations)
- Relatively small (thousands to millions of rows)
- Examples: `dim_customer`, `dim_product`, `dim_date`, `dim_geography`

```
dim_customer:
| customer_id | name | email | country | segment | signup_date |

dim_date:
| date_id | date | day_of_week | week | month | quarter | year | is_holiday |
```

**Why a separate date dimension?** Because you can attach business attributes (is_holiday, fiscal_quarter) that don't exist in a plain date field, enabling rich time-based analysis.

---

## Q6. What is the grain of a fact table and why does it matter?

**Answer:**

The **grain** defines **exactly what one row represents** in a fact table. It must be decided first before designing the fact table — everything else flows from it.

**Example grains:**
- `fact_orders` grain = **one row per order line item** (not per order)
- `fact_page_views` grain = **one row per page view event**
- `fact_daily_sales_summary` grain = **one row per product per day** (aggregated)

**Why it matters:**
- Determines what measures you can store and at what level of detail
- Defines what JOIN keys you need
- Affects storage size and query patterns

**Gotcha:** Mixing grains in one fact table is a design error. E.g., having order-level rows AND order-line-level rows in the same table causes incorrect aggregations.

```sql
-- Wrong: mixing grain
-- order_total is repeated for every line item → SUM gives wrong total
SELECT order_id, SUM(order_total) FROM fact_orders GROUP BY order_id;
-- ❌ This double-counts! order_total should be in a separate order-level fact table.
```

---

## Q7. What are incremental loads and how do you implement them in BigQuery?

**Answer:**

**Full load**: Truncate and reload all data every run. Simple but wastes compute for large tables.

**Incremental load**: Load only **new or changed records** since the last run.

### Append-only (no updates)
```sql
-- Load only events from yesterday
INSERT INTO dataset.events
SELECT *
FROM dataset.events_raw
WHERE DATE(created_at) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY);
```

### Watermark-based (with updates)
```sql
-- Track last loaded timestamp
INSERT INTO dataset.users
SELECT *
FROM source.users
WHERE updated_at > (SELECT MAX(updated_at) FROM dataset.users);
```

### Partition-based (most reliable in BQ)
```sql
-- Delete partition for the date, then reload (idempotent)
DELETE FROM dataset.events WHERE event_date = @run_date;

INSERT INTO dataset.events
SELECT *, @run_date AS event_date
FROM source.events_raw
WHERE DATE(created_at) = @run_date;
```

**Why partition-based is preferred:**
- Idempotent (safe to re-run)
- Atomic at partition level
- Works with BQ's partition pruning

---

## Q8. What GCP services would you use to build a real-time data pipeline?

**Answer:**

```
IoT/App → Pub/Sub → Dataflow → BigQuery (streaming insert) → Looker
```

**Step-by-step:**

1. **Pub/Sub** — message queue that decouples producers from consumers. Handles millions of events/second with at-least-once delivery.

2. **Dataflow (Apache Beam)** — processes the Pub/Sub stream. Can filter, transform, aggregate, and handle late-arriving data (windowing).

3. **BigQuery Streaming** — Dataflow writes results to BigQuery via streaming insert. Data visible within seconds.

4. **Cloud Monitoring + Alerting** — monitor pipeline health, set up alerts for lag, errors.

**For batch (daily/hourly):**
```
GCS (files) → Cloud Composer (Airflow) → BigQuery (load job) → Looker
```

---

## Q9. How do you handle late-arriving data in a pipeline?

**Answer:**

Late-arriving data = events that happened in the past but arrive in your pipeline after you've already processed that time window.

**Approaches:**

**1. Reprocessing (batch):**
Re-run the pipeline for the affected date when late data is detected.
```sql
-- In Airflow: trigger backfill for affected partition
airflow dags backfill my_dag -s 2024-01-10 -e 2024-01-10
```

**2. Merge/Upsert instead of append:**
```sql
-- Use MERGE so late-arriving records update existing ones
MERGE fact_events T USING new_batch S ON T.event_id = S.event_id
WHEN NOT MATCHED THEN INSERT ROW
WHEN MATCHED THEN UPDATE SET T.value = S.value;
```

**3. Streaming with watermarks (Dataflow):**
```python
# In Apache Beam streaming:
# Allow events up to 1 hour late
pcoll | beam.WindowInto(
    beam.window.FixedWindows(3600),   # 1 hour windows
    allowed_lateness=beam.window.Duration(seconds=3600),  # accept up to 1hr late
    trigger=...,
)
```

**4. Append with snapshot_date:**
```sql
-- Keep all versions with load date
-- Query for the "correct" version by selecting latest loaded_at per event_id
SELECT * EXCEPT(rn) FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY loaded_at DESC) rn
  FROM fact_events_with_history
) WHERE rn = 1
```

---

## Q10. What is the difference between Dataflow and Dataproc?

**Answer:**

| | Dataflow | Dataproc |
|--|---------|---------|
| Engine | Apache Beam | Apache Spark / Hadoop |
| Mode | Streaming + Batch | Primarily Batch |
| Cluster management | Fully serverless (no clusters) | Manages clusters (you choose machine types) |
| Auto-scaling | Yes, automatic | Manual or autoscaling config |
| Startup time | Minutes | 1-2 minutes (fast), but cluster persists |
| Cost model | Pay per vCPU/hour used | Pay for cluster while it runs |
| Best for | New pipelines, streaming, GCP-native | Migrating existing Spark/Hadoop workloads |
| Language | Python/Java (Beam SDK) | PySpark, Scala, SQL (HiveQL) |

**Simple rule:**
- Starting fresh on GCP → **Dataflow**
- Have existing Spark code → **Dataproc**
- Need streaming → **Dataflow** (Dataproc can do it but Beam is cleaner)

---

## Q11. What is data quality? How do you implement data quality checks?

**Answer:**

Data quality ensures your data is **accurate, complete, consistent, timely, and valid**.

**Dimensions:**
- **Completeness**: Are there NULLs where there shouldn't be?
- **Accuracy**: Are values correct (e.g., age not negative)?
- **Consistency**: Does user_id exist in dim_users for every fact row?
- **Timeliness**: Is data fresh enough (arrived within expected window)?
- **Uniqueness**: No duplicate records?

**Implementation:**
```sql
-- Row count check (compare against expected range)
ASSERT (SELECT COUNT(*) FROM staging WHERE load_date = CURRENT_DATE()) > 1000
  AS 'Too few rows loaded today';

-- Null check on required columns
ASSERT (SELECT COUNT(*) FROM staging WHERE user_id IS NULL) = 0
  AS 'NULL user_ids found';

-- Duplicate check
ASSERT (
  SELECT COUNT(*) FROM (
    SELECT event_id FROM staging GROUP BY event_id HAVING COUNT(*) > 1
  )
) = 0 AS 'Duplicate event_ids found';

-- Referential integrity
ASSERT (
  SELECT COUNT(*) FROM fact_orders f
  LEFT JOIN dim_users d ON f.user_id = d.user_id
  WHERE d.user_id IS NULL
) = 0 AS 'Orphaned user_ids in fact_orders';
```

**In Airflow:** Add a `PythonOperator` task after load that runs these checks and raises an exception if any fail.

**Tools:** Great Expectations, dbt tests, custom SQL assertions.

---

## Q12. What is Cloud Composer and how is it different from self-hosted Airflow?

**Answer:**

**Cloud Composer** is Google's **fully managed Airflow service** on Google Kubernetes Engine (GKE).

| Feature | Self-hosted Airflow | Cloud Composer |
|---------|--------------------|--------------------|
| Setup | Manual (install, configure DB, workers) | One-click deploy |
| Maintenance | You manage upgrades, scaling | Google manages |
| HA | Manual setup | Built-in |
| Scaling | Manual worker management | Auto-scales |
| DAG deployment | Copy to local FS | Copy to GCS bucket |
| Monitoring | Set up Prometheus/Grafana | Cloud Monitoring built-in |
| Cost | Infrastructure cost | Composer environment cost (~$300-500+/month) |
| GCP Integration | Manual (connection setup) | Native (auto IAM for BQ, GCS, etc.) |

**DAG deployment in Composer:**
```bash
# Simply copy to the GCS dags folder
gcloud composer environments storage dags import \
  --environment=my-composer-env \
  --location=us-central1 \
  --source=my_dag.py

# Airflow picks it up within 1-2 minutes
```

**Best practice:** In production, use CI/CD to auto-deploy DAGs to the Composer bucket when merged to main branch.
