# BigQuery - Most Asked Interview Questions & Answers

---

## Q1. What is BigQuery and how does it differ from a traditional database?

**Answer:**
BigQuery is Google Cloud's fully managed, serverless, columnar data warehouse designed for large-scale analytics. Key differences:

| Feature | Traditional DB (Postgres/MySQL) | BigQuery |
|---------|----------------------------------|----------|
| Purpose | OLTP (transactional) | OLAP (analytical) |
| Storage | Row-based | Columnar |
| Scaling | Manual (add nodes) | Automatic / serverless |
| Indexing | Indexes required | No indexes — partitioning/clustering |
| Transactions | Full ACID support | Limited (scripting transactions) |
| Cost | Fixed server cost | Pay per bytes scanned |
| Best for | Many small reads/writes | Few massive analytical reads |

BigQuery separates storage (Colossus) from compute (Dremel engine), which allows it to scale each independently.

---

## Q2. What is the difference between Partitioning and Clustering in BigQuery? When would you use both?

**Answer:**

### Partitioning
- Divides a table into segments based on a column value
- When you query with a filter on the partition column, BigQuery **skips entire partitions** that don't match — reducing bytes scanned and cost
- Supports: DATE, TIMESTAMP, INTEGER RANGE, or ingestion time
- Max 4,000 partitions per table

### Clustering
- Sorts data **within** each partition by up to 4 columns
- Doesn't eliminate data like partitioning does, but reduces bytes scanned when filtering on clustered columns
- Works best on **high-cardinality** columns (user_id, product_id, country)

### When to use both together:
```sql
CREATE TABLE analytics.events
PARTITION BY DATE(event_time)         -- prune whole days
CLUSTER BY user_id, event_type        -- within each day, sorted by user
AS SELECT * FROM raw.events;
```
You query like:
```sql
-- This scans minimum data: partition prunes dates, clustering prunes user chunks
WHERE DATE(event_time) = '2024-01-15' AND user_id = 'user_123'
```

**Rule of thumb:** Partition on the date/time column you always filter by. Cluster on the high-cardinality columns you frequently filter or join on.

---

## Q3. How do you optimize a slow BigQuery query?

**Answer:**

Step-by-step approach:

**1. Check the query plan first**
- Click "Explain" in BQ UI → look at which stage is consuming most time
- Look for: large input rows, heavy shuffle (repartitioning), or skewed data

**2. Ensure partition pruning is working**
```sql
-- BAD: function on partition column defeats pruning
WHERE CAST(event_time AS DATE) = '2024-01-15'

-- GOOD: BigQuery can prune partitions
WHERE DATE(event_time) = '2024-01-15'
```

**3. Select only needed columns**
```sql
-- BAD: scans all columns
SELECT * FROM events

-- GOOD: scans only 2 columns
SELECT user_id, event_type FROM events
```

**4. Filter before joining**
```sql
-- GOOD: filter inside CTE first, then join smaller result
WITH filtered AS (
  SELECT * FROM events WHERE DATE(event_time) = '2024-01-15'
)
SELECT f.*, u.name FROM filtered f JOIN users u ON f.user_id = u.id
```

**5. Avoid data skew in GROUP BY / JOIN**
- If one key has millions of rows, that reducer becomes a bottleneck
- Use approximate functions: `APPROX_COUNT_DISTINCT()` instead of `COUNT(DISTINCT)`

**6. Use materialized views or intermediate tables** for repeated heavy queries

**7. Check if clustering is helping** using `INFORMATION_SCHEMA.JOBS`

---

## Q4. How do you implement an upsert (insert or update) in BigQuery?

**Answer:**
BigQuery doesn't have traditional upsert. You use `MERGE`:

```sql
MERGE `project.dataset.target_table` AS T
USING `project.dataset.source_table` AS S
ON T.user_id = S.user_id

WHEN MATCHED AND T.updated_at < S.updated_at THEN
  -- Row exists in target and source has newer version → UPDATE
  UPDATE SET
    T.email = S.email,
    T.name = S.name,
    T.updated_at = S.updated_at

WHEN NOT MATCHED BY TARGET THEN
  -- Row exists in source but not target → INSERT
  INSERT (user_id, email, name, created_at, updated_at)
  VALUES (S.user_id, S.email, S.name, S.created_at, S.updated_at)

WHEN NOT MATCHED BY SOURCE THEN
  -- Row exists in target but not source → optionally DELETE
  DELETE;
```

**Common patterns:**
- `WRITE_TRUNCATE` → full reload (simple but costly for big tables)
- `MERGE` → incremental upsert (efficient, preserves history)
- `DELETE + INSERT` → delete partition then reload (idempotent, simpler than MERGE)

---

## Q5. Explain window functions. Give examples of ROW_NUMBER, RANK, DENSE_RANK, LAG/LEAD.

**Answer:**

Window functions compute a result **across a set of rows related to the current row** without collapsing them into a single group (unlike GROUP BY).

Syntax: `function() OVER (PARTITION BY col1 ORDER BY col2 [frame])`

### ROW_NUMBER vs RANK vs DENSE_RANK

Given this data: scores = [100, 100, 90, 80]

| score | ROW_NUMBER | RANK | DENSE_RANK |
|-------|-----------|------|------------|
| 100 | 1 | 1 | 1 |
| 100 | 2 | 1 | 1 |
| 90 | 3 | 3 | 2 |
| 80 | 4 | 4 | 3 |

- **ROW_NUMBER**: always unique, no ties
- **RANK**: ties get same rank, next rank **skips** (1,1,3)
- **DENSE_RANK**: ties get same rank, next rank **does not skip** (1,1,2)

```sql
-- Deduplicate: keep latest record per user
WITH ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) AS rn
  FROM users
)
SELECT * EXCEPT(rn) FROM ranked WHERE rn = 1;
```

### LAG / LEAD (compare to previous/next row)
```sql
SELECT
  date,
  revenue,
  LAG(revenue, 1) OVER (ORDER BY date) AS prev_day_revenue,
  LEAD(revenue, 1) OVER (ORDER BY date) AS next_day_revenue,
  revenue - LAG(revenue, 1) OVER (ORDER BY date) AS day_over_day_change
FROM daily_sales;
```

### Running/Moving aggregates
```sql
SELECT
  date,
  revenue,
  SUM(revenue) OVER (ORDER BY date) AS cumulative_total,
  AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_7d_avg
FROM daily_sales;
```

---

## Q6. How do nested and repeated fields (ARRAY, STRUCT) work in BigQuery?

**Answer:**

BigQuery supports nested data natively, which is common in JSON/event data.

- **STRUCT**: like a row within a row (nested object)
- **ARRAY**: repeated values (list of items)

```sql
-- Example schema: orders with line items
-- order_id | customer | line_items (ARRAY of STRUCT)

-- UNNEST expands array into rows
SELECT
  o.order_id,
  o.customer.name,         -- access STRUCT field
  item.product_id,
  item.quantity,
  item.price
FROM orders o,
UNNEST(o.line_items) AS item    -- each item becomes a separate row
WHERE item.price > 50;

-- Aggregate back: count items per order
SELECT
  order_id,
  ARRAY_LENGTH(line_items) AS item_count,
  (SELECT SUM(i.price) FROM UNNEST(line_items) i) AS total_value
FROM orders;
```

**Why use them?** Avoids expensive JOINs for hierarchical data. A single row can contain all related data (e.g., a user with all their events).

---

## Q7. How do you control BigQuery query costs?

**Answer:**

**1. Partitioning** — most impactful. Partition on date → only relevant partitions scanned.

**2. Clustering** — reduces bytes within partitions.

**3. Column selection** — BQ is columnar, only scans columns you SELECT.

**4. Set maximum bytes billed**
```python
job_config = bigquery.QueryJobConfig(maximum_bytes_billed=10 * 1024**3)  # 10GB limit
```
Query fails if it would scan more than the limit — prevents runaway queries.

**5. Use materialized views** — BQ automatically uses them to serve queries that match, reducing scan.

**6. Audit with INFORMATION_SCHEMA**
```sql
SELECT user_email, total_bytes_billed/1e9 AS gb_billed, query
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY total_bytes_billed DESC LIMIT 20;
```

**7. Flat-rate / reservations** — for predictable, high-volume workloads, buy slots (no per-query charges).

**8. Table expiration / partition expiration** — auto-delete old data you no longer need.

---

## Q8. What is a BigQuery stored procedure and how do you write one?

**Answer:**

A stored procedure is reusable SQL logic stored in BigQuery with support for variables, control flow (IF/WHILE/FOR), and error handling. Unlike views, they execute statements (DML, DDL) rather than just return data.

```sql
CREATE OR REPLACE PROCEDURE dataset.load_daily_summary(IN run_date DATE)
BEGIN
  DECLARE rows_loaded INT64;

  -- Delete existing data for this date (idempotent)
  DELETE FROM dataset.daily_summary WHERE summary_date = run_date;

  -- Insert fresh aggregation
  INSERT INTO dataset.daily_summary (summary_date, total_events, total_revenue)
  SELECT
    run_date,
    COUNT(*) AS total_events,
    SUM(revenue) AS total_revenue
  FROM dataset.events
  WHERE DATE(event_time) = run_date;

  SET rows_loaded = @@row_count;

  -- Validate
  IF rows_loaded = 0 THEN
    RAISE USING MESSAGE = CONCAT('No data for date: ', CAST(run_date AS STRING));
  END IF;

  SELECT CONCAT('Loaded ', CAST(rows_loaded AS STRING), ' rows') AS result;
END;

-- Call it:
CALL dataset.load_daily_summary('2024-01-15');
```

**Key features:**
- `DECLARE` — declare variables
- `SET` — assign values
- `@@row_count` — rows affected by last DML
- `IF/ELSEIF/ELSE/END IF` — conditionals
- `WHILE/LOOP` — loops
- `EXCEPTION WHEN ERROR THEN` — error handling
- `RAISE` — throw errors

---

## Q9. What is INFORMATION_SCHEMA in BigQuery and how do you use it?

**Answer:**

`INFORMATION_SCHEMA` is a set of views that expose metadata about your BigQuery resources — tables, columns, jobs, partitions, etc.

```sql
-- List all tables in a dataset
SELECT table_name, row_count, size_bytes/1e9 AS size_gb, creation_time
FROM dataset.INFORMATION_SCHEMA.TABLES;

-- List all columns for a table
SELECT column_name, data_type, is_nullable
FROM dataset.INFORMATION_SCHEMA.COLUMNS
WHERE table_name = 'events';

-- Find expensive queries in last 7 days
SELECT
  user_email,
  total_bytes_billed / 1e9 AS gb_billed,
  ROUND(total_bytes_billed / 1e12 * 5, 4) AS estimated_cost_usd,
  query
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND state = 'DONE'
ORDER BY total_bytes_billed DESC LIMIT 20;

-- Check partition info
SELECT partition_id, row_count, last_modified_time
FROM dataset.INFORMATION_SCHEMA.PARTITIONS
WHERE table_name = 'events'
ORDER BY partition_id DESC LIMIT 10;
```

---

## Q10. How do you load data into BigQuery? What formats does it support?

**Answer:**

**Supported formats:** CSV, JSON (newline delimited), Avro, Parquet, ORC, Datastore exports

**Methods:**

1. **Load from GCS** (most common for bulk loads)
```python
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    write_disposition='WRITE_APPEND',
    autodetect=True,
)
load_job = client.load_table_from_uri(
    'gs://my-bucket/data/2024-01-15/*.parquet',
    'project.dataset.table',
    job_config=job_config
)
load_job.result()
```

2. **Streaming insert** (real-time, row by row or small batches)
```python
errors = client.insert_rows_json('project.dataset.table', rows)
```
⚠️ Streaming inserts cost more and data isn't immediately available for DML operations.

3. **Load from DataFrame** (via Python client)
```python
client.load_table_from_dataframe(df, 'project.dataset.table', job_config=...).result()
```

4. **BigQuery Data Transfer Service** — scheduled imports from SaaS sources (Google Ads, S3, etc.)

5. **LOAD DATA statement** (SQL-based load from GCS)
```sql
LOAD DATA INTO dataset.table
FROM FILES (format='CSV', uris=['gs://bucket/data/*.csv']);
```

---

## Q11. What happens when you run a query on an unpartitioned 10TB table? How would you fix it?

**Answer:**

Without partitioning, BigQuery does a **full table scan** — reads all 10TB every time. At $5/TB, that's **$50 per query**.

**Fix:**
1. **Create a new partitioned table:**
```sql
CREATE TABLE dataset.events_partitioned
PARTITION BY DATE(event_time)
CLUSTER BY user_id
AS SELECT * FROM dataset.events_old;
```

2. **Or use `bq` CLI to recreate with partitioning:**
```bash
bq mk --table --time_partitioning_field=event_time \
  project:dataset.events_partitioned schema.json
bq cp --append_table dataset.events_old dataset.events_partitioned
```

3. **Add clustering** on top for the columns frequently used in WHERE/JOIN.

4. **Short-term:** Add a `WHERE DATE(event_time) BETWEEN ...` filter manually to limit scan until the table is restructured.

---

## Q12. What is a materialized view in BigQuery?

**Answer:**

A materialized view is a **precomputed, stored result** of a query that BigQuery automatically keeps fresh and uses to serve queries faster.

```sql
CREATE MATERIALIZED VIEW dataset.mv_daily_user_events
AS
SELECT
  DATE(event_time) AS event_date,
  user_id,
  COUNT(*) AS event_count,
  SUM(revenue) AS total_revenue
FROM dataset.raw_events
GROUP BY 1, 2;
```

**Key properties:**
- BigQuery **auto-refreshes** it when base table changes (within 30 min by default)
- BigQuery **transparently rewrites** queries that match the MV pattern — even if you query the base table directly
- Significantly reduces cost for repeated aggregation queries
- Best for heavy GROUP BY on large tables

---

## Q13. What is the difference between a VIEW and a TABLE in BigQuery?

**Answer:**

| | Table | View | Materialized View |
|--|-------|------|-------------------|
| Data stored | Yes | No | Yes (cached) |
| Query cost | Scan stored data | Scan underlying tables | Scan cached result |
| Auto-refresh | N/A | Always live | Periodic |
| DML allowed | Yes | No | No |
| Use case | Permanent data | Logical abstraction | Repeated heavy aggregations |

Views are purely logical — every time you query a view, BigQuery expands it and runs the underlying query.

---

## Q14. How do you handle NULL values in BigQuery?

**Answer:**

```sql
-- Check for NULL
SELECT * FROM table WHERE col IS NULL;
SELECT * FROM table WHERE col IS NOT NULL;

-- Replace NULL with default
SELECT IFNULL(revenue, 0) AS revenue FROM orders;
SELECT COALESCE(address, city, 'Unknown') AS location FROM users;  -- returns first non-null

-- NULL in aggregations: NULL is ignored by SUM, COUNT, AVG
SELECT AVG(revenue) FROM orders;  -- NULLs not counted in average

-- NULL in comparisons: always use IS NULL, not = NULL
-- This NEVER matches: WHERE col = NULL
-- This works:          WHERE col IS NULL

-- NULLIF: returns NULL if two values are equal (useful to avoid divide by zero)
SELECT revenue / NULLIF(impressions, 0) AS ctr FROM ads;
```

---

## Q15. What is the difference between standard SQL and legacy SQL in BigQuery?

**Answer:**

- **Legacy SQL**: BigQuery's old proprietary SQL dialect (uses `[project:dataset.table]` syntax, `TABLE_DATE_RANGE`, etc.)
- **Standard SQL**: ANSI-compliant SQL (uses backticks `` `project.dataset.table` ``)

**Always use Standard SQL.** Legacy SQL is deprecated. Standard SQL supports:
- CTEs (`WITH` clauses)
- Window functions
- ARRAY/STRUCT types
- DML (INSERT, UPDATE, DELETE, MERGE)
- DDL (CREATE, ALTER, DROP)
- Scripting (variables, loops, stored procedures)

Set in Python:
```python
job_config = bigquery.QueryJobConfig(use_legacy_sql=False)  # standard SQL (default)
```

---

## Q16. How do you handle schema evolution in BigQuery (adding/changing columns)?

**Answer:**

**Adding a column (safe — backwards compatible):**
```sql
ALTER TABLE dataset.events ADD COLUMN new_col STRING;
-- Or in Python:
table = client.get_table('project.dataset.events')
table.schema = table.schema + [bigquery.SchemaField("new_col", "STRING")]
client.update_table(table, ["schema"])
```

**Relaxing NOT NULL → NULLABLE (safe):**
```sql
ALTER TABLE dataset.events ALTER COLUMN col DROP NOT NULL;
```

**Changing data type (NOT directly supported):**
You cannot change INT to STRING directly. Workarounds:
1. Add a new column with the correct type
2. Backfill it: `UPDATE table SET new_col = CAST(old_col AS STRING) WHERE TRUE`
3. Drop old column (only if it's NULLABLE and no dependencies)

**Deleting a column:**
```sql
ALTER TABLE dataset.events DROP COLUMN old_col;
-- Only works if column is NULLABLE
```

---

## Q17. What causes data skew in BigQuery and how do you fix it?

**Answer:**

**Data skew** = one key in a GROUP BY or JOIN has significantly more rows than others, causing one worker to do all the work while others idle.

**Example:** Joining on `country_code` where 80% of rows are 'US'.

**Symptoms:** Query plan shows one stage taking much longer; one slot at 100% while others idle.

**Fixes:**
1. **Filter before join:** reduce the skewed dataset first
2. **Use approximate functions:** `APPROX_COUNT_DISTINCT()` instead of `COUNT(DISTINCT)`
3. **Split into multiple queries:** handle the dominant key separately
4. **Add salt/randomness to join key** (advanced — splits one key into N sub-groups)

```sql
-- Workaround: separate the dominant key
-- Query for 'US' separately (optimized)
SELECT ... WHERE country = 'US' GROUP BY ...
UNION ALL
-- Query for all others
SELECT ... WHERE country != 'US' GROUP BY ...
```
