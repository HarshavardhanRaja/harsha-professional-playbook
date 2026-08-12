# GROUP BY & HAVING - Cheatsheet

---

# GROUP BY

`GROUP BY` groups rows having the same value in one or more columns.

It allows aggregate functions to execute **independently for each group**.

Example:

```sql
SELECT
    department,
    COUNT(*)
FROM employees
GROUP BY department;
```

---

# Why GROUP BY?

Without `GROUP BY`:

```sql
COUNT(*)
```

↓

One result for the **entire table**

With `GROUP BY`:

```sql
COUNT(*)
```

↓

One result for **each group**

---

# Mental Model

```text
One Big Table

↓

Identify Unique Groups

↓

Split Into Buckets

↓

Run Aggregate Function
On Each Bucket

↓

Return One Row Per Group
```

---

# Aggregate Functions Per Group

```sql
COUNT(*)

SUM()

AVG()

MIN()

MAX()
```

Each aggregate runs independently inside every group.

---

# Golden Rule

After `GROUP BY`:

Every selected column must be:

✅ In the `GROUP BY`

OR

✅ Wrapped inside an aggregate function

---

# Invalid Query

```sql
SELECT
    department,
    salary
FROM employees
GROUP BY department;
```

❌ Invalid

Reason:

```text
salary

↓

Multiple values exist
inside one department.

SQL doesn't know
which one to return.
```

---

# Valid Query

```sql
SELECT
    department,
    MAX(salary)
FROM employees
GROUP BY department;
```

`MAX()` reduces multiple salaries into one value.

---

# One Row Per Group

```text
IT

↓

3 Employees

↓

One Output Row

--------------------

HR

↓

1 Employee

↓

One Output Row

--------------------

Finance

↓

2 Employees

↓

One Output Row
```

---

# HAVING

`HAVING` filters groups after aggregation.

Example:

```sql
SELECT
    department,
    COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 2;
```

---

# WHERE vs HAVING

| WHERE                 | HAVING             |
| --------------------- | ------------------ |
| Filters rows          | Filters groups     |
| Before GROUP BY       | After GROUP BY     |
| Cannot use aggregates | Can use aggregates |

---

# Use WHERE For

```sql
salary > 100000

department = 'IT'

bonus IS NULL
```

These are **row-level filters**.

---

# Use HAVING For

```sql
COUNT(*) > 5

AVG(salary) > 100000

SUM(sales) > 1000000
```

These are **group-level filters**.

---

# Execution Order

```text
FROM

↓

WHERE

↓

GROUP BY

↓

Aggregate Functions

↓

HAVING

↓

SELECT

↓

ORDER BY

↓

LIMIT
```

---

# Invalid Query

```sql
WHERE COUNT(*) > 2
```

❌ Invalid

Reason:

```text
WHERE

↓

Before GROUP BY

↓

COUNT(*) doesn't exist yet.
```

---

# Correct Query

```sql
HAVING COUNT(*) > 2
```

✅ Valid

Reason:

```text
GROUP BY

↓

Aggregate Functions

↓

HAVING
```

The count now exists.

---

# WHERE + HAVING

```sql
SELECT
    department,
    AVG(salary)
FROM employees
WHERE salary > 50000
GROUP BY department
HAVING AVG(salary) > 100000;
```

Flow:

```text
Filter Rows

↓

Create Groups

↓

Calculate Average

↓

Filter Groups
```

---

# Production Best Practices

✅ Filter rows using `WHERE` whenever possible.

✅ Filter aggregates using `HAVING`.

✅ Every selected column must be grouped or aggregated.

✅ Remember that `GROUP BY` returns **one row per group**, not one row per original record.

---

# Common Mistakes

❌ Selecting non-grouped columns

❌ Using aggregates in `WHERE`

❌ Using `HAVING` for row-level filtering

❌ Forgetting that aggregation happens after grouping

---

# Quick Revision

```text
GROUP BY

↓

Create Groups

----------------------

Aggregate

↓

One Value Per Group

----------------------

Golden Rule

↓

Grouped

OR

Aggregated

----------------------

WHERE

↓

Rows

↓

Before GROUP BY

----------------------

HAVING

↓

Groups

↓

After GROUP BY

----------------------

GROUP BY

↓

One Output Row
Per Group
```
