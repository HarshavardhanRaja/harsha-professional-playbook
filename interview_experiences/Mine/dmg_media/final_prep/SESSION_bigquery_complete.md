# BigQuery — Pre-Interview Reference
# Sharp, skimmable, complete. Read this the morning of your interview.

---

# PART 1 — ARCHITECTURE

## What BigQuery IS (say this first in any architecture question)
BigQuery is Google's **serverless, columnar data warehouse** built for large-scale analytics (OLAP).
It is NOT a transactional database — it's designed for few massive analytical queries, not thousands of small ones.

**Key architecture: Storage and Compute are SEPARATE**
- **Colossus** = where data is stored (Google's distributed file system, cheap)
- **Dremel** = the query engine that processes queries (auto-scales, serverless)
- You pay for storage and compute independently

---

## Columnar Storage — why BQ is fast

**Row-based (Postgres):** stores all columns of a row together.
→ `SELECT revenue, country` still reads ALL 50 columns per row. Wasteful.

**Columnar (BigQuery):** stores each column separately.
→ `SELECT revenue, country` reads ONLY 2 columns. Skips the other 48.
→ `SELECT *` forces BQ to read all columns = expensive!

**Rule: always select only the columns you need.**

---

## What happens when you run a query

```
Your query → Dremel creates an execution plan → breaks into 3 stages:

Stage 1 (Leaf Workers)  → thousands of workers read data IN PARALLEL
                           each reads a chunk, applies WHERE, partial aggregation
                           THIS IS WHAT YOU'RE BILLED FOR (bytes read here)

Stage 2 (Mixer Workers) → workers send partial results to mixers
                           mixers merge/aggregate (GROUP BY happens here)
                           expensive if too much data shuffles across network

Stage 3 (Root Worker)   → final ORDER BY, returns result to you
```

**Key insight:** Cost = bytes read in Stage 1. All optimization = reduce bytes read.

---

## OLTP vs OLAP — know this cold

| | OLTP (Postgres, MySQL) | OLAP (BigQuery) |
|--|----------------------|----------------|
| Use case | Apps — insert/update/read single rows | Analytics — aggregate millions of rows |
| Query pattern | Many small fast queries | Few massive slow queries |
| Storage | Row-based | Columnar |
| Indexes | Yes (essential) | No (uses partitioning/clustering) |
| Examples | Uber app, Amazon checkout | Business dashboards, data pipelines |

---

## Interview Q&A — Architecture

**Q: Why doesn't BigQuery have indexes?**
> Indexes help find ONE specific row fast — great for apps doing single-row lookups. BigQuery always scans millions of rows to aggregate — an index can't help with that. Instead BQ uses partitioning (skip whole date ranges) and clustering (skip blocks within a partition), which work at a much larger scale.

**Q: Explain BigQuery architecture in 60 seconds.**
> BigQuery separates storage (Colossus) from compute (Dremel). When you run a query, Dremel spins up thousands of workers automatically — they read only the columns you requested from only the partitions your WHERE clause matches, compute partial aggregations in parallel, shuffle results to mixer nodes, and return the final answer. You pay only for bytes scanned in that read stage — which is why all query optimization focuses on reducing how much data gets read.

**Q: What is the difference between BigQuery and a traditional database?**
> BigQuery is OLAP — designed for massive analytical scans on structured data. Traditional databases are OLTP — designed for many concurrent small transactional reads/writes. BQ is columnar (reads only needed columns), serverless (no infrastructure), and charges per byte scanned. Postgres is row-based, server-managed, and charges for fixed compute. You'd never use BQ for an app backend, and you'd never use Postgres to aggregate 1 billion rows.

---

# PART 2 — PRICING

## On-Demand vs Flat-Rate

### On-Demand — pay per query
- **$5 per TB** of data scanned
- Pay nothing when idle
- Unpredictable — bad query = surprise bill
- Best for: low/variable usage, small teams

### Flat-Rate / Slots — pay fixed monthly fee
- Buy **slots** (compute workers) upfront — fixed monthly cost
- Scan 1GB or 1PB — same price
- Predictable cost, protects against runaway queries
- Best for: high query volume, production pipelines, large teams
- Break-even: ~$2,000/month on-demand → consider switching

### What is a slot?
One slot = one BigQuery compute worker. Think of it as hiring a worker for the month.

### Slot Reservations — how to divide slots between teams
```
Without: 500 slots shared → pipelines starve analysts

With reservations:
  Pipelines:  300 slots (guaranteed)
  Analysts:   150 slots (guaranteed)
  Dashboards:  50 slots (guaranteed)
```
Set this up before switching to flat-rate or teams will fight for compute.

---

## Interview Q&A — Pricing

**Q: On-demand vs flat-rate — which would you recommend for a company with daily Airflow pipelines?**
> For production pipelines running daily/hourly, flat-rate slots make more sense — costs are predictable and you're using BQ constantly anyway. I'd use slot reservations to separate pipeline slots from analyst ad-hoc slots so they don't compete. For dev/test or analyst one-off queries, I'd keep on-demand. Many companies use both: flat-rate for production, on-demand for everything else.

**Q: How do you prevent a badly written query from costing thousands of dollars?**
> Set maximum bytes billed on the job — the query will fail instead of run if it would scan more than the limit. In Python: `QueryJobConfig(maximum_bytes_billed=10 * 1024**3)` for a 10GB cap. For flat-rate: cost is already capped. Also use partition pruning, SELECT specific columns, and educate the team on checking the bytes estimate before hitting Run.

---

# PART 3 — PARTITIONING

## What it is
BigQuery physically divides the table into **separate file groups** by a column's value.
When your WHERE clause filters on the partition column, BQ **skips entire partitions** — they're not read at all.

A 3-year table filtered to 1 day → scans 0.3% of data → 99.7% cost reduction.

---

## Types of Partitioning

```sql
-- 1. By date column (most common)
CREATE TABLE dataset.orders
PARTITION BY DATE(order_time)
AS SELECT * FROM dataset.raw;

-- 2. By integer range
CREATE TABLE dataset.users
PARTITION BY RANGE_BUCKET(age, GENERATE_ARRAY(0, 100, 10));
-- Creates: 0-10, 10-20, 20-30 ... 90-100

-- 3. By ingestion time (no column needed)
CREATE TABLE dataset.events
PARTITION BY _PARTITIONDATE;
```

---

## THE #1 GOTCHA — What breaks partition pruning

Partition pruning = BQ deciding to skip a partition BEFORE running the query.
BQ can only do this if it can read the partition value directly from the WHERE clause.
**Wrapping the column in a function breaks it** — BQ can't evaluate the function before scanning.

```sql
-- ✅ PRUNING WORKS
WHERE DATE(order_time) = '2024-01-15'
WHERE order_time BETWEEN '2024-01-15' AND '2024-01-15 23:59:59'

-- ❌ PRUNING BROKEN — scans ALL partitions, no error shown!
WHERE CAST(order_time AS DATE) = '2024-01-15'
WHERE FORMAT_DATE('%Y-%m-%d', order_time) = '2024-01-15'
WHERE EXTRACT(YEAR FROM order_time) = 2024
```

---

## Adding partitioning to an existing table (CTAS pattern)

You **cannot** add partitioning to an existing table — must recreate it.

```sql
-- Step 1: Create new partitioned table
CREATE TABLE dataset.orders_new
PARTITION BY DATE(order_time)
CLUSTER BY country
AS SELECT * FROM dataset.orders_old;

-- Step 2: Validate (row counts should match)
SELECT COUNT(*) FROM dataset.orders_old;
SELECT COUNT(*) FROM dataset.orders_new;

-- Step 3: Swap names
ALTER TABLE dataset.orders_old RENAME TO orders_backup;
ALTER TABLE dataset.orders_new RENAME TO orders;

-- Step 4: Drop backup once confident
DROP TABLE dataset.orders_backup;
```

## Partition auto-expiry
```sql
-- Auto-delete partitions older than 90 days
OPTIONS (partition_expiration_days = 90)
```

---

## Interview Q&A — Partitioning

**Q: What is partitioning and how does partition pruning work?**
> Partitioning divides a table into physical file groups by a column value — usually a date. When your WHERE clause filters on the partition column, BigQuery reads the partition metadata and skips entire file groups that can't match. A 3-year table queried for one day scans only 0.3% of the data. The critical thing is partition pruning only works if the column appears as-is or wrapped in DATE() — wrapping in CAST or FORMAT_DATE breaks it silently because BQ can't evaluate those functions before scanning.

**Q: Can you add partitioning to an existing table?**
> No — partitioning must be defined at creation time. To add it to an existing table, I'd use CTAS: create a new table with the desired partitioning, validate the row counts match, then rename the tables to swap them. It costs money to copy the data once, but it's a one-time operation.

---

# PART 4 — CLUSTERING

## What it is
Sorts data **within each partition** by up to 4 columns.
BQ reads block-level metadata and skips blocks where values can't match your filter.

Think of it like: partitioning = go to the right drawer, clustering = find the right section within the drawer.

---

## Column order matters — put most-filtered column FIRST

```sql
CLUSTER BY country, product_category, user_id

WHERE country = 'UK'                                    -- ✅ very effective
WHERE country = 'UK' AND product_category = 'elec'     -- ✅ very effective
WHERE product_category = 'elec'                         -- ⚠️ less effective
WHERE user_id = 99                                      -- ❌ not effective alone
```

---

## Clustering can be changed after creation (unlike partitioning)

```sql
ALTER TABLE dataset.orders CLUSTER BY product_category, country;  -- change
ALTER TABLE dataset.orders CLUSTER BY ();                          -- remove
```

---

## Partitioning vs Clustering — comparison

| | Partitioning | Clustering |
|--|-------------|------------|
| Skips | Entire partitions (file groups) | Blocks within a partition |
| Column type | Low cardinality (date) | High cardinality (user_id, country) |
| Max columns | 1 | 4 |
| Can change after? | ❌ No (CTAS needed) | ✅ Yes (ALTER TABLE) |
| Data expiry | ✅ Yes | ❌ No |
| Cost impact | Massive (97%+ reduction) | Significant (additional 60-80%) |

---

## Interview Q&A — Clustering

**Q: When would you use both partitioning and clustering?**
> When you always filter on a date AND one or more other high-cardinality columns. Partition on the date — that prunes whole day partitions. Cluster on country/category/user_id — that prunes blocks within the day's partition. Together they can reduce scan from 100TB to 50GB on a typical daily query. I put the most-commonly-filtered column first in the CLUSTER BY list since BQ can only prune effectively from left to right.

---

# PART 5 — QUERY OPTIMIZATION

## The 100TB cost story (use this in interviews)

```
Unoptimized (SELECT *, no filters):           100 TB = $500/query
After Step 1 — Add partitioning (date filter):  3 TB = $15     (97% saved)
After Step 2 — Add clustering (country filter): 0.6 TB = $3    (80% more)
After Step 3 — SELECT needed columns only:     0.12 TB = $0.60 (80% more)
After Step 4 — Filter before JOIN, use APPROX: 0.05 TB = $0.25 (final)

Total: $500 → $0.25 per run. 99.95% reduction.
```

## All optimization rules

| Rule | Why |
|------|-----|
| Filter on partition column with `DATE(col)` | Partition pruning — skip 99%+ of data |
| SELECT only needed columns | Columnar — only those columns read from disk |
| Filter BEFORE joining | Join operates on smaller data → less shuffle |
| CLUSTER BY on filter columns | Skip blocks within partition |
| `APPROX_COUNT_DISTINCT()` | No shuffle needed — 99% accurate |
| Use materialized views | Pre-computed result — tiny scan |
| Avoid `SELECT *` | Forces reading all columns |
| Push filters into CTEs before JOINs | Reduces data entering shuffle stage |

---

# PART 6 — WINDOW FUNCTIONS

## What they are
Compute aggregations across related rows **without collapsing them** (unlike GROUP BY).
You keep all original rows but get the aggregate value alongside each one.

```sql
-- GROUP BY: 1M rows → 5 rows (one per country)
SELECT country, SUM(revenue) FROM orders GROUP BY country;

-- Window: 1M rows → still 1M rows, but country total on each row
SELECT country, revenue,
  SUM(revenue) OVER (PARTITION BY country) AS country_total
FROM orders;
```

---

## Syntax
```sql
function() OVER (PARTITION BY col  ORDER BY col  ROWS BETWEEN ... AND ...)
              ①              ②               ③            ④

① What to compute    ② Group (like GROUP BY but doesn't collapse)
③ Order within group  ④ Frame — how many rows around you
```

---

## All important window functions

### ROW_NUMBER — unique sequential number, no ties
```sql
-- Most common use: DEDUPLICATION — keep latest record per user
WITH ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) AS rn
  FROM users
)
SELECT * EXCEPT(rn) FROM ranked WHERE rn = 1;
```

### RANK vs DENSE_RANK — when there are ties

```
Scores: 100, 100, 90, 80

ROW_NUMBER:   1,  2,  3,  4   (always unique — no ties)
RANK:         1,  1,  3,  4   (ties share rank, SKIPS next number — like Olympics)
DENSE_RANK:   1,  1,  2,  3   (ties share rank, NO skip — like leaderboards)
```

### LAG / LEAD — access neighbouring rows

```sql
LAG(revenue, 1)    -- value from 1 row BEFORE current row
LAG(revenue, 7)    -- value from 7 rows before (same day last week)
LAG(revenue, 1, 0) -- value from 1 row before, return 0 if no row exists
LEAD(revenue, 1)   -- value from 1 row AFTER current row
```

Example — day-over-day change:
```sql
SELECT date, revenue,
  LAG(revenue) OVER (ORDER BY date) AS prev_day,
  revenue - LAG(revenue) OVER (ORDER BY date) AS daily_change
FROM daily_sales;
```

### Frames — how many rows to include

```sql
-- Running total (default when ORDER BY present)
SUM(revenue) OVER (ORDER BY date)
-- = ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

-- 7-day rolling average
AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)

-- Centred 3-day average
AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
```

---

## Interview Q&A — Window Functions

**Q: Write a query to find top 3 products by revenue per category.**
```sql
WITH ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rn
  FROM products
)
SELECT * EXCEPT(rn) FROM ranked WHERE rn <= 3;
-- Use DENSE_RANK instead if you want ties to be included
```

**Q: What's the difference between RANK and DENSE_RANK?**
> Both give the same rank to tied values. RANK skips the next rank number after a tie (1, 1, 3) — like Olympic medals where two gold means no silver. DENSE_RANK doesn't skip (1, 1, 2) — like video game leaderboards. Use RANK when gaps in ranking are meaningful, DENSE_RANK when you want sequential ranking regardless of ties.

**Q: Why can't you filter on a window function in a WHERE clause?**
> SQL execution order is: FROM → WHERE → GROUP BY → SELECT → ORDER BY. Window functions run during SELECT, but WHERE runs before SELECT — so the window function result doesn't exist yet when WHERE tries to filter it. Solution: wrap in a CTE, compute the window function first, then filter in the outer query.

---

# PART 7 — MERGE (Upsert)

## What it is
Combines INSERT + UPDATE + DELETE in one atomic statement.
Used to sync new/changed records into an existing table without duplicating.

```sql
MERGE dataset.users AS target          -- table to update
USING dataset.users_staging AS source  -- new/changed data
ON target.user_id = source.user_id     -- match condition

WHEN MATCHED AND target.email != source.email THEN
  UPDATE SET target.email = source.email, target.updated_at = source.updated_at

WHEN NOT MATCHED BY TARGET THEN        -- in source but not target → INSERT
  INSERT (user_id, email, created_at)
  VALUES (source.user_id, source.email, source.created_at)

WHEN NOT MATCHED BY SOURCE THEN        -- in target but not source → DELETE (optional)
  DELETE;
```

## MERGE vs DELETE+INSERT

| Scenario | Use |
|----------|-----|
| Individual records changing (don't know which ones) | MERGE |
| Reloading an entire date partition | DELETE + INSERT |
| SCD Type 2 (add new row to preserve history) | MERGE (complex) |

DELETE + INSERT is simpler and faster for partitions — no row-level matching overhead.

---

# PART 8 — STORED PROCEDURES

## What they are
Multi-step SQL logic stored in BigQuery — like a Python function but in SQL.
Supports variables, conditionals, loops, error handling.
Called with `CALL`, NOT used inside SELECT.

```sql
CREATE OR REPLACE PROCEDURE dataset.load_daily(IN run_date DATE)
BEGIN
  DECLARE rows_loaded INT64;   -- variable declaration

  -- Step 1: idempotent delete
  DELETE FROM dataset.summary WHERE summary_date = run_date;

  -- Step 2: insert fresh data
  INSERT INTO dataset.summary
  SELECT run_date, country, COUNT(*), SUM(revenue)
  FROM dataset.orders
  WHERE DATE(order_time) = run_date
  GROUP BY country;

  SET rows_loaded = @@row_count;  -- rows affected by last DML

  -- Step 3: validate
  IF rows_loaded = 0 THEN
    RAISE USING MESSAGE = CONCAT('No data for: ', CAST(run_date AS STRING));
  END IF;
END;

-- How to call it:
CALL dataset.load_daily('2024-01-15');
```

## Key scripting features
```
DECLARE var TYPE;              -- declare variable
SET var = value;               -- assign value
@@row_count                    -- rows affected by last INSERT/UPDATE/DELETE
@@error.message                -- error text (only inside EXCEPTION block)
IF ... THEN ... END IF;        -- conditional
WHILE condition DO ... END WHILE; -- loop
RAISE USING MESSAGE = '...';   -- throw error (like Python's raise Exception)
BEGIN ... EXCEPTION WHEN ERROR THEN ... END;  -- try/except equivalent
```

## Error handling pattern
```sql
BEGIN
  -- your risky code
  CALL dataset.load_daily(run_date);
EXCEPTION WHEN ERROR THEN
  INSERT INTO dataset.error_log VALUES (@@error.message, CURRENT_TIMESTAMP());
  RAISE;  -- re-raise so Airflow marks the task as failed
END;
```

---

## Interview Q&A — Stored Procedures

**Q: What is a stored procedure and when would you use it over writing logic in Python?**
> A stored procedure is reusable SQL logic stored inside BigQuery — with variables, loops, conditionals, and error handling. I'd use it when the pipeline logic is purely SQL — delete a partition, reload it, validate row counts, log results. Putting all that in a stored procedure means Airflow calls one `CALL` statement instead of managing multiple SQL strings in Python. For logic involving Python libraries, API calls, or complex business rules, I'd keep that in Python.

---

# PART 9 — VIEWS, MATERIALIZED VIEWS, UDFs

## View — saved query, zero data stored
```sql
CREATE OR REPLACE VIEW dataset.uk_orders AS
SELECT * FROM dataset.orders WHERE country = 'UK';
```
- Scans full underlying table every time it's queried — no performance benefit
- Always shows live data
- Use for: abstraction, security (hide columns), simplify complex queries

## Materialized View — pre-computed, cached result
```sql
CREATE MATERIALIZED VIEW dataset.mv_daily_revenue AS
SELECT DATE(order_time) AS date, country, COUNT(*), SUM(revenue)
FROM dataset.orders GROUP BY 1, 2;
```
- Physically stores the result, BQ refreshes it ~every 30 minutes
- **BQ automatically uses it even when you query the base table** (transparent rewrite)
- Use for: expensive aggregations queried many times (dashboards, daily summaries)

## UDF (User Defined Function) — reusable formula
```sql
CREATE OR REPLACE FUNCTION dataset.to_gbp(amount FLOAT64)
RETURNS STRING AS (CONCAT('£', FORMAT('%.2f', amount)));

-- Use in SELECT like any built-in function:
SELECT order_id, dataset.to_gbp(revenue) FROM orders;
```
- Returns ONE value per row, used inside SELECT
- Cannot run DML, cannot have complex loops
- Use for: reusable transformations, custom categorisation

## Comparison table
| | View | Materialized View | UDF | Stored Procedure |
|--|------|-------------------|-----|-----------------|
| Data stored | ❌ | ✅ (cached) | ❌ | ❌ |
| Speed | Base table speed | Fast (cached) | Base table speed | N/A |
| Can run DML | ❌ | ❌ | ❌ | ✅ |
| Use in SELECT | ✅ | ✅ | ✅ | ❌ (use CALL) |
| Auto-refresh | Always live | ~30 min | N/A | N/A |

---

# PART 10 — DATA INGESTION

## Method 1: Batch Load from GCS (most common — FREE)
```python
load_job = client.load_table_from_uri(
    'gs://bucket/data/2024-01-15/*.parquet',
    'project.dataset.orders',
    job_config=bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition='WRITE_APPEND',  # WRITE_TRUNCATE or WRITE_EMPTY
        autodetect=True,
    )
)
load_job.result()  # blocks until done
```
✅ Free, handles TB-scale, supports Parquet/CSV/JSON/Avro
❌ Data appears after minutes (not real-time)

## Method 2: Streaming Insert (real-time, costs extra)
```python
errors = client.insert_rows_json('project.dataset.events', rows)
```
✅ Data visible in seconds
❌ Costs ~$0.01/200MB, can't immediately run DML on streamed rows

## Method 3: External Table (query GCS without loading)
```sql
CREATE EXTERNAL TABLE dataset.orders_ext
OPTIONS (format='PARQUET', uris=['gs://bucket/data/*.parquet']);
```
✅ Zero BQ storage cost, instant — data stays in GCS
❌ No partitioning/clustering benefits, slower, no DML allowed

## Method 4: BigQuery Data Transfer Service
- Scheduled imports from Google Ads, Analytics, S3, Salesforce — no code needed

## write_disposition options
```
WRITE_TRUNCATE  → wipe table then load (safe for full reload)
WRITE_APPEND    → add to existing (risk: duplicates if rerun!)
WRITE_EMPTY     → only load if table empty, error otherwise
```

## File format preference
**Always prefer Parquet** — columnar (matches BQ internal format), compressed (5-10x smaller than CSV), self-describing (BQ auto-detects schema). CSV is fine for simple cases but slower and larger.

---

## Interview Q&A — Ingestion

**Q: What's the difference between batch load and streaming insert?**
> Batch load from GCS is free, handles any volume, but data takes minutes to appear and must go through a load job. Streaming insert makes data visible in seconds but costs extra and newly streamed rows can't immediately be updated/deleted. I use batch load for ETL pipelines and streaming only when genuine near-real-time freshness is required — like live dashboards or event tracking.

**Q: When would you use an external table?**
> When I need to occasionally query data in GCS without the cost or complexity of loading it into BigQuery — for example, querying archive files I only need to analyse once, or data I don't control. For anything queried regularly, a native BQ table with proper partitioning is much faster.

---

# PART 11 — TIME TRAVEL (Rollback bad loads)

BigQuery keeps **7 days of previous versions** automatically.

```sql
-- Query table as it was 2 hours ago
SELECT * FROM dataset.orders
FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR);

-- Restore table after a bad load
CREATE OR REPLACE TABLE dataset.orders AS
SELECT * FROM dataset.orders
FOR SYSTEM_TIME AS OF '2024-01-15 09:00:00';

-- Restore just one partition
DELETE FROM dataset.orders WHERE event_date = '2024-01-15';
INSERT INTO dataset.orders
SELECT * FROM dataset.orders
FOR SYSTEM_TIME AS OF '2024-01-15 06:00:00'
WHERE event_date = '2024-01-15';
```

**Interview answer:** *"If a bad load happens, I use BigQuery's time travel — it keeps 7 days of previous table versions. I restore with CREATE OR REPLACE TABLE ... FOR SYSTEM_TIME AS OF before the bad load happened. I also keep the raw GCS files as a permanent backup in case I need to reload beyond 7 days."*

---

# PART 12 — INFORMATION_SCHEMA (Debug & Audit)

```sql
-- Find expensive queries (last 7 days) — use this to audit costs
SELECT user_email,
  ROUND(total_bytes_billed/1e9, 2) AS gb_billed,
  ROUND(total_bytes_billed/1e12 * 5, 2) AS est_cost_usd,
  query
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY total_bytes_billed DESC LIMIT 20;

-- Check which partitions exist and their row counts
SELECT partition_id, row_count, last_modified_time
FROM dataset.INFORMATION_SCHEMA.PARTITIONS
WHERE table_name = 'orders' ORDER BY partition_id DESC;

-- List tables with sizes
SELECT table_name, row_count, ROUND(size_bytes/1e9, 2) AS size_gb
FROM dataset.INFORMATION_SCHEMA.TABLES;

-- List columns of a table
SELECT column_name, data_type, is_nullable
FROM dataset.INFORMATION_SCHEMA.COLUMNS
WHERE table_name = 'orders';
```

---

# PART 13 — ARRAYS & STRUCTS (Nested Data)

BigQuery supports nested data natively — common in JSON/event data.

**STRUCT** = a row within a row (nested object)
**ARRAY** = repeated values (a list)

```sql
-- Table: orders with line_items as ARRAY of STRUCT
-- UNNEST expands array into rows
SELECT
  o.order_id,
  o.customer.name,          -- access STRUCT field with dot notation
  item.product_id,
  item.quantity
FROM orders o,
UNNEST(o.line_items) AS item  -- each item becomes its own row

-- Array aggregation
SELECT user_id,
  ARRAY_AGG(product_id ORDER BY purchase_date) AS purchased_products
FROM purchases GROUP BY user_id;
```

**Why use them?** Avoids expensive JOINs for hierarchical data. One row can contain all related records (e.g. an order with all its line items).

---

# PART 14 — DML LIMITATIONS

Things that catch people out:

```
❌ Cannot UPDATE/DELETE/MERGE on streaming buffer rows (wait ~90 min)
❌ Cannot change partition column after creation
❌ Cannot add partitioning to existing table (CTAS required)
❌ Cannot change column data type directly (add new col + backfill)
❌ SELECT * in views is not safe — if base table adds column, view breaks
✅ Can add new columns with ALTER TABLE ADD COLUMN
✅ Can drop NULLABLE columns with ALTER TABLE DROP COLUMN
✅ Can change clustering with ALTER TABLE CLUSTER BY
```

---

# PART 15 — SCHEMA EVOLUTION

```sql
-- Safely add a new column (backwards compatible)
ALTER TABLE dataset.orders ADD COLUMN discount FLOAT64;

-- Change data type (NOT directly supported — workaround):
ALTER TABLE dataset.orders ADD COLUMN user_id_str STRING;
UPDATE dataset.orders SET user_id_str = CAST(user_id AS STRING) WHERE TRUE;
ALTER TABLE dataset.orders DROP COLUMN user_id;

-- Relax NOT NULL constraint
ALTER TABLE dataset.orders ALTER COLUMN revenue DROP NOT NULL;
```

**In production:** Always use explicit schemas in load jobs, not autodetect — autodetect can misread IDs as integers, booleans as strings, etc.

---

# KEY ANSWERS — BigQuery (Read before interview, no questions listed)

## BigQuery vs Traditional Database
BigQuery is a serverless, columnar OLAP data warehouse — built for massive analytical queries on billions of rows. Traditional databases (Postgres, MySQL) are OLTP — built for many small fast reads/writes for app backends. BigQuery has no indexes, no fixed servers, charges per byte scanned, and scales automatically. You'd never use BQ for an app backend, and you'd never use Postgres to aggregate 1 billion rows.

---

## What happens when a query runs
Dremel (query engine) creates an execution plan. Thousands of leaf workers spin up and read data **in parallel** — reading only the columns you selected from only the partitions your WHERE clause matches. They do partial aggregation and shuffle results to mixer workers which merge and aggregate. A root worker does the final sort and returns results. **You're billed only for bytes read in the leaf stage.**

---

## Partition pruning — and what silently breaks it
Before scanning, BQ reads partition metadata and skips partitions that can't match your WHERE clause. This only works if BQ can evaluate the filter value **before** running the query. Wrapping the partition column in `CAST()`, `FORMAT_DATE()`, or `EXTRACT()` breaks it because BQ can't evaluate those functions early — it has to scan everything first.
- ✅ Works: `WHERE DATE(order_time) = '2024-01-15'`
- ❌ Broken: `WHERE CAST(order_time AS DATE) = '2024-01-15'`

---

## Partitioning vs Clustering
**Partitioning** divides the table into separate file groups (by date) — BQ skips entire partitions that don't match. Biggest cost saving (can reduce 100TB to 3TB for a single day's query).
**Clustering** sorts data within each partition by columns — BQ skips blocks where values can't match. Secondary saving on top of partitioning.
- Together: 100TB → 3TB (partition) → 0.6TB (clustering)
- Column order in clustering matters: most-filtered column goes first
- Partitioning cannot be changed after creation; clustering can (ALTER TABLE)

---

## Optimizing a slow query — the 100TB story
Start: `SELECT *`, no filters → 100TB = $500/run
1. Partition by date, filter with `DATE(col)` → 3TB = $15 (97% less)
2. Cluster by country, filter by country → 0.6TB = $3 (80% more)
3. SELECT only needed columns → 0.12TB = $0.60 (80% more)
4. Filter before JOIN, use APPROX functions → 0.05TB = $0.25 (final)
Result: $500 → $0.25 per run. 99.95% reduction.

---

## On-demand vs Flat-rate
- **On-demand:** $5/TB scanned. Pay nothing when idle. Unpredictable bills. Good for low/variable usage.
- **Flat-rate:** Fixed monthly fee for reserved slots. Same cost whether you scan 1GB or 1PB. Good for constant high-volume pipelines.
- **Decision:** If spending > ~$2K/month on-demand → flat-rate likely saves money. Use **slot reservations** to divide slots between teams (pipelines vs analysts) — without this they compete for the same pool.
- **Best practice:** Flat-rate for production Airflow pipelines, on-demand for analyst ad-hoc queries.

---

## APPROX_COUNT_DISTINCT
Approximate version of `COUNT(DISTINCT col)` — 99% accurate. Uses HyperLogLog algorithm which maintains a tiny sketch per worker instead of shuffling all distinct values across the network. 10-100x cheaper and faster on large datasets. Use for dashboards and analytics. Do NOT use for billing, financial reporting, or anything needing exact counts.

---

## Top-N per group — the pattern (comes up constantly)
```sql
WITH ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rn
  FROM products
)
SELECT * EXCEPT(rn) FROM ranked WHERE rn <= 3;
-- Use DENSE_RANK instead of ROW_NUMBER if you want tied values both included
```
Cannot use window function in WHERE clause directly — window functions run in SELECT, WHERE runs before SELECT. Wrap in CTE first.

---

## RANK vs DENSE_RANK
Both assign same rank to tied values.
- **RANK:** skips next number after a tie. Scores 100,100,90 → ranks 1,1,3. Like Olympics — two gold means no silver.
- **DENSE_RANK:** never skips. Scores 100,100,90 → ranks 1,1,2. Like leaderboards.
Use RANK when gaps are meaningful. Use DENSE_RANK when you need sequential numbering.

---

## MERGE vs DELETE+INSERT
**MERGE** = INSERT + UPDATE + DELETE in one atomic statement. Use when syncing individual changed records where you don't know which rows changed (e.g. users table — any user could have updated).
**DELETE+INSERT** = wipe a partition and reload fresh data. Use when reloading an entire time partition. Simpler and faster — no row-level matching overhead.
Both are idempotent — safe to rerun.

---

## Stored Procedure — daily load pattern
```sql
CREATE OR REPLACE PROCEDURE dataset.load_daily(IN run_date DATE)
BEGIN
  DECLARE rows_loaded INT64;
  DELETE FROM dataset.summary WHERE summary_date = run_date;   -- idempotent
  INSERT INTO dataset.summary
  SELECT run_date, country, COUNT(*), SUM(revenue)
  FROM dataset.orders WHERE DATE(order_time) = run_date GROUP BY country;
  SET rows_loaded = @@row_count;    -- rows affected by last DML
  IF rows_loaded = 0 THEN
    RAISE USING MESSAGE = CONCAT('No data for: ', CAST(run_date AS STRING));
  END IF;
END;
CALL dataset.load_daily('2024-01-15');
```
Use stored procedures when pipeline logic is purely SQL steps in sequence. Airflow calls one `CALL` instead of managing multiple SQL strings. For Python libraries, API calls, or complex logic — keep that in Python.

---

## View vs Materialized View vs UDF
- **View:** saved query, no data stored, scans full base table every time. Use for abstraction and security (restricting columns).
- **Materialized View:** physically stores the pre-computed result. BQ auto-refreshes (~30 min) and **transparently rewrites queries to use it** — even if you query the base table. Use for expensive aggregations queried many times (dashboards, daily summaries).
- **UDF:** custom function returning one value per row, used inside SELECT. Cannot run DML. Use for reusable transformations, formatting, categorisation.

---

## Loading data from GCS into BigQuery
```python
load_job = client.load_table_from_uri(
    'gs://bucket/data/*.parquet',
    'project.dataset.table',
    job_config=bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition='WRITE_TRUNCATE',  # full reload
        autodetect=True,
    )
)
load_job.result()  # wait for completion
```
Loading is **free**. Prefer Parquet — columnar, compressed (5-10x smaller than CSV), self-describing.
- `WRITE_TRUNCATE` = wipe then load (safe for full reload)
- `WRITE_APPEND` = add to existing (risk: duplicates if rerun!)
- `WRITE_EMPTY` = only if table is empty

---

## External Table
A table definition pointing to GCS files. BQ reads directly from GCS at query time — data never moves into BigQuery. Zero BQ storage cost, instant setup. But: no partitioning/clustering benefits, slower than native tables, no DML (INSERT/UPDATE/DELETE) allowed. Use for occasional archive queries or data you don't control.

---

## Rolling back a bad load — Time Travel
BigQuery keeps 7 days of previous table versions automatically.
```sql
-- Restore entire table to before the bad load
CREATE OR REPLACE TABLE dataset.orders AS
SELECT * FROM dataset.orders
FOR SYSTEM_TIME AS OF '2024-01-15 09:00:00';  -- timestamp before the bad load
```
Also keep raw GCS files permanently — if bad load happened > 7 days ago, reload from GCS.

---

## Adding partitioning to existing table — CTAS pattern
Cannot add partitioning to existing table. Must recreate:
```sql
CREATE TABLE dataset.orders_new
PARTITION BY DATE(order_time) CLUSTER BY country
AS SELECT * FROM dataset.orders_old;
-- Validate: both tables should have same COUNT(*)
ALTER TABLE dataset.orders_old RENAME TO orders_backup;
ALTER TABLE dataset.orders_new RENAME TO orders;
DROP TABLE dataset.orders_backup;
```

---

## @@row_count in stored procedures
System variable that holds the number of rows affected by the **last** INSERT, UPDATE, DELETE, or MERGE statement. Read it immediately after DML — it resets on the next statement.
Use it to validate: if `@@row_count = 0` after an INSERT, no data was loaded — raise an error.

---

## Monitoring query costs — INFORMATION_SCHEMA
```sql
SELECT user_email,
  ROUND(total_bytes_billed/1e9, 2) AS gb_billed,
  ROUND(total_bytes_billed/1e12 * 5, 2) AS est_cost_usd,
  query
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY total_bytes_billed DESC LIMIT 20;
```
Also use the Explain button in BQ console to see the query execution plan and identify which stage is the bottleneck.

---

## Preferred file format for BQ loads — Parquet
Parquet is columnar (matches BQ's internal storage format — no conversion needed), compressed (5-10x smaller than CSV — faster to upload, less GCS storage cost), and self-describing (BQ auto-detects schema — no need to define it). CSV is acceptable for simple cases but larger, slower, and requires schema definition. Always use Parquet for production pipelines.

