# SQL & BigQuery Stored Procedures - Interview Prep

---

## 1. Advanced SQL Patterns

### CTEs (Common Table Expressions)
```sql
-- Chain multiple CTEs for readability
WITH
daily_events AS (
  SELECT
    DATE(event_time) AS event_date,
    user_id,
    COUNT(*) AS event_count
  FROM events
  WHERE DATE(event_time) >= '2024-01-01'
  GROUP BY 1, 2
),
user_summary AS (
  SELECT
    user_id,
    AVG(event_count) AS avg_daily_events,
    MAX(event_count) AS max_daily_events
  FROM daily_events
  GROUP BY 1
)
SELECT * FROM user_summary WHERE avg_daily_events > 10;

-- Recursive CTE (hierarchy traversal)
WITH RECURSIVE org_hierarchy AS (
  -- Base case: top-level managers
  SELECT employee_id, manager_id, name, 0 AS level
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  -- Recursive case
  SELECT e.employee_id, e.manager_id, e.name, h.level + 1
  FROM employees e
  JOIN org_hierarchy h ON e.manager_id = h.employee_id
)
SELECT * FROM org_hierarchy ORDER BY level;
```

### Window Functions Deep Dive
```sql
-- Percentile / Quantile
SELECT
  user_id,
  revenue,
  NTILE(4) OVER (ORDER BY revenue) AS quartile,
  PERCENT_RANK() OVER (ORDER BY revenue) AS percentile,
  CUME_DIST() OVER (ORDER BY revenue) AS cumulative_dist
FROM orders;

-- Deduplication with ROW_NUMBER
WITH ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) AS rn
  FROM users
)
SELECT * FROM ranked WHERE rn = 1;

-- Moving average
SELECT
  date,
  revenue,
  AVG(revenue) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS rolling_7day_avg
FROM daily_sales;

-- FIRST_VALUE / LAST_VALUE
SELECT
  order_id,
  product_id,
  FIRST_VALUE(product_id) OVER (PARTITION BY order_id ORDER BY line_item_id) AS first_product,
  LAST_VALUE(product_id) OVER (
    PARTITION BY order_id ORDER BY line_item_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS last_product
FROM order_lines;
```

---

## 2. BigQuery Stored Procedures - Full Reference

### Basic Structure
```sql
CREATE OR REPLACE PROCEDURE `project.dataset.procedure_name`(
  IN param1 STRING,
  IN param2 DATE,
  OUT result_count INT64
)
BEGIN
  DECLARE v_temp_count INT64 DEFAULT 0;

  -- Use parameters
  SELECT COUNT(*) INTO v_temp_count
  FROM `project.dataset.events`
  WHERE source = param1
    AND DATE(event_time) = param2;

  SET result_count = v_temp_count;
END;

-- Call it
DECLARE output INT64;
CALL `project.dataset.procedure_name`('web', '2024-01-15', output);
SELECT output;
```

### Control Flow
```sql
CREATE OR REPLACE PROCEDURE dataset.incremental_load(IN run_date DATE)
BEGIN
  DECLARE rows_inserted INT64;
  DECLARE rows_deleted INT64;

  -- Delete existing data for the date
  DELETE FROM dataset.fact_events WHERE event_date = run_date;
  SET rows_deleted = @@row_count;

  -- Insert new data
  INSERT INTO dataset.fact_events
  SELECT
    DATE(event_time) AS event_date,
    user_id,
    event_type,
    COUNT(*) AS event_count
  FROM dataset.raw_events
  WHERE DATE(event_time) = run_date
  GROUP BY 1, 2, 3;

  SET rows_inserted = @@row_count;

  -- Conditional logic
  IF rows_inserted = 0 THEN
    RAISE USING MESSAGE = CONCAT('No data found for ', CAST(run_date AS STRING));
  END IF;

  -- Log results
  INSERT INTO dataset.pipeline_log (run_date, rows_deleted, rows_inserted, run_at)
  VALUES (run_date, rows_deleted, rows_inserted, CURRENT_TIMESTAMP());

  SELECT CONCAT('Deleted: ', CAST(rows_deleted AS STRING),
                ', Inserted: ', CAST(rows_inserted AS STRING)) AS summary;
END;
```

### Loop Pattern - Process Multiple Dates
```sql
CREATE OR REPLACE PROCEDURE dataset.backfill(IN start_date DATE, IN end_date DATE)
BEGIN
  DECLARE current_date DATE;
  SET current_date = start_date;

  WHILE current_date <= end_date DO
    CALL dataset.incremental_load(current_date);
    SET current_date = DATE_ADD(current_date, INTERVAL 1 DAY);
  END WHILE;
END;

-- Call backfill
CALL dataset.backfill('2024-01-01', '2024-01-31');
```

### Error Handling
```sql
CREATE OR REPLACE PROCEDURE dataset.safe_load(IN run_date DATE)
BEGIN
  BEGIN
    CALL dataset.incremental_load(run_date);
  EXCEPTION WHEN ERROR THEN
    -- Log the error
    INSERT INTO dataset.error_log (run_date, error_message, occurred_at)
    VALUES (run_date, @@error.message, CURRENT_TIMESTAMP());

    -- Re-raise to let Airflow know it failed
    RAISE;
  END;
END;
```

### Dynamic SQL with EXECUTE IMMEDIATE
```sql
DECLARE table_name STRING DEFAULT 'my_table';
DECLARE query STRING;

SET query = CONCAT(
  'SELECT COUNT(*) FROM `project.dataset.', table_name, '`'
);

EXECUTE IMMEDIATE query;

-- With parameters
EXECUTE IMMEDIATE
  'SELECT * FROM dataset.events WHERE event_type = ? AND date = ?'
  USING 'click', '2024-01-15';
```

---

## 3. Transaction-like Patterns in BigQuery

BigQuery does **not** have traditional transactions but supports:

```sql
-- Multi-statement transactions (BigQuery scripting)
BEGIN TRANSACTION;

  DELETE FROM dataset.summary WHERE summary_date = '2024-01-15';

  INSERT INTO dataset.summary
  SELECT '2024-01-15', COUNT(*) FROM dataset.events WHERE DATE(event_time) = '2024-01-15';

COMMIT TRANSACTION;

-- Or ROLLBACK on failure:
BEGIN
  BEGIN TRANSACTION;
    -- operations
  COMMIT TRANSACTION;
EXCEPTION WHEN ERROR THEN
  ROLLBACK TRANSACTION;
  RAISE;
END;
```

---

## 4. SQL Interview Questions - Solutions

### Find duplicates
```sql
SELECT id, COUNT(*) AS cnt
FROM table
GROUP BY id
HAVING COUNT(*) > 1;
```

### Nth highest salary
```sql
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET N-1;  -- N=2 means 2nd highest
```

### Running total / cumulative sum
```sql
SELECT date, revenue,
  SUM(revenue) OVER (ORDER BY date) AS cumulative_revenue
FROM daily_sales;
```

### Pivot
```sql
SELECT
  user_id,
  SUM(CASE WHEN event_type = 'click' THEN 1 ELSE 0 END) AS clicks,
  SUM(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS views,
  SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchases
FROM events
GROUP BY user_id;
```

### Year-over-year comparison
```sql
SELECT
  year,
  revenue,
  LAG(revenue) OVER (ORDER BY year) AS prev_year_revenue,
  ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY year)) / LAG(revenue) OVER (ORDER BY year), 2) AS yoy_pct_change
FROM (
  SELECT EXTRACT(YEAR FROM order_date) AS year, SUM(amount) AS revenue
  FROM orders GROUP BY 1
);
```

---

## ❓ Likely Interview Questions

1. What is a stored procedure in BigQuery and how does it differ from a view?
2. Write a stored procedure that loads data for a given date range
3. How do you handle errors in a BigQuery stored procedure?
4. Explain the difference between ROW_NUMBER, RANK, and DENSE_RANK
5. How do you write a recursive CTE?
6. How do you implement a slowly changing dimension in BigQuery using SQL?
7. Write a query to find the top 3 products by revenue for each category
8. What is EXECUTE IMMEDIATE used for?
9. How do you make stored procedures idempotent?
10. Write a query to find users who were active in month 1 but not in month 2 (churn analysis)
