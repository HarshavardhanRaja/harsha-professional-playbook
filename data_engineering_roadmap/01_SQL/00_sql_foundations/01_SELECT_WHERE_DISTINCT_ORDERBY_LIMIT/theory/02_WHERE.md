# WHERE

## What Is WHERE?

The `WHERE` clause filters individual rows before they are processed by the rest of the query.

It tells SQL:

> "From all the available rows, keep only those that satisfy the given condition."

Example:

```sql
SELECT name,
       salary
FROM employees
WHERE salary > 100000;
```

Only employees with a salary greater than 100000 are returned.

---

## Why Do We Need WHERE?

WHERE helps us:

* Retrieve only relevant rows
* Reduce unnecessary processing
* Improve query performance
* Reduce data scanned in large tables

---

## Mental Model

Think of SQL as recruiting employees.

* **FROM** collects all applications.
* **WHERE** rejects candidates who don't meet the criteria.
* **GROUP BY** groups the remaining candidates.
* **SELECT** displays the required information.

WHERE always works on **individual rows**.

---

## Example

Employee Table

| employee_id | name   | salary | department |
| ----------- | ------ | ------ | ---------- |
| 1           | Harsha | 120000 | IT         |
| 2           | Ravi   | 90000  | HR         |
| 3           | Priya  | 150000 | Finance    |

Query

```sql
SELECT name,
       salary
FROM employees
WHERE salary > 100000;
```

Output

| name   | salary |
| ------ | ------ |
| Harsha | 120000 |
| Priya  | 150000 |

Rows that don't satisfy the condition are removed before further processing.

---

## WHERE vs HAVING

One of the most common SQL interview questions.

### WHERE

Filters **rows**.

```sql
SELECT *
FROM employees
WHERE salary > 100000;
```

---

### HAVING

Filters **groups**.

```sql
SELECT department,
       COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;
```

Easy way to remember:

```text
WHERE  → Rows

HAVING → Groups
```

---

## Can We Use Aggregate Functions In WHERE?

No.

Invalid:

```sql
SELECT department,
       COUNT(*)
FROM employees
WHERE COUNT(*) > 5
GROUP BY department;
```

Reason:

WHERE executes before GROUP BY.

At the WHERE stage, COUNT(*) has not been calculated yet.

Use HAVING instead.

---

## Using Functions In WHERE

Avoid applying functions directly on filtered columns.

Instead of:

```sql
SELECT *
FROM orders
WHERE YEAR(order_date) = 2025;
```

Prefer:

```sql
SELECT *
FROM orders
WHERE order_date >= '2025-01-01'
  AND order_date < '2026-01-01';
```

---

## Why Avoid Functions In WHERE?

Using functions on filter columns may prevent the database from efficiently using indexes or partition pruning.

Filtering directly on the original column allows the optimizer to scan only the required data.

---

## Production Scenario

Suppose an orders table is partitioned by `order_date`.

This query:

```sql
WHERE YEAR(order_date) = 2025
```

may force the database to evaluate every row.

Whereas:

```sql
WHERE order_date >= '2025-01-01'
  AND order_date < '2026-01-01'
```

allows the optimizer to scan only the required partitions.

This improves performance and reduces cloud cost.

---

## Common Mistakes

### Mistake 1

Using aggregate functions inside WHERE.

---

### Mistake 2

Confusing WHERE with HAVING.

---

### Mistake 3

Applying functions on indexed or partitioned columns.

---

### Mistake 4

Writing filters after GROUP BY mentally instead of understanding SQL execution order.

---

## Interview Explanation

A concise interview answer:

> "WHERE filters individual rows before grouping or aggregation. Since it executes before GROUP BY, aggregate functions cannot be used inside WHERE. In production, I also avoid applying functions on filtered columns because they may prevent efficient index usage or partition pruning."

---

## Key Takeaways

* WHERE filters rows.
* WHERE executes before GROUP BY.
* Aggregate functions cannot be used in WHERE.
* HAVING is used to filter groups.
* Avoid functions on indexed or partitioned columns.
* Filter using ranges whenever possible.
