# Debugging & Scenario-Based - Most Asked Interview Questions & Answers

---

## Q1. "Your BigQuery query is taking 10 minutes when it used to take 30 seconds. How do you debug it?"

**Answer (walk through this systematically):**

**Step 1: Check if data volume increased**
```sql
SELECT partition_id, row_count, last_modified_time
FROM dataset.INFORMATION_SCHEMA.PARTITIONS
WHERE table_name = 'events'
ORDER BY partition_id DESC LIMIT 7;
-- If recent partitions have 10x more rows → data explosion, not a query problem
```

**Step 2: Look at the query execution plan**
- Click "Explain" in BQ console on the slow query
- Identify which stage is the bottleneck (most input bytes, longest time)
- Look for: large shuffle, skewed stages, wide broadcast joins

**Step 3: Check if partition pruning broke**
```sql
-- Common mistake: someone added a function that defeats partition pruning
-- BAD (no pruning):
WHERE CAST(event_time AS DATE) = '2024-01-15'
WHERE FORMAT_DATE('%Y-%m-%d', event_time) = '2024-01-15'

-- GOOD (pruning works):
WHERE DATE(event_time) = '2024-01-15'
```

**Step 4: Check if a JOIN condition changed**
```sql
-- If someone accidentally removed a filter before a JOIN:
-- SELECT * FROM events e JOIN users u ON e.user_id = u.user_id  ← now a HUGE join
-- vs
-- with filter: WHERE DATE(e.event_time) = '2024-01-15'
```

**Step 5: Compare with INFORMATION_SCHEMA**
```sql
SELECT total_bytes_processed, total_slot_ms, query
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND query LIKE '%event_summary%'
ORDER BY creation_time DESC LIMIT 5;
-- Compare slot_ms and bytes for recent vs old runs
```

**Step 6: Fix options**
- Restore partition filter if it was removed
- Break into smaller queries with intermediate tables
- Add clustering if not present
- Check for new N:M JOIN created by schema changes

---

## Q2. "An Airflow DAG ran successfully but data is missing in BigQuery. What do you do?"

**Answer:**

This is a common scenario — the pipeline *ran* but didn't load correctly.

**Step 1: Verify the DAG actually succeeded properly**
```bash
# Check exact task states — "success" doesn't mean correct data
# Look at EACH task's log, not just the DAG-level status
```
In Airflow UI: Click the DAG run → inspect each task's individual log.

**Step 2: Check the load task log specifically**
- Was there a `rows_loaded = 0` warning?
- Did the GCS file exist? Was it empty?
- Did the query have a wrong date filter?

**Step 3: Check the source data**
```sql
-- Was the GCS file actually written?
-- gsutil ls gs://bucket/data/2024-01-15/

-- Was the staging table loaded?
SELECT COUNT(*), MIN(created_at), MAX(created_at)
FROM dataset.staging
WHERE load_date = '2024-01-15';
```

**Step 4: Check the target table**
```sql
-- Did the MERGE/INSERT actually run?
SELECT COUNT(*) FROM dataset.events WHERE DATE(event_time) = '2024-01-15';

-- Check job history for that table
SELECT job_id, statement_type, start_time, end_time
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE referenced_tables LIKE '%events%'
  AND creation_time BETWEEN '2024-01-15' AND '2024-01-16'
ORDER BY start_time;
```

**Step 5: Likely causes and fixes**
| Cause | Fix |
|-------|-----|
| Wrong date filter in query | Fix filter, rerun task |
| GCS file empty/missing | Check upstream producer, rerun |
| MERGE matched nothing | Debug match condition |
| BQ job failed silently | Check job errors in INFORMATION_SCHEMA |
| Task used wrong XCom value | Fix XCom key/task_id reference |

**Step 6: Re-run**
Clear the failed tasks in Airflow and re-trigger. Since the pipeline is idempotent (delete+insert), it's safe to re-run.

---

## Q3. "You see duplicate rows in your BigQuery table after a pipeline run. How do you fix it and prevent it?"

**Answer:**

**Immediate fix — deduplicate the table:**
```sql
-- Atomic overwrite with deduplication
CREATE OR REPLACE TABLE dataset.events AS
SELECT * EXCEPT(rn)
FROM (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY event_id    -- your unique key
      ORDER BY loaded_at DESC  -- keep the latest version
    ) AS rn
  FROM dataset.events
)
WHERE rn = 1;
```

**Root cause analysis — why did duplicates appear?**

1. **Pipeline ran twice** (e.g., Airflow retry after a partial success)
   - Fix: Use `WRITE_TRUNCATE` or `DELETE+INSERT` instead of `WRITE_APPEND`

2. **Source API returns duplicate events**
   - Fix: Deduplicate at source or in staging before loading to production

3. **MERGE condition was wrong** (matched on too-broad a key)
   - Fix: Tighten the ON condition to the true unique key

4. **No unique constraint enforced**
   - BigQuery doesn't enforce unique keys — you must handle this in your pipeline

**Prevention:**
```sql
-- Option 1: Delete partition before insert (most reliable)
DELETE FROM dataset.events WHERE DATE(event_time) = run_date;
INSERT INTO dataset.events SELECT ...;

-- Option 2: MERGE with correct unique key
MERGE dataset.events T USING new_data S ON T.event_id = S.event_id
WHEN NOT MATCHED THEN INSERT ROW
WHEN MATCHED THEN UPDATE SET T.value = S.value;

-- Option 3: Downstream view that always deduplicates
CREATE OR REPLACE VIEW dataset.events_deduped AS
SELECT * EXCEPT(rn) FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY loaded_at DESC) rn
  FROM dataset.events
) WHERE rn = 1;
```

---

## Q4. "An API you're ingesting from starts returning 429 Too Many Requests. What do you do?"

**Answer:**

**429 = Rate Limited** — you're calling the API too fast.

**Immediate handling in code:**
```python
import time
import requests

def call_with_backoff(url: str, headers: dict, max_retries: int = 5) -> dict:
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 429:
            # Respect the Retry-After header if provided
            retry_after = int(response.headers.get('Retry-After', 2 ** attempt))
            print(f"Rate limited. Waiting {retry_after}s (attempt {attempt+1})")
            time.sleep(retry_after)
            continue

        response.raise_for_status()
        return response.json()

    raise Exception("Exceeded max retries due to rate limiting")
```

**Longer-term fixes:**
1. **Reduce parallelism** — if you're making concurrent requests, limit workers
2. **Add delays between requests** — `time.sleep(0.5)` between calls
3. **Increase batch size, reduce request count** — fetch more per call if API allows
4. **Cache responses** — don't re-fetch the same data repeatedly
5. **Check your API plan** — you may have hit a quota; request a higher tier
6. **Use exponential backoff** — double the wait time on each retry

**In Airflow:**
```python
# Reduce parallelism at DAG level
with DAG('api_ingestion', max_active_tasks=2, ...):  # limit concurrent tasks
```

---

## Q5. "How do you ensure your data pipeline is idempotent?"

**Answer:**

**Idempotent** = running the pipeline multiple times produces the same result as running it once. Critical for safe retries, backfills, and debugging.

**What breaks idempotency:**
```python
# BAD: append-only — creates duplicates on re-run
INSERT INTO target SELECT * FROM source WHERE date = run_date;
```

**Patterns that ensure idempotency:**

**1. Delete + Insert (most reliable for BigQuery partitions)**
```sql
-- Always safe to re-run
DELETE FROM dataset.events WHERE event_date = @run_date;
INSERT INTO dataset.events
SELECT * FROM staging WHERE DATE(event_time) = @run_date;
```

**2. MERGE (upsert)**
```sql
-- Updates if exists, inserts if not — idempotent by design
MERGE target T USING source S ON T.id = S.id
WHEN MATCHED THEN UPDATE SET T.val = S.val
WHEN NOT MATCHED THEN INSERT VALUES (S.id, S.val, S.ts);
```

**3. CREATE OR REPLACE TABLE**
```sql
-- For derived/aggregated tables
CREATE OR REPLACE TABLE dataset.summary AS
SELECT DATE(ts) AS date, COUNT(*) FROM events GROUP BY 1;
```

**4. GCS: write to deterministic path (not append)**
```python
# BAD: timestamp in filename — creates new file every run
blob_path = f"data/{date}/output_{datetime.now()}.csv"

# GOOD: deterministic path — overwrites on re-run
blob_path = f"data/{date}/output.csv"
```

---

## Q6. "How do you monitor a production data pipeline? What would you set up?"

**Answer:**

A robust monitoring setup has three layers:

**Layer 1: Pipeline-level monitoring (Airflow)**
- Airflow UI shows DAG run status, task durations, failure history
- Set `email_on_failure=True` in `default_args`
- Use Airflow's built-in Slack/PagerDuty integration for alerts

**Layer 2: Data quality monitoring (post-load checks)**
```sql
-- Run these as separate Airflow tasks after each load
-- 1. Row count check
ASSERT (SELECT COUNT(*) FROM events WHERE event_date = CURRENT_DATE()) > 0
  AS 'No events loaded today';

-- 2. Data freshness
ASSERT (SELECT MAX(event_time) FROM events) >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)
  AS 'Data is stale (>2 hours old)';

-- 3. Anomaly: row count deviation > 50% from 7-day avg
WITH avg_count AS (
  SELECT AVG(cnt) AS avg_7d FROM (
    SELECT event_date, COUNT(*) AS cnt FROM events
    WHERE event_date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 8 DAY) AND DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
    GROUP BY 1
  )
)
SELECT IF(
  ABS((SELECT COUNT(*) FROM events WHERE event_date = CURRENT_DATE()) - avg_7d) / avg_7d > 0.5,
  ERROR('Row count anomaly detected'),
  'OK'
) FROM avg_count;
```

**Layer 3: Infrastructure monitoring (Cloud Monitoring)**
```
Metrics to monitor:
- Airflow task success rate
- BQ job duration and slot usage
- GCS file arrival latency
- Pub/Sub subscription lag (for streaming)

Alerts:
- DAG failure → PagerDuty/Slack
- Data freshness SLA breach → on-call alert
- BQ slot usage > 90% → scaling alert
```

**Layer 4: Logging**
```python
import logging
logger = logging.getLogger(__name__)

def load_task(**kwargs):
    logger.info(f"Starting load for {kwargs['ds']}")
    try:
        rows = load_data(kwargs['ds'])
        logger.info(f"Loaded {rows} rows successfully")
    except Exception as e:
        logger.error(f"Load failed: {str(e)}", exc_info=True)
        raise
```

---

## Q7. "How do you roll back a bad data load in BigQuery?"

**Answer:**

**Option 1: Time Travel (if < 7 days ago)**

BigQuery automatically keeps previous versions for up to 7 days (configurable).
```sql
-- Restore table to state at a specific time
CREATE OR REPLACE TABLE dataset.events AS
SELECT * FROM dataset.events
FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR);

-- Or restore just a partition
CREATE OR REPLACE TABLE dataset.events_backup AS
SELECT * FROM dataset.events
FOR SYSTEM_TIME AS OF '2024-01-15 09:00:00';
```

**Option 2: Reload from GCS (if you have the raw file)**
```sql
-- Delete the bad data
DELETE FROM dataset.events WHERE DATE(event_time) = '2024-01-15';

-- Reload from GCS
LOAD DATA INTO dataset.events
FROM FILES (format='CSV', uris=['gs://my-bucket/data/20240115/events.csv']);
```

**Option 3: Delete the bad partition**
```sql
-- If you loaded a bad date partition
DELETE FROM dataset.events WHERE event_date = '2024-01-15';
-- Then re-run the pipeline for that date
```

**Prevention:**
- Always write to a **staging table** first → validate → then swap/merge to production
- Use time travel as your safety net (keep 7-day retention)
- Keep the raw GCS files as immutable source of truth (don't delete after loading)

---

## Q8. What are common Python performance pitfalls in data engineering and how do you fix them?

**Answer:**

**1. Loading entire large file into memory**
```python
# BAD: 10GB file → OOM
df = pd.read_csv('huge_file.csv')

# GOOD: process in chunks
for chunk in pd.read_csv('huge_file.csv', chunksize=100_000):
    process_and_load(chunk)
```

**2. Looping over DataFrame rows (extremely slow)**
```python
# BAD: O(n) loop
for index, row in df.iterrows():
    df.at[index, 'new_col'] = row['a'] * 2

# GOOD: vectorized operation (100x faster)
df['new_col'] = df['a'] * 2
```

**3. Not using connection pooling for DB**
```python
# BAD: new connection per query
for row in rows:
    conn = psycopg2.connect(...)  # slow! connection overhead
    conn.execute(query)
    conn.close()

# GOOD: reuse connection or use SQLAlchemy pool
engine = create_engine(conn_string, pool_size=5)
with engine.connect() as conn:
    for row in rows:
        conn.execute(query, row)
```

**4. Making thousands of individual API calls**
```python
# BAD: one API call per user
for user_id in user_ids:  # 10,000 users = 10,000 calls
    data = requests.get(f"/users/{user_id}")

# GOOD: batch API call if supported
data = requests.post('/users/batch', json={'ids': user_ids})

# OR: parallel calls with ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_user, user_ids))
```

**5. String concatenation in loops**
```python
# BAD: O(n²) string concat
result = ""
for row in rows:
    result += str(row)  # creates new string each time!

# GOOD: join at the end
result = "".join(str(row) for row in rows)
```
