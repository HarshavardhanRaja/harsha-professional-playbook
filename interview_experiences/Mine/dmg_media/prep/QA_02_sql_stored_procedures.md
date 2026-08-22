# SQL & Stored Procedures - Most Asked Interview Questions & Answers

---

## Q1. What is a stored procedure? How is it different from a function or a view?

**Answer:**

| | Stored Procedure | Function (UDF) | View |
|--|-----------------|----------------|------|
| Returns | Optional result sets | Must return a value | Always returns data |
| Can run DML | Yes (INSERT/UPDATE/DELETE) | No (in BQ) | No |
| Input params | IN, OUT, INOUT | IN only | No params |
| Use in SQL | `CALL proc()` | `SELECT my_func()` | `SELECT * FROM view` |
| Control flow | Yes (loops, conditionals) | Yes (limited) | No |
| Side effects | Yes | No (pure) | No |

**BigQuery Stored Procedure example:**
```sql
CREATE OR REPLACE PROCEDURE dataset.daily_load(IN run_date DATE)
BEGIN
  DELETE FROM dataset.summary WHERE date = run_date;
  INSERT INTO dataset.summary SELECT run_date, COUNT(*), SUM(revenue)
  FROM dataset.events WHERE DATE(ts) = run_date;
END;

CALL dataset.daily_load('2024-01-15');
```

**BigQuery UDF (function) example:**
```sql
CREATE OR REPLACE FUNCTION dataset.format_currency(amount FLOAT64)
RETURNS STRING AS (
  CONCAT('£', FORMAT('%.2f', amount))
);

-- Use in SELECT:
SELECT dataset.format_currency(revenue) FROM orders;
```

---

## Q2. What are CTEs and when would you use them over subqueries?

**Answer:**

**CTE (Common Table Expression)** = a named temporary result set defined with `WITH`, scoped to the query.

```sql
-- CTE version
WITH active_users AS (
  SELECT user_id FROM users WHERE status = 'active'
),
recent_orders AS (
  SELECT user_id, COUNT(*) AS order_count
  FROM orders
  WHERE order_date >= '2024-01-01'
  GROUP BY user_id
)
SELECT u.user_id, o.order_count
FROM active_users u
JOIN recent_orders o ON u.user_id = o.user_id;
```

**CTE vs Subquery:**
| | CTE | Subquery |
|--|-----|----------|
| Readability | Better (named, reusable in same query) | Can get deeply nested |
| Reuse | Can reference same CTE multiple times | Must repeat |
| Debugging | Easy to isolate and test each CTE | Harder |
| Performance | Same in BigQuery (BQ inlines CTEs) | Same |

**Use CTEs when:** query has multiple logical steps, you need to reference the same intermediate result multiple times, or the query is complex and needs to be readable.

---

## Q3. Explain the difference between WHERE and HAVING.

**Answer:**

- **WHERE**: filters **rows** before aggregation (operates on raw columns)
- **HAVING**: filters **groups** after aggregation (operates on aggregated results)

```sql
-- WHERE: filter before grouping
SELECT
  category,
  SUM(revenue) AS total_revenue
FROM orders
WHERE status = 'completed'          -- filter raw rows first
GROUP BY category
HAVING SUM(revenue) > 10000;        -- then filter aggregated groups
```

**Rule:** If you can put a filter in WHERE, always do — it reduces data before aggregation and is more efficient. Use HAVING only when filtering on aggregate results (SUM, COUNT, AVG, etc.).

---

## Q4. Write a query to find the top 3 products by revenue for each category.

**Answer:**

This is a classic **Top-N per group** problem — solved with `ROW_NUMBER()`:

```sql
WITH ranked_products AS (
  SELECT
    category,
    product_id,
    product_name,
    SUM(revenue) AS total_revenue,
    ROW_NUMBER() OVER (
      PARTITION BY category           -- restart rank for each category
      ORDER BY SUM(revenue) DESC      -- highest revenue first
    ) AS rank
  FROM order_items
  GROUP BY category, product_id, product_name
)
SELECT category, product_id, product_name, total_revenue, rank
FROM ranked_products
WHERE rank <= 3
ORDER BY category, rank;
```

---

## Q5. How do you write a query for churn analysis (users active in month 1 but not in month 2)?

**Answer:**

```sql
-- Users active in January 2024 but NOT in February 2024
WITH jan_users AS (
  SELECT DISTINCT user_id FROM events
  WHERE DATE_TRUNC(event_date, MONTH) = '2024-01-01'
),
feb_users AS (
  SELECT DISTINCT user_id FROM events
  WHERE DATE_TRUNC(event_date, MONTH) = '2024-02-01'
)
SELECT
  j.user_id,
  'churned' AS status
FROM jan_users j
LEFT JOIN feb_users f ON j.user_id = f.user_id
WHERE f.user_id IS NULL;    -- present in Jan, missing in Feb
```

**Alternative using NOT EXISTS:**
```sql
SELECT DISTINCT user_id
FROM events
WHERE DATE_TRUNC(event_date, MONTH) = '2024-01-01'
  AND user_id NOT IN (
    SELECT DISTINCT user_id FROM events
    WHERE DATE_TRUNC(event_date, MONTH) = '2024-02-01'
  );
```

---

## Q6. What is a MERGE statement and when would you use it over INSERT or UPDATE?

**Answer:**

`MERGE` combines INSERT, UPDATE, and DELETE into a single atomic statement based on a matching condition. It's the standard way to do **upserts** in BigQuery.

**Use MERGE when:**
- You have a source of new/changed data and need to sync it to a target table
- You want to handle insert/update/delete cases in one operation
- You're implementing SCD Type 2 (slowly changing dimensions)
- You want an idempotent load (safe to re-run)

```sql
-- Load incremental data from staging to production
MERGE `project.dataset.users` AS target
USING `project.dataset.users_staging` AS source
ON target.user_id = source.user_id

WHEN MATCHED AND target.updated_at < source.updated_at THEN
  -- Record exists and source is newer → update
  UPDATE SET
    target.email = source.email,
    target.name = source.name,
    target.updated_at = source.updated_at

WHEN NOT MATCHED BY TARGET THEN
  -- New record in source → insert
  INSERT (user_id, email, name, created_at, updated_at)
  VALUES (source.user_id, source.email, source.name, source.created_at, source.updated_at)

WHEN NOT MATCHED BY SOURCE THEN
  -- Record in target not in source → can DELETE if needed
  DELETE;
```

**Prefer DELETE+INSERT for partitioned tables** when you're reloading a whole partition — it's simpler and works better with BigQuery's partition-level atomicity.

---

## Q7. How do you implement SCD Type 2 in BigQuery using SQL?

**Answer:**

SCD Type 2 = keep full history by adding a new row when a record changes.

**Schema:**
```sql
CREATE TABLE dim_users (
  user_id INT64,
  email STRING,
  plan STRING,
  is_current BOOL,
  valid_from DATE,
  valid_to DATE
);
```

**SCD Type 2 MERGE:**
```sql
-- Step 1: Expire old records that changed
UPDATE dim_users
SET is_current = FALSE,
    valid_to = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
WHERE is_current = TRUE
  AND user_id IN (
    SELECT s.user_id FROM staging_users s
    JOIN dim_users d ON s.user_id = d.user_id AND d.is_current = TRUE
    WHERE s.email != d.email OR s.plan != d.plan  -- something changed
  );

-- Step 2: Insert new versions
INSERT INTO dim_users (user_id, email, plan, is_current, valid_from, valid_to)
SELECT s.user_id, s.email, s.plan, TRUE, CURRENT_DATE(), NULL
FROM staging_users s
WHERE NOT EXISTS (
  SELECT 1 FROM dim_users d
  WHERE d.user_id = s.user_id AND d.is_current = TRUE
    AND d.email = s.email AND d.plan = s.plan  -- no change
);
```

**Query current state:**
```sql
SELECT * FROM dim_users WHERE is_current = TRUE;
```

**Query state at a point in time:**
```sql
SELECT * FROM dim_users
WHERE valid_from <= '2023-06-01'
  AND (valid_to IS NULL OR valid_to >= '2023-06-01');
```

---

## Q8. Explain PARTITION BY in window functions vs GROUP BY. What's the difference?

**Answer:**

| | GROUP BY | PARTITION BY (window) |
|--|----------|----------------------|
| Output rows | One row per group | Same number of rows as input |
| Collapses rows | Yes | No |
| Access to other cols | Only aggregated | All original columns retained |
| Use case | Summarize data | Compute rank/running total per group |

```sql
-- GROUP BY: 3 rows → 1 row per category
SELECT category, SUM(revenue) AS total FROM orders GROUP BY category;
-- Result: electronics → 50000, clothing → 30000

-- PARTITION BY: keeps all rows, adds aggregate alongside each
SELECT
  order_id, category, revenue,
  SUM(revenue) OVER (PARTITION BY category) AS category_total,
  revenue / SUM(revenue) OVER (PARTITION BY category) AS pct_of_category
FROM orders;
-- Result: still all 1000 order rows, but with category total and % alongside each
```

---

## Q9. How do you write a recursive CTE? Give a practical example.

**Answer:**

Recursive CTEs are used for **hierarchical/tree data** — org charts, categories, bill of materials.

```sql
-- Example: traverse an org hierarchy to get all reports under a manager
WITH RECURSIVE employee_hierarchy AS (
  -- Anchor (base case): start from the top-level manager
  SELECT
    employee_id,
    manager_id,
    name,
    title,
    0 AS depth
  FROM employees
  WHERE employee_id = 1001   -- CEO

  UNION ALL

  -- Recursive step: find direct reports of previous level
  SELECT
    e.employee_id,
    e.manager_id,
    e.name,
    e.title,
    h.depth + 1
  FROM employees e
  INNER JOIN employee_hierarchy h ON e.manager_id = h.employee_id
)
SELECT
  REPEAT('  ', depth) || name AS indented_name,
  title,
  depth AS org_level
FROM employee_hierarchy
ORDER BY depth, name;
```

> ⚠️ BigQuery supports recursive CTEs but requires the `RECURSIVE` keyword. Add a depth limit to prevent infinite loops if data has cycles.

---

## Q10. Write a query to calculate year-over-year growth.

**Answer:**

```sql
WITH yearly_revenue AS (
  SELECT
    EXTRACT(YEAR FROM order_date) AS year,
    SUM(amount) AS revenue
  FROM orders
  GROUP BY 1
)
SELECT
  year,
  revenue,
  LAG(revenue) OVER (ORDER BY year) AS prev_year_revenue,
  ROUND(
    100.0 * (revenue - LAG(revenue) OVER (ORDER BY year))
    / LAG(revenue) OVER (ORDER BY year),
    2
  ) AS yoy_growth_pct
FROM yearly_revenue
ORDER BY year;
```

---

## Q11. What is EXECUTE IMMEDIATE in BigQuery? When would you use it?

**Answer:**

`EXECUTE IMMEDIATE` runs a **dynamically constructed SQL string** at runtime. Used when the table name, columns, or conditions need to be determined at run time.

```sql
-- Dynamic table name
DECLARE table_suffix STRING DEFAULT '20240115';
EXECUTE IMMEDIATE
  CONCAT('SELECT COUNT(*) FROM `project.dataset.events_', table_suffix, '`');

-- Dynamic with parameters (prevents SQL injection)
EXECUTE IMMEDIATE
  'SELECT * FROM dataset.events WHERE event_type = ? AND date = ?'
  USING 'click', '2024-01-15';

-- Practical use: process each date in a loop dynamically
FOR date_row IN (SELECT DISTINCT DATE(ts) AS d FROM source ORDER BY d) DO
  EXECUTE IMMEDIATE
    CONCAT('CALL dataset.load_partition("', CAST(date_row.d AS STRING), '")');
END FOR;
```

**When to use:** dynamic partition processing, multi-tenant pipelines where table names are parameterized, metadata-driven ETL.

---

## Q12. How do you pivot data in BigQuery (rows to columns)?

**Answer:**

BigQuery doesn't have a native `PIVOT` keyword (as of now — it does have experimental PIVOT but it's limited). Standard approach uses conditional aggregation:

```sql
-- Convert: (user_id, month, revenue) → (user_id, jan_rev, feb_rev, mar_rev)
SELECT
  user_id,
  SUM(CASE WHEN month = 1 THEN revenue ELSE 0 END) AS jan_revenue,
  SUM(CASE WHEN month = 2 THEN revenue ELSE 0 END) AS feb_revenue,
  SUM(CASE WHEN month = 3 THEN revenue ELSE 0 END) AS mar_revenue
FROM monthly_revenue
WHERE year = 2024
GROUP BY user_id;
```

**For dynamic pivot** (unknown columns), you'd need to generate SQL dynamically using `EXECUTE IMMEDIATE`.

---

## Q13. How do you find and remove duplicate rows in BigQuery?

**Answer:**

```sql
-- Step 1: Find duplicates
SELECT id, COUNT(*) AS cnt
FROM my_table
GROUP BY id
HAVING COUNT(*) > 1;

-- Step 2a: Keep latest version (using CTE + overwrite)
CREATE OR REPLACE TABLE my_table AS
SELECT * EXCEPT(rn)
FROM (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC) AS rn
  FROM my_table
)
WHERE rn = 1;

-- Step 2b: Delete duplicates keeping one (using DELETE + subquery)
DELETE FROM my_table
WHERE id IN (
  SELECT id FROM (
    SELECT id,
      ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC) AS rn
    FROM my_table
  )
  WHERE rn > 1
);
```

---

## Q14. What is a stored procedure's error handling and how does @@error work?

**Answer:**

```sql
CREATE OR REPLACE PROCEDURE dataset.safe_load(IN run_date DATE)
BEGIN
  -- Outer block with exception handler
  BEGIN
    -- Your main logic
    DELETE FROM dataset.target WHERE date = run_date;

    INSERT INTO dataset.target
    SELECT * FROM dataset.source WHERE DATE(ts) = run_date;

    -- @@row_count = rows affected by last DML statement
    IF @@row_count = 0 THEN
      RAISE USING MESSAGE = 'No rows inserted - check source data';
    END IF;

  EXCEPTION WHEN ERROR THEN
    -- @@error.message = error message from the failed statement
    -- @@error.statement_text = SQL that caused the error
    -- @@error.formatted_stack_trace = full stack

    INSERT INTO dataset.pipeline_errors
      (procedure_name, run_date, error_message, occurred_at)
    VALUES
      ('safe_load', run_date, @@error.message, CURRENT_TIMESTAMP());

    -- Re-raise so the caller (Airflow) sees the failure
    RAISE USING MESSAGE = @@error.message;
  END;
END;
```

**Key system variables in BQ scripting:**
- `@@row_count` — rows affected by last DML
- `@@error.message` — error message (only in EXCEPTION block)
- `@@error.statement_text` — the SQL that failed
- `@@script.bytes_billed` — bytes billed so far in script

---

## Q15. What's the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN?

**Answer:**

```sql
-- Sample data:
-- orders: order_id=1,user_id=10 | order_id=2,user_id=99 (no matching user)
-- users:  user_id=10,name='Alice' | user_id=20,name='Bob' (no orders)

-- INNER JOIN: only rows matching in BOTH tables
SELECT o.order_id, u.name FROM orders o INNER JOIN users u ON o.user_id = u.user_id;
-- Result: order_id=1, 'Alice' only (user 99 and user 20 excluded)

-- LEFT JOIN: all rows from LEFT + matching from RIGHT (NULL if no match)
SELECT o.order_id, u.name FROM orders o LEFT JOIN users u ON o.user_id = u.user_id;
-- Result: order_id=1,'Alice' AND order_id=2,NULL (all orders, user 20 excluded)

-- RIGHT JOIN: all rows from RIGHT + matching from LEFT
-- (rarely used, same as LEFT JOIN with tables swapped)

-- FULL OUTER JOIN: all rows from BOTH tables (NULL where no match)
SELECT o.order_id, u.name FROM orders o FULL OUTER JOIN users u ON o.user_id = u.user_id;
-- Result: order_id=1,'Alice' AND order_id=2,NULL AND NULL,'Bob'
```

**Best practice in BigQuery:** Prefer LEFT JOIN. FULL OUTER JOIN is expensive — it requires a full scan of both tables and produces more output data.
