# Data Warehousing Concepts - Interview Prep

---

## 1. Data Warehouse vs Data Lake vs Lakehouse

| | Data Warehouse | Data Lake | Lakehouse |
|--|---------------|-----------|-----------|
| Data type | Structured | All types | All types |
| Schema | Schema-on-write | Schema-on-read | Both |
| Storage | Proprietary (BQ, Redshift) | GCS, S3 | GCS + Delta/Iceberg |
| Users | Analysts (SQL) | Data scientists | Both |
| Example | BigQuery | GCS | BigLake, Databricks |
| Cost | Higher | Lower | Medium |

---

## 2. Dimensional Modeling

### Fact Tables
- Contains **measurable events/metrics** (revenue, clicks, page views)
- Has foreign keys to dimension tables
- Usually large (millions to billions of rows)
- Types: **Transaction, Snapshot, Accumulating Snapshot**

### Dimension Tables
- Contains **descriptive attributes** (who, what, where, when)
- Relatively small
- Example: `dim_user`, `dim_product`, `dim_date`

---

## 3. Star vs Snowflake Schema

### Star Schema
- Fact table at center, dimension tables around it
- Dimension tables are **denormalized** (flat)
- Fast queries (fewer JOINs)
- More storage, less normalization

```
          dim_date
             |
dim_user -- fact_orders -- dim_product
             |
          dim_location
```

### Snowflake Schema
- Dimension tables are **normalized** (split into sub-dimensions)
- Saves storage, but more JOINs
- Used when storage is a concern or data integrity is critical

```
dim_category
     |
dim_product -- fact_orders -- dim_user -- dim_region -- dim_country
```

**For BigQuery**: Star schema preferred — JOINs are cheap, storage is cheaper than compute.

---

## 4. Slowly Changing Dimensions (SCD)

### SCD Type 1 - Overwrite
```sql
-- Just update the record, no history
UPDATE dim_user
SET email = 'new@email.com', updated_at = CURRENT_TIMESTAMP()
WHERE user_id = 123;
```
✅ Simple | ❌ No history

### SCD Type 2 - Add New Row (Most Common)
```sql
-- Add new row, keep old row with is_current = FALSE
INSERT INTO dim_user (user_id, email, is_current, valid_from, valid_to)
VALUES (123, 'new@email.com', TRUE, CURRENT_DATE(), NULL);

UPDATE dim_user
SET is_current = FALSE, valid_to = CURRENT_DATE()
WHERE user_id = 123 AND is_current = TRUE;
```
✅ Full history | ❌ More complex queries

**BigQuery SCD Type 2 with MERGE:**
```sql
MERGE dim_user T
USING (SELECT 123 AS user_id, 'new@email.com' AS email) S
ON T.user_id = S.user_id AND T.is_current = TRUE AND T.email != S.email
WHEN MATCHED THEN
  UPDATE SET T.is_current = FALSE, T.valid_to = CURRENT_DATE()
```

### SCD Type 3 - Add Column
```sql
-- Add previous value column
ALTER TABLE dim_user ADD COLUMN previous_email STRING;
UPDATE dim_user SET previous_email = email, email = 'new@email.com' WHERE user_id = 123;
```
✅ Simple | ❌ Only 1 level of history

---

## 5. ETL vs ELT

### ETL (Extract → Transform → Load)
- Transform **before** loading
- Used when target is not powerful enough to transform
- Old pattern (Informatica, SSIS era)

### ELT (Extract → Load → Transform)
- Load raw data first, transform **in** the warehouse
- Modern approach for BigQuery, Snowflake
- Cheaper (cloud storage is cheap), more flexible
- Tools: **dbt**, Dataform, BigQuery stored procedures

```
ELT with BigQuery:
GCS (raw CSV) → BQ staging table → BQ transformed table (via SQL/dbt)
```

---

## 6. Incremental vs Full Load

### Full Load
```sql
-- Truncate and reload
TRUNCATE TABLE staging.events;
INSERT INTO staging.events SELECT * FROM source.events;
```
✅ Simple | ❌ Slow for large tables, wastes compute

### Incremental Load
```sql
-- Load only new/changed records
INSERT INTO staging.events
SELECT * FROM source.events
WHERE updated_at > (SELECT MAX(updated_at) FROM staging.events);
```
✅ Fast | ❌ Need reliable watermark column

### Upsert / Merge
```sql
MERGE staging.events T
USING new_data S ON T.id = S.id
WHEN MATCHED THEN UPDATE SET T.value = S.value
WHEN NOT MATCHED THEN INSERT VALUES (S.id, S.value, S.created_at);
```

---

## 7. Data Quality

### Common Checks
```sql
-- Null check
SELECT COUNT(*) FROM table WHERE critical_column IS NULL;

-- Duplicate check
SELECT id, COUNT(*) FROM table GROUP BY id HAVING COUNT(*) > 1;

-- Row count check
SELECT COUNT(*) FROM staging_table;  -- compare with source

-- Referential integrity
SELECT t.user_id FROM fact_orders t
LEFT JOIN dim_user d ON t.user_id = d.user_id
WHERE d.user_id IS NULL;

-- Date range check
SELECT MIN(created_at), MAX(created_at) FROM events;
```

---

## 8. Partitioning Strategy in Data Warehousing

```sql
-- Partition by date (most common)
CREATE TABLE fact_events
PARTITION BY DATE(event_date) AS ...

-- Partition + cluster (best of both)
CREATE TABLE fact_orders
PARTITION BY DATE(order_date)
CLUSTER BY customer_id, product_category AS ...

-- Range partitioning (for numeric IDs)
CREATE TABLE dim_users
PARTITION BY RANGE_BUCKET(user_id, GENERATE_ARRAY(0, 10000000, 100000)) AS ...
```

---

## 9. Data Freshness Patterns

| Pattern | Description | Latency |
|---------|-------------|---------|
| Batch | Run every N hours | Hours |
| Micro-batch | Run every few minutes | Minutes |
| Streaming | Real-time ingestion (Pub/Sub → Dataflow → BQ) | Seconds |
| Lambda Architecture | Both batch and streaming | Mix |

---

## 10. Common Data Modeling Interview Terms

| Term | Definition |
|------|------------|
| Grain | The level of detail in a fact table (e.g., one row per order line) |
| Surrogate key | Auto-generated key (not from source) for dim table |
| Natural key | Business key from source system |
| Conformed dimension | Shared dimension across multiple fact tables |
| Degenerate dimension | Dimension stored in fact table (e.g., order number) |
| Bridge table | Handles many-to-many relationships |
| Date dimension | Pre-populated calendar table with attributes |

---

## ❓ Likely Interview Questions

1. What's the difference between a star and snowflake schema?
2. What are SCD types? Which one would you use and why?
3. What's the difference between ETL and ELT?
4. How do you implement incremental loads in BigQuery?
5. How do you ensure data quality in a pipeline?
6. What is a fact table vs a dimension table?
7. How would you model a scenario where a customer's address changes over time?
8. What is a date dimension and why is it important?
9. How do you handle late-arriving data?
10. What is the grain of a fact table?
