# BigQuery — 20 Interview Questions with Full Answers
# Format: Question → Answer, in interview-ready language

---

**What is BigQuery and how does it differ from a traditional database?**

BigQuery is Google's serverless, fully managed **columnar data warehouse** built for large-scale analytics (OLAP). Traditional databases like Postgres or MySQL are OLTP — designed for apps doing many small fast reads/writes (insert one order, read one user). BigQuery is the opposite: it handles a few massive analytical queries scanning millions or billions of rows.

Key differences:
- **Storage:** BigQuery is columnar (reads only the columns you SELECT). Postgres is row-based (reads every column even if you only need 2).
- **Scaling:** BigQuery has no servers to manage — compute auto-scales to thousands of workers. Postgres runs on a fixed server.
- **Indexes:** Postgres relies on indexes for fast lookups. BigQuery has no indexes — it uses partitioning and clustering instead.
- **Cost:** BigQuery charges $5 per TB of data scanned. Postgres charges for fixed server uptime.
- **Transactions:** Postgres supports full ACID transactions. BigQuery has limited DML and is not built for high-frequency row updates.

---

**Explain BigQuery architecture — what happens when you run a query?**

BigQuery has two main components: **Colossus** (storage layer — where data lives) and **Dremel** (compute layer — the query engine). These are completely separate and scale independently.

When you run a query:
1. **Dremel** receives the query and creates an execution plan — breaking it into stages.
2. **Stage 1 (Leaf Workers):** Thousands of workers spin up in parallel, each reading a chunk of data. They read **only the columns you requested** (columnar benefit) from **only the partitions your WHERE clause matches** (partition pruning). This is the stage you're billed for — bytes read here.
3. **Stage 2 (Mixer Workers):** Leaf workers send partial results (e.g. partial GROUP BY counts) to mixer workers over the network. Mixers merge and aggregate. This shuffle is expensive if there's a lot of data moving.
4. **Stage 3 (Root Worker):** Final ORDER BY, then results returned to you.

This is why BigQuery can scan 1TB in seconds — not because it's fast per worker, but because it uses 10,000 workers reading in parallel.

---

**What is the difference between partitioning and clustering? When would you use both?**

**Partitioning** divides the table into separate physical file groups by a column value — most commonly a date. When your WHERE clause filters on the partition column, BigQuery skips entire partitions without reading them. A 3-year table filtered to 1 day scans ~0.3% of the data.

**Clustering** sorts data within each partition by one or more columns. BigQuery reads block metadata and skips blocks where the sorted values can't match your filter. It's a secondary saving on top of partitioning.

Use **both** when you always filter by date AND one or more other columns:
```sql
CREATE TABLE orders
PARTITION BY DATE(order_time)   -- skip entire days
CLUSTER BY country, category    -- skip blocks within a day
```
A query filtering `WHERE DATE(order_time) = '2024-01-15' AND country = 'UK'` might scan 100TB → 3TB (partition) → 0.6TB (clustering). Put the most-filtered column first in CLUSTER BY.

---

**What is partition pruning and what breaks it?**

Partition pruning is when BigQuery reads the partition metadata and skips entire partitions before scanning any data. This only works if BigQuery can evaluate which partitions to skip **before running the query** — which means the partition column must appear as-is or wrapped only in `DATE()`.

**Works (pruning ON):**
```sql
WHERE DATE(order_time) = '2024-01-15'
WHERE order_time BETWEEN '2024-01-15' AND '2024-01-15 23:59:59'
```

**Breaks (full table scan — no error shown!):**
```sql
WHERE CAST(order_time AS DATE) = '2024-01-15'    -- CAST breaks it
WHERE FORMAT_DATE('%Y-%m-%d', order_time) = '...' -- FORMAT breaks it
WHERE EXTRACT(YEAR FROM order_time) = 2024        -- EXTRACT alone breaks it
```

Why does wrapping break it? BQ can't evaluate `CAST(order_time AS DATE)` for each partition without actually reading the data first. So it reads everything. This is the most common silent performance killer in BigQuery.

---

**On-demand vs flat-rate pricing — which would you recommend and why?**

**On-demand:** $5 per TB scanned. You pay only when you run queries — $0 when idle. Bills are unpredictable — a badly written query can cost hundreds of dollars unexpectedly. Best for low or variable usage, small teams, dev/test.

**Flat-rate (slots):** You buy a fixed number of "slots" (compute workers) for a fixed monthly price. Whether you scan 1GB or 1PB — same cost. Predictable. Best for production pipelines running constantly.

**My recommendation for DMG Media:** Flat-rate for production Airflow pipelines (they run daily/hourly — consistent usage, predictable cost). On-demand for analyst ad-hoc queries (variable — pay only when used). Before switching to flat-rate, set up **slot reservations** to divide slots between teams:
```
Pipelines: 300 slots | Analysts: 150 slots | Dashboards: 50 slots
```
Without reservations, all teams compete for the same pool — heavy pipelines can starve analysts.

Break-even: if you're spending > ~$2,000/month on-demand, flat-rate likely saves money.

---

**How do you optimize a slow BigQuery query? Walk through the cost story.**

Starting with a 100TB unoptimized table — here's the step-by-step cost reduction:

**Start:** `SELECT *` with no filters → **100TB = $500 per run**

**Step 1 — Add partitioning + filter with `DATE(col)`**
BigQuery skips 364 days of data. A year has ~365 days. One day's data ≈ 3TB.
→ **3TB = $15** (97% reduction)

**Step 2 — Add clustering on `country`, filter by country**
UK is ~20% of traffic. Clustering lets BQ skip the other 80% of blocks.
→ **0.6TB = $3** (80% further reduction)

**Step 3 — SELECT only needed columns**
We need 3 of 50 columns. Columnar storage means unused columns are never read.
→ **0.12TB = $0.60** (80% further reduction)

**Step 4 — Filter before JOIN + use APPROX functions**
Push the WHERE filter into a CTE before joining. Use `APPROX_COUNT_DISTINCT` instead of `COUNT(DISTINCT)`.
→ **0.05TB = $0.25** (final)

**Result: $500 → $0.25 per run. 99.95% cost reduction.**

---

**What is a window function? Give examples of ROW_NUMBER, LAG, and running total.**

A window function computes an aggregation across related rows **without collapsing them** — unlike GROUP BY which reduces rows. You keep all original rows but get an aggregate value on each one.

**ROW_NUMBER** — unique sequential number per group. Most common use: deduplication.
```sql
-- Keep only the latest record per user
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) AS rn
  FROM users
)
SELECT * EXCEPT(rn) FROM ranked WHERE rn = 1;
```

**LAG** — access the previous row's value. Use for day-over-day or period comparisons.
```sql
SELECT date, revenue,
  LAG(revenue, 1) OVER (ORDER BY date) AS prev_day,
  revenue - LAG(revenue, 1) OVER (ORDER BY date) AS daily_change
FROM daily_sales;
-- LAG(col, N) looks N rows back. LAG(col, 7) = same day last week.
```

**Running total** — cumulative sum using SUM with ORDER BY.
```sql
SELECT date, revenue,
  SUM(revenue) OVER (ORDER BY date) AS cumulative_total
FROM daily_sales;
-- With ORDER BY, the default frame is UNBOUNDED PRECEDING to CURRENT ROW
-- Each row gets the sum of all rows up to and including itself
```

---

**Write a query to find the top 3 products by revenue for each category.**

```sql
WITH ranked AS (
  SELECT
    product_id,
    name,
    category,
    revenue,
    ROW_NUMBER() OVER (
      PARTITION BY category     -- restart rank for each category
      ORDER BY revenue DESC     -- rank 1 = highest revenue
    ) AS rn
  FROM products
)
SELECT product_id, name, category, revenue
FROM ranked
WHERE rn <= 3;   -- keep top 3 per category
```

Why use a CTE? You can't filter on a window function in the WHERE clause of the same SELECT — window functions run during SELECT, but WHERE runs before SELECT. The CTE runs the inner query completely first, making `rn` available to filter on.

Use `DENSE_RANK()` instead of `ROW_NUMBER()` if you want ties to all be included (e.g. if two products share rank 1, you'd get 4 rows for that category instead of 3).

---

**What is the difference between RANK and DENSE_RANK?**

Both assign the same rank to tied values — but differ in what happens to the next rank after a tie.

```
Values: 100, 100, 90, 80

ROW_NUMBER:   1, 2, 3, 4    -- always unique, no concept of ties
RANK:         1, 1, 3, 4    -- ties share rank, SKIPS the next number
DENSE_RANK:   1, 1, 2, 3    -- ties share rank, does NOT skip
```

**RANK** is like Olympic medals: two people win gold, no one gets silver, next is bronze (3rd). The gap exists intentionally.

**DENSE_RANK** is like a leaderboard: two people tied at #1, the next person is #2 (not #3).

**When to use which:**
- `ROW_NUMBER` → when you need unique values (deduplication — pick exactly one row)
- `RANK` → when ties should create gaps (exam rankings, sports results)
- `DENSE_RANK` → when you want sequential ranking without gaps (app leaderboards)

---

**What is MERGE and when would you use it vs DELETE+INSERT?**

MERGE combines INSERT + UPDATE + DELETE in one atomic statement. It matches rows between a source and target table and applies different actions depending on whether a match is found.

```sql
MERGE dataset.users AS target
USING dataset.users_staging AS source
ON target.user_id = source.user_id

WHEN MATCHED AND target.email != source.email THEN
  UPDATE SET target.email = source.email, target.updated_at = CURRENT_TIMESTAMP()

WHEN NOT MATCHED BY TARGET THEN
  INSERT (user_id, email, created_at) VALUES (source.user_id, source.email, CURRENT_TIMESTAMP())

WHEN NOT MATCHED BY SOURCE THEN
  DELETE;  -- optional: remove rows that disappeared from source
```

**Use MERGE when:** you're syncing individual changed records and don't know which rows changed (e.g. a users table where any user might have updated their email). MERGE finds them row by row.

**Use DELETE+INSERT when:** you're reloading an entire date partition. Simpler, faster — no row-level matching overhead. Just wipe the partition and reload fresh:
```sql
DELETE FROM dataset.events WHERE event_date = '2024-01-15';
INSERT INTO dataset.events SELECT * FROM staging WHERE event_date = '2024-01-15';
```

Both patterns are idempotent — safe to rerun if Airflow retries.

---

**What is a stored procedure in BigQuery? Write one for a daily load.**

A stored procedure is reusable multi-step SQL logic stored inside BigQuery — like a Python function but written in SQL. It supports variables, conditionals, loops, and error handling. Called with `CALL`, not inside SELECT.

```sql
CREATE OR REPLACE PROCEDURE dataset.load_daily(IN run_date DATE)
BEGIN
  -- Declare a variable
  DECLARE rows_loaded INT64;

  -- Step 1: Delete existing data for this date (makes it safe to rerun)
  DELETE FROM dataset.order_summary WHERE summary_date = run_date;

  -- Step 2: Insert fresh aggregation
  INSERT INTO dataset.order_summary (summary_date, country, order_count, total_revenue)
  SELECT
    run_date,
    country,
    COUNT(*),
    SUM(revenue)
  FROM dataset.orders
  WHERE DATE(order_time) = run_date
  GROUP BY country;

  -- Step 3: Capture how many rows were loaded
  SET rows_loaded = @@row_count;   -- rows affected by the last DML

  -- Step 4: Validate — if nothing loaded, something is wrong
  IF rows_loaded = 0 THEN
    RAISE USING MESSAGE = CONCAT('No data found for: ', CAST(run_date AS STRING));
  END IF;

  -- Step 5: Return a summary
  SELECT run_date AS processed_date, rows_loaded AS rows_inserted;
END;

-- Call it from Airflow or manually:
CALL dataset.load_daily('2024-01-15');
```

Use stored procedures when the pipeline is purely SQL steps. Airflow calls one `CALL` statement instead of managing multiple SQL strings in Python.

---

**What is the difference between a view and a materialized view?**

**View:** A saved SQL query — no data is stored. Every time you query it, BigQuery runs the underlying SQL fresh against the base table. Always shows live data. No performance benefit — if the underlying query scans 1TB, the view scans 1TB. Use for abstraction (simplify complex queries, restrict column access).

**Materialized View:** Physically stores the pre-computed result of a query. BigQuery automatically refreshes it within ~30 minutes of base table changes. The killer feature: **BigQuery rewrites your queries to use the materialized view transparently** — even if you query the base table directly. Use for expensive aggregations queried repeatedly (daily revenue summaries, dashboard metrics).

Example: your analytics team runs this 200 times/day — 1TB scan, $5 each = $1,000/day:
```sql
SELECT DATE(event_time), country, COUNT(*) FROM events GROUP BY 1, 2;
```
Create a materialized view covering this pattern. BigQuery serves it from the pre-computed result (tiny scan). Same query, 99% cheaper.

---

**What is APPROX_COUNT_DISTINCT and why would you use it?**

`APPROX_COUNT_DISTINCT(col)` is an approximate version of `COUNT(DISTINCT col)`. It uses the HyperLogLog algorithm — each worker maintains a tiny mathematical sketch (a few KB) of which values it's seen, then combines sketches across workers. This avoids shuffling millions of actual values across the network.

Result: 99% accurate, but 10-100x cheaper and faster than exact COUNT(DISTINCT) on large datasets.

```sql
-- Exact: must shuffle ALL 500M user_id values to one node
SELECT COUNT(DISTINCT user_id) FROM events

-- Approximate: workers combine tiny sketches, not actual values
SELECT APPROX_COUNT_DISTINCT(user_id) FROM events
```

**Use when:** counting unique users, sessions, products for dashboards, analytics, trend analysis — anything where 99% accuracy is fine.

**Don't use when:** billing, financial reporting, compliance reporting — anywhere exact numbers are required.

---

**How do you load data from GCS into BigQuery?**

**Python (most common in Airflow):**
```python
from google.cloud import bigquery

client = bigquery.Client()
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    write_disposition='WRITE_TRUNCATE',   # wipe then load
    autodetect=True,                      # detect schema from Parquet
)
load_job = client.load_table_from_uri(
    'gs://my-bucket/data/2024-01-15/*.parquet',
    'project.dataset.orders',
    job_config=job_config
)
load_job.result()  # blocks until job finishes
print(f"Loaded {load_job.output_rows} rows")
```

**SQL (LOAD DATA):**
```sql
LOAD DATA INTO dataset.orders
FROM FILES (format='PARQUET', uris=['gs://bucket/data/2024-01-15/*.parquet']);
```

Loading is **free** — BigQuery doesn't charge for load jobs. Always prefer **Parquet** over CSV — columnar, compressed, self-describing.

`write_disposition` options:
- `WRITE_TRUNCATE` → wipe the table then load (safe full reload)
- `WRITE_APPEND` → add rows (careful — duplicates if rerun!)
- `WRITE_EMPTY` → only load if table is empty, error otherwise

---

**What is an external table and when would you use it?**

An external table is a BigQuery table definition that points to files in GCS — BQ reads them directly at query time without ever moving the data into BigQuery storage.

```sql
CREATE EXTERNAL TABLE dataset.archive_orders
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://archive-bucket/orders/2020/*.parquet']
);

-- Query it like a normal table — data stays in GCS
SELECT country, SUM(revenue) FROM dataset.archive_orders GROUP BY 1;
```

**Advantages:** Zero BigQuery storage cost. Data stays in GCS. Instant setup — no load job needed.

**Disadvantages:** No partitioning or clustering benefits. Slower than native tables (BQ reads GCS at query time). No DML allowed (can't INSERT/UPDATE/DELETE/MERGE).

**Use when:** Querying archive data you rarely need. Querying data you don't own or control. One-off analysis without committing to loading it. For anything queried regularly, load into a native BQ table with partitioning.

---

**How do you handle a bad data load? How do you roll it back?**

BigQuery automatically keeps **7 days of previous table versions** — this is called Time Travel.

```sql
-- Restore entire table to state before the bad load
CREATE OR REPLACE TABLE dataset.orders AS
SELECT * FROM dataset.orders
FOR SYSTEM_TIME AS OF '2024-01-15 09:00:00';  -- timestamp before bad load ran

-- Or restore just one date partition
DELETE FROM dataset.orders WHERE event_date = '2024-01-15';
INSERT INTO dataset.orders
SELECT * FROM dataset.orders
FOR SYSTEM_TIME AS OF '2024-01-15 06:00:00'
WHERE event_date = '2024-01-15';
```

**If the bad load was > 7 days ago:** reload from the raw GCS files — which is why you always keep raw files in GCS permanently (never delete after loading).

**Prevention:** Always load to a staging table first, validate row counts and data quality, then merge/swap into production. Never load directly to production tables.

---

**Can you add partitioning to an existing table? How?**

No — partitioning must be defined at table creation time. BigQuery cannot retroactively add partitioning to an existing unpartitioned table.

**The workaround — CTAS (Create Table As Select):**

```sql
-- Step 1: Create a new table with partitioning (copies all data)
CREATE TABLE dataset.orders_new
PARTITION BY DATE(order_time)
CLUSTER BY country
AS SELECT * FROM dataset.orders_old;

-- Step 2: Validate row counts match
SELECT COUNT(*) FROM dataset.orders_old;     -- e.g. 500,000,000
SELECT COUNT(*) FROM dataset.orders_new;     -- should match exactly

-- Step 3: Swap the table names
ALTER TABLE dataset.orders_old RENAME TO orders_backup;
ALTER TABLE dataset.orders_new RENAME TO orders;

-- Step 4: Drop backup once you're confident
DROP TABLE dataset.orders_backup;
```

This is a one-time cost — you pay to scan the full table once to copy it. But after that, every query saves money through partition pruning.

Note: clustering CAN be added to or changed on an existing table with `ALTER TABLE CLUSTER BY col1, col2` — no CTAS needed.

---

**What does @@row_count do in a stored procedure?**

`@@row_count` is a system variable in BigQuery stored procedures that holds the number of rows affected by the **most recent** INSERT, UPDATE, DELETE, or MERGE statement.

```sql
INSERT INTO dataset.summary SELECT ...;
SET rows_loaded = @@row_count;   -- capture immediately after the INSERT

IF rows_loaded = 0 THEN
  RAISE USING MESSAGE = 'No rows were loaded — something is wrong!';
END IF;
```

Important: `@@row_count` is reset by the next DML statement, so capture it immediately after the operation you care about. It's the primary way to validate that data actually loaded — if `@@row_count = 0` after an INSERT, either the source had no matching rows or something went wrong.

---

**How do you monitor query costs in BigQuery?**

**1. INFORMATION_SCHEMA — the main tool:**
```sql
SELECT
  user_email,
  ROUND(total_bytes_billed/1e9, 2) AS gb_billed,
  ROUND(total_bytes_billed/1e12 * 5, 2) AS est_cost_usd,
  total_slot_ms,
  SUBSTR(query, 1, 200) AS query_preview
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY total_bytes_billed DESC
LIMIT 20;
```
This shows you the most expensive queries in the last 7 days — great for auditing and finding optimization targets.

**2. Query plan (Explain):** Click the Explain button in BQ console after running a query. Shows each stage's input/output bytes and slot time — helps identify which stage is the bottleneck.

**3. Cost estimate before running:** BQ shows estimated bytes to be processed before you run a query. Check this before running on large tables.

**4. Cloud Monitoring:** Set up billing alerts on GCP project spend. Get notified if daily BQ spend exceeds a threshold.

**5. Maximum bytes billed (prevent runaway queries):**
```python
QueryJobConfig(maximum_bytes_billed=10 * 1024**3)  # fail if > 10GB
```

---

**What file format do you prefer for BigQuery loads and why?**

**Parquet — always, for production pipelines.**

Reasons:
1. **Columnar:** Parquet stores data column-by-column — exactly how BigQuery stores it internally. Loading Parquet requires minimal conversion, making it faster to ingest.
2. **Compressed:** Parquet files are typically 5-10x smaller than equivalent CSV files. Less data to upload = faster transfers, less GCS storage cost.
3. **Self-describing schema:** Parquet embeds the schema in the file — BigQuery can auto-detect column names and types without you defining them.
4. **Typed:** Integers stay integers, timestamps stay timestamps. CSV is all strings — BQ must parse and convert every value, which is slower and error-prone (e.g. `"2024-01-15"` might be read as string instead of date).

When is CSV acceptable? Simple one-off loads, data coming from systems that only export CSV, or when sharing data with humans who need to read it.

**Never use CSV for production pipelines if you can avoid it.**
