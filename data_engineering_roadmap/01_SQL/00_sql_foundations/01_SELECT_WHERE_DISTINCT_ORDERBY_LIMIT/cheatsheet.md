# SQL Query Basics - Cheatsheet

## SELECT

### ✅ Best Practices

* Select only the required columns.
* Avoid `SELECT *` in production.
* Use meaningful column aliases when required.

### ❌ Avoid

```sql
SELECT *
FROM employees;
```

### ✅ Prefer

```sql
SELECT employee_id,
       name,
       department
FROM employees;
```

### Why?

* Better performance
* Lower cloud cost
* Better readability
* Prevents accidental exposure of sensitive data
* Avoids schema coupling

---

## WHERE

### Purpose

Filters **rows** before grouping.

### Example

```sql
SELECT *
FROM employees
WHERE salary > 100000;
```

### Remember

```text
WHERE → Rows
```

### Best Practices

* Filter as early as possible.
* Avoid applying functions on indexed or partitioned columns.

### ❌ Avoid

```sql
WHERE YEAR(order_date) = 2025
```

### ✅ Prefer

```sql
WHERE order_date >= '2025-01-01'
  AND order_date < '2026-01-01'
```

---

## DISTINCT

### Purpose

Returns unique values.

### Example

```sql
SELECT DISTINCT department
FROM employees;
```

### DISTINCT vs GROUP BY

| DISTINCT               | GROUP BY                          |
| ---------------------- | --------------------------------- |
| Retrieve unique values | Aggregate data                    |
| Better readability     | Required for COUNT, SUM, AVG etc. |

### Best Practices

* Use DISTINCT only when uniqueness is required.
* Don't use DISTINCT to hide incorrect JOINs.

---

## ORDER BY

### Purpose

Sorts the final result.

### Example

```sql
SELECT *
FROM employees
ORDER BY salary DESC;
```

### Default

```text
ASC
```

### Multiple Columns

```sql
ORDER BY department,
         salary DESC;
```

```text
Primary Sort Key

↓

Secondary Sort Key
```

### Aliases

✅ Allowed

```sql
SELECT salary AS sal
FROM employees
ORDER BY sal;
```

---

## LIMIT

### Purpose

Restricts the number of returned rows.

### Example

```sql
SELECT *
FROM employees
LIMIT 10;
```

### Always Prefer

```sql
SELECT *
FROM employees
ORDER BY employee_id
LIMIT 10;
```

Never rely on LIMIT without ORDER BY.

---

## OFFSET

### Example

```sql
LIMIT 20 OFFSET 40
```

Meaning:

```text
Skip first 40 rows

↓

Return next 20 rows
```

### Drawback

Large OFFSET values become slower because the database must skip all preceding rows.

---

## Cursor Pagination

Instead of

```sql
LIMIT 20 OFFSET 1000000
```

Prefer

```sql
WHERE post_id > 1000000
ORDER BY post_id
LIMIT 20
```

Benefits:

* Faster
* Scalable
* Better for APIs

---

# SQL Execution Reminder

```text
FROM
JOIN
WHERE
GROUP BY
HAVING
SELECT
DISTINCT
ORDER BY
LIMIT
```

---

# Frequently Asked Interview Traps

| Question                  | Answer                                            |
| ------------------------- | ------------------------------------------------- |
| Can WHERE use aliases?    | ❌ No                                              |
| Can ORDER BY use aliases? | ✅ Yes                                             |
| Can WHERE use COUNT()?    | ❌ No                                              |
| Can HAVING use COUNT()?   | ✅ Yes                                             |
| LIMIT without ORDER BY?   | Non-deterministic                                 |
| DISTINCT vs GROUP BY?     | DISTINCT for uniqueness, GROUP BY for aggregation |

---

# Production Best Practices

✅ Select only required columns.

✅ Filter early using WHERE.

✅ Avoid functions on indexed/partitioned columns.

✅ Don't use DISTINCT to hide duplicate problems.

✅ Always pair LIMIT with ORDER BY.

✅ Prefer Cursor Pagination over large OFFSET values.

---

# Quick Revision

```text
SELECT
↓

Choose required columns

------------------------

WHERE
↓

Filter rows

------------------------

DISTINCT
↓

Remove duplicates

------------------------

ORDER BY
↓

Sort output

------------------------

LIMIT
↓

Restrict rows returned

------------------------

OFFSET
↓

Skip rows

------------------------

Cursor Pagination
↓

Better than OFFSET for large datasets
```
