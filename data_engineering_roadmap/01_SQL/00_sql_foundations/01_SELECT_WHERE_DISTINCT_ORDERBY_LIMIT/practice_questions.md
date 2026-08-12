# SQL Query Basics - Practice Questions

> Goal: Test your understanding of SELECT, WHERE, DISTINCT, ORDER BY, LIMIT, OFFSET and production best practices.
>
> Rule: Try answering first before looking at the answer.

================================================================================

# 🟢 LEVEL 1 - FUNDAMENTALS

================================================================================

## Question 1

```sql
SELECT *
FROM employees;
```

Would you approve this query for production?

---

Answer:

❌ No.

Reasons:

* Reads unnecessary columns.
* Increases I/O and cloud cost.
* May expose sensitive columns.
* Couples downstream applications to schema changes.
* Makes the query harder to understand.

Better approach:

```sql
SELECT employee_id,
       name,
       department
FROM employees;
```

================================================================================

## Question 2

```sql
SELECT *
FROM orders
WHERE YEAR(order_date) = 2025;
```

Would you approve this query?

---

Answer:

❌ No.

Applying a function on the filter column may prevent efficient index usage or partition pruning.

Better query:

```sql
SELECT *
FROM orders
WHERE order_date >= '2025-01-01'
  AND order_date < '2026-01-01';
```

================================================================================

## Question 3

Will these two queries return the same result?

```sql
SELECT DISTINCT department
FROM employees;
```

```sql
SELECT department
FROM employees
GROUP BY department;
```

Which one would you prefer?

---

Answer:

✅ Both return the same result.

Prefer **DISTINCT** because the requirement is simply to retrieve unique values.

Use GROUP BY only when aggregations are required.

================================================================================

## Question 4

```sql
SELECT *
FROM employees
LIMIT 10;
```

Does this return the first 10 employees?

---

Answer:

❌ No.

SQL tables are logically unordered.

Without ORDER BY, LIMIT may return different rows across executions.

================================================================================

## Question 5

```sql
SELECT *
FROM employees
ORDER BY salary DESC
LIMIT 10;
```

What does this query return?

---

Answer:

✅ The top 10 highest-paid employees.

ORDER BY determines which rows come first.

LIMIT determines how many rows are returned.

================================================================================

# 🟡 LEVEL 2 - INTERVIEW TRAPS

================================================================================

## Question 6

Which query is better for pagination?

Query A

```sql
SELECT *
FROM posts
ORDER BY post_id
LIMIT 20 OFFSET 1000000;
```

Query B

```sql
SELECT *
FROM posts
WHERE post_id > 1000000
ORDER BY post_id
LIMIT 20;
```

---

Answer:

✅ Query B.

It uses Cursor (Keyset) Pagination.

The database can jump directly to the required location using the index instead of skipping one million rows.

================================================================================

## Question 7

Review this query.

```sql
SELECT DISTINCT customer_id
FROM orders;
```

Would you approve it immediately?

---

Answer:

❌ Not immediately.

First ask:

> Why are duplicates being generated?

DISTINCT should not hide incorrect JOINs or data quality problems.

================================================================================

## Question 8

Which query is easier to understand?

```sql
SELECT *
FROM employees;
```

OR

```sql
SELECT employee_id,
       name,
       department
FROM employees;
```

---

Answer:

✅ Second query.

Explicit column selection improves readability and clearly communicates the business requirement.

================================================================================

## Question 9

Suppose a new column named `aadhaar_number` is added to the table.

Which query is affected?

```sql
SELECT *
FROM employees;
```

OR

```sql
SELECT employee_id,
       name
FROM employees;
```

---

Answer:

The first query.

`SELECT *` automatically includes the new column, which may expose sensitive data or break downstream applications.

================================================================================

# 🔴 LEVEL 3 - PRODUCTION THINKING

================================================================================

## Question 10

Review this query.

```sql
SELECT DISTINCT *
FROM orders
WHERE YEAR(order_date)=2025
LIMIT 100;
```

Identify all the issues.

---

Answer:

Issues:

* Avoid SELECT *.
* Avoid YEAR() in WHERE.
* DISTINCT may hide duplicate problems.
* LIMIT should usually be paired with ORDER BY.

================================================================================

## Question 11

A dashboard displays only:

* Employee Name
* Department

Developer writes:

```sql
SELECT *
FROM employees;
```

What feedback would you give?

---

Answer:

Retrieve only the required columns.

```sql
SELECT name,
       department
FROM employees;
```

This improves readability, reduces data scanned, lowers cloud cost, and avoids exposing unnecessary information.

================================================================================

## Question 12

An API supports pagination.

Current implementation:

```sql
SELECT *
FROM posts
ORDER BY post_id
LIMIT 20 OFFSET 500000;
```

How would you improve it?

---

Answer:

Use Cursor Pagination.

```sql
SELECT *
FROM posts
WHERE post_id > :last_post_id
ORDER BY post_id
LIMIT 20;
```

This avoids scanning and skipping hundreds of thousands of rows.

================================================================================

# 🧠 MASTERY CHALLENGE

================================================================================

## Question 13

Review the following query like a Senior Data Engineer.

```sql
SELECT DISTINCT *
FROM orders
WHERE YEAR(order_date)=2025
LIMIT 100;
```

List every issue, explain why it is a problem, and rewrite the query following production best practices.

---

Expected Answer

Problems:

1. `SELECT *` reads unnecessary columns and increases cost.
2. `YEAR(order_date)` may prevent efficient index usage or partition pruning.
3. `DISTINCT` may hide data quality or JOIN issues.
4. `LIMIT` without `ORDER BY` produces non-deterministic results.

One possible rewrite:

```sql
SELECT order_id,
       customer_id,
       order_date,
       order_amount
FROM orders
WHERE order_date >= '2025-01-01'
  AND order_date < '2026-01-01'
ORDER BY order_date DESC
LIMIT 100;
```

================================================================================

# ✅ Completion Criteria

If you can confidently answer all 13 questions without looking at the answers, you have mastered:

* SELECT
* WHERE
* DISTINCT
* ORDER BY
* LIMIT
* OFFSET
* Cursor Pagination
* Production SQL Best Practices
