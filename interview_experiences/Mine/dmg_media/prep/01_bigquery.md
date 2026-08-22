# BigQuery - Interview Prep

---

## 1. Core Architecture

- **Serverless** columnar data warehouse (no infrastructure management)
- Separation of **compute** (Dremel) and **storage** (Colossus)
- Data stored in **Capacitor** format (columnar, compressed)
- Queries billed by **bytes processed** (not compute time)

---

## 2. Partitioning vs Clustering

### Partitioning
- Divides table into segments (pruning at read time = less data scanned)
- Types:
  - **Ingestion-time** (`_PARTITIONTIME`)
  - **Column-based**: DATE, TIMESTAMP, INTEGER RANGE
- Max **4000 partitions** per table
- Use when filtering on a **single column** frequently

```sql
CREATE TABLE dataset.events
PARTITION BY DATE(event_date)
AS SELECT * FROM dataset.raw_events;
```

### Clustering
- Sorts data within partitions by up to **4 columns**
- Reduces bytes scanned when filtering/joining on clustered columns
- Good for **high-cardinality** columns

```sql
CREATE TABLE dataset.events
PARTITION BY DATE(event_date)
CLUSTER BY user_id, event_type
AS SELECT * FROM dataset.raw_events;
```

### When to use which?
| Scenario | Use |
|----------|-----|
| Filter on date range | Partitioning |
| Filter on user_id or category | Clustering |
| Large table with multi-column filters | Both |
| Table < 1GB | Neither (overhead not worth it) |

---

## 3. Query Optimization

- **Always filter on partition column first**
- Avoid `SELECT *` — select only needed columns
- Use `APPROX_COUNT_DISTINCT()` instead of `COUNT(DISTINCT)` for large datasets
- Push filters **before** JOINs
- Use **materialized views** for repeated expensive queries
- Avoid cross joins / cartesian products
- Use `EXPLAIN` (Query plan) to understand execution

```sql
-- Bad
SELECT * FROM huge_table WHERE CAST(created_at AS DATE) = '2024-01-01'

-- Good (partition pruning works)
SELECT id, name FROM huge_table WHERE DATE(created_at) = '2024-01-01'
```

---

## 4. Window Functions

```sql
-- ROW_NUMBER - rank per partition
SELECT
  user_id,
  event_date,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_date DESC) AS rn
FROM events

-- Running total
SELECT
  date,
  revenue,
  SUM(revenue) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_revenue
FROM sales

-- LAG / LEAD - previous/next row value
SELECT
  date,
  revenue,
  LAG(revenue, 1) OVER (ORDER BY date) AS prev_revenue,
  revenue - LAG(revenue, 1) OVER (ORDER BY date) AS delta
FROM sales
```

---

## 5. Nested & Repeated Fields (STRUCT / ARRAY)

```sql
-- UNNEST an array
SELECT user_id, tag
FROM users, UNNEST(tags) AS tag

-- Access STRUCT fields
SELECT order.customer.name, order.total
FROM orders

-- Array aggregation
SELECT
  user_id,
  ARRAY_AGG(product_id ORDER BY purchase_date) AS purchased_products
FROM purchases
GROUP BY user_id
```

---

## 6. DML Operations

```sql
-- MERGE (upsert)
MERGE dataset.target T
USING dataset.source S
ON T.id = S.id
WHEN MATCHED THEN
  UPDATE SET T.value = S.value, T.updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
  INSERT (id, value, created_at) VALUES (S.id, S.value, CURRENT_TIMESTAMP())
WHEN NOT MATCHED BY SOURCE THEN
  DELETE;

-- DELETE with subquery
DELETE FROM dataset.events
WHERE event_id IN (SELECT event_id FROM dataset.duplicate_events);
```

---

## 7. Stored Procedures / Scripting in BigQuery

```sql
-- Basic stored procedure
CREATE OR REPLACE PROCEDURE dataset.update_summary(IN run_date DATE)
BEGIN
  DECLARE row_count INT64;

  DELETE FROM dataset.summary WHERE summary_date = run_date;

  INSERT INTO dataset.summary
  SELECT
    DATE(event_date) AS summary_date,
    COUNT(*) AS total_events,
    SUM(revenue) AS total_revenue
  FROM dataset.events
  WHERE DATE(event_date) = run_date;

  SET row_count = @@row_count;
  SELECT CONCAT('Inserted ', CAST(row_count AS STRING), ' rows') AS status;
END;

-- Call it
CALL dataset.update_summary('2024-01-15');
```

### Control Flow
```sql
-- IF / ELSE
IF condition THEN
  -- statements
ELSEIF other_condition THEN
  -- statements
ELSE
  -- statements
END IF;

-- LOOP / WHILE
SET counter = 0;
LOOP
  SET counter = counter + 1;
  IF counter >= 10 THEN LEAVE; END IF;
END LOOP;

-- FOR LOOP (over query results)
FOR row IN (SELECT date FROM calendar WHERE year = 2024) DO
  CALL dataset.process_date(row.date);
END FOR;
```

### Exception Handling
```sql
BEGIN
  -- risky operation
  INSERT INTO ...
EXCEPTION WHEN ERROR THEN
  -- handle error
  INSERT INTO dataset.error_log VALUES (@@error.message, CURRENT_TIMESTAMP());
END;
```

---

## 8. BigQuery Cost Control

- **Slot-based pricing**: Pay for reserved slots (flat-rate)
- **On-demand pricing**: Pay per byte scanned
- Use **partitioning** to reduce bytes scanned
- Use `INFORMATION_SCHEMA.JOBS` to audit query costs
- Set **maximum bytes billed** to prevent runaway queries

```sql
-- Check bytes billed for recent queries
SELECT
  job_id,
  user_email,
  total_bytes_billed / POW(10,9) AS gb_billed,
  query
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY total_bytes_billed DESC
LIMIT 20;
```

---

## 9. Common Gotchas

| Issue | Solution |
|-------|----------|
| NULL handling | Use `IFNULL()`, `COALESCE()`, `IS NULL` |
| Duplicate rows after JOIN | Use `DISTINCT` or check join keys |
| Partition expiration | Set `partition_expiration_days` |
| Table not found | Check dataset location (US vs EU) |
| Quota exceeded | Use slots, reduce concurrency |
| Stale data in views | Use materialized views with refresh |

---

## 10. Useful System Tables

```sql
-- Table metadata
SELECT * FROM dataset.INFORMATION_SCHEMA.TABLES;
SELECT * FROM dataset.INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'events';

-- Job history
SELECT * FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE state = 'DONE' AND error_result IS NOT NULL
ORDER BY end_time DESC;

-- Partitions info
SELECT * FROM dataset.events_table$__PARTITIONS_SUMMARY__;
```

---

## ❓ Likely Interview Questions

1. How do you optimize a slow BigQuery query?
2. What's the difference between partitioning and clustering? When would you use both?
3. How do you implement an upsert/merge in BigQuery?
4. Explain window functions with an example
5. How do you handle schema changes in BigQuery (adding columns, changing types)?
6. How do you control query costs?
7. What is a stored procedure in BQ and how do you use it?
8. How do you load data into BigQuery? What formats are supported?
9. What is `INFORMATION_SCHEMA` and how do you use it?
10. How do nested/repeated fields work and when would you use them?
