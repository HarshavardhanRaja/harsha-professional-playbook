# LIMIT

## What Is LIMIT?

The `LIMIT` clause restricts the number of rows returned by a query.

It tells SQL:

> "Return only the required number of rows."

Example:

```sql
SELECT *
FROM employees
LIMIT 5;
```

Only the first 5 rows from the result set are returned.

---

## Why Do We Need LIMIT?

LIMIT helps us:

* Retrieve Top N records
* Preview data
* Build dashboards
* Implement pagination
* Reduce unnecessary data transfer

---

## Mental Model

Think of a restaurant.

The kitchen prepares many dishes.

LIMIT tells the waiter:

> "Serve only the first N dishes."

It doesn't change how the dishes are prepared—it only limits what is served.

---

## Example

Employee Table

| employee_id | name   | salary |
| ----------- | ------ | ------ |
| 1           | Harsha | 120000 |
| 2           | Ravi   | 90000  |
| 3           | Priya  | 150000 |
| 4           | Amit   | 100000 |
| 5           | Kiran  | 95000  |

Query

```sql
SELECT *
FROM employees
LIMIT 3;
```

Output

| employee_id | name   | salary |
| ----------- | ------ | ------ |
| 1           | Harsha | 120000 |
| 2           | Ravi   | 90000  |
| 3           | Priya  | 150000 |

---

## LIMIT Without ORDER BY

Consider:

```sql
SELECT *
FROM employees
LIMIT 3;
```

Does this return the "first" three employees?

**No.**

SQL tables are logically unordered.

Without an `ORDER BY` clause, the database is free to return **any** three rows based on the execution plan, storage layout, indexes, or partitions.

If you need deterministic results, always use ORDER BY.

Example:

```sql
SELECT *
FROM employees
ORDER BY employee_id
LIMIT 3;
```

---

## LIMIT With ORDER BY

A very common production pattern:

```sql
SELECT *
FROM employees
ORDER BY salary DESC
LIMIT 10;
```

This returns the top 10 highest-paid employees.

ORDER BY determines **which** rows are first.

LIMIT determines **how many** rows are returned.

---

## OFFSET

OFFSET skips a specified number of rows before returning results.

Example:

```sql
SELECT *
FROM employees
ORDER BY employee_id
LIMIT 5 OFFSET 10;
```

SQL performs:

1. Skip the first 10 rows.
2. Return the next 5 rows.

This is commonly used for pagination.

---

## Why OFFSET Becomes Slow

Suppose you execute:

```sql
LIMIT 20 OFFSET 1000000;
```

The database still needs to process and skip the first one million rows before returning the next 20.

As the OFFSET grows, query performance degrades.

---

## Cursor (Keyset) Pagination

Instead of OFFSET:

```sql
SELECT *
FROM posts
ORDER BY post_id
LIMIT 20 OFFSET 1000000;
```

Prefer:

```sql
SELECT *
FROM posts
WHERE post_id > 1000000
ORDER BY post_id
LIMIT 20;
```

If `post_id` is indexed, the database can jump directly to the required location instead of scanning and skipping previous rows.

This technique is called **Cursor Pagination** or **Keyset Pagination**.

It is commonly used in production systems such as APIs and social media feeds.

---

## Production Scenario

An application displays 20 products per page.

Using OFFSET works well for small page numbers.

For very large datasets, Cursor Pagination scales much better because it avoids skipping millions of rows.

---

## Common Mistakes

### Mistake 1

Using LIMIT without ORDER BY.

---

### Mistake 2

Assuming LIMIT returns the "first" rows from a table.

---

### Mistake 3

Using OFFSET for deep pagination on large datasets.

---

### Mistake 4

Ignoring indexes when implementing pagination.

---

## Interview Explanation

A concise interview answer:

> "LIMIT restricts the number of rows returned by a query. When deterministic results are required, it should always be used with ORDER BY. For large-scale pagination, OFFSET becomes inefficient because the database must skip rows before returning results, so I prefer Cursor (Keyset) Pagination whenever possible."

---

## Key Takeaways

* LIMIT restricts the number of rows returned.
* LIMIT does not define row order.
* Always combine LIMIT with ORDER BY for deterministic results.
* OFFSET skips rows before returning results.
* OFFSET becomes slower as the page number increases.
* Cursor Pagination is more efficient for large datasets.
