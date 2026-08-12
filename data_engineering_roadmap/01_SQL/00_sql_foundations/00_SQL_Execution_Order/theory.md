# SQL Execution Order

## What Is SQL Execution Order?

Although SQL queries are written from top to bottom, SQL does not execute them in that order.

Example:

```sql
SELECT name
FROM employees
WHERE salary > 100000;
```

Most beginners assume SQL executes:

1. SELECT
2. FROM
3. WHERE

This is incorrect.

SQL follows a logical execution order.

---

## Why Do We Need To Understand It?

Understanding execution order helps explain:

- Why aliases don't work in WHERE
- Why aliases work in ORDER BY
- Difference between WHERE and HAVING
- Why aggregate functions fail in WHERE
- Window function limitations
- Many SQL interview questions

---

## Actual SQL Execution Order

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

## Mental Model

Think of SQL as a restaurant.

### FROM

Bring ingredients.

### JOIN

Combine ingredients.

### WHERE

Throw away bad ingredients.

### GROUP BY

Create baskets of ingredients.

### HAVING

Remove unwanted baskets.

### SELECT

Choose what to serve.

### DISTINCT

Remove duplicates.

### ORDER BY

Arrange dishes.

### LIMIT

Serve only requested dishes.

---

## Rows → Groups → Output

### Rows Stage

```text
FROM
JOIN
WHERE
```

Question:

Which rows do I want?

---

### Groups Stage

```text
GROUP BY
HAVING
```

Question:

Which groups do I want?

---

### Output Stage

```text
SELECT
DISTINCT
ORDER BY
LIMIT
```

Question:

What should I display?

---

## Real World Example

Business asks:

"Show departments having more than 10 employees."

SQL process:

1. Read employee table
2. Group employees by department
3. Count employees in each department
4. Keep departments having more than 10 employees
5. Display result

Query:

```sql
SELECT department,
       COUNT(*) AS employee_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 10;
```

---

## Deep Dive

### Why Alias Doesn't Work In WHERE

Invalid:

```sql
SELECT salary AS sal
FROM employees
WHERE sal > 100000;
```

Reason:

WHERE executes before SELECT.

At the WHERE stage:

```text
sal does not exist.
```

---

### Why Alias Works In ORDER BY

Valid:

```sql
SELECT salary AS sal
FROM employees
ORDER BY sal;
```

Reason:

ORDER BY executes after SELECT.

Alias already exists.

---

### Why Aggregate Functions Fail In WHERE

Invalid:

```sql
SELECT department,
       COUNT(*)
FROM employees
WHERE COUNT(*) > 10
GROUP BY department;
```

Reason:

COUNT(*) becomes available only after grouping.

WHERE executes before grouping.

---

### Why Aggregate Functions Work In HAVING

Valid:

```sql
SELECT department,
       COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 10;
```

Reason:

HAVING executes after GROUP BY.

---

## Common Mistakes

### Mistake 1

Using aliases in WHERE.

```sql
WHERE alias_name > 100
```

---

### Mistake 2

Using aggregates in WHERE.

```sql
WHERE COUNT(*) > 10
```

---

### Mistake 3

Confusing WHERE and HAVING.

WHERE → Rows

HAVING → Groups

---

### Mistake 4

Thinking SQL executes top-to-bottom.

It does not.

---

## Interview Explanation

A concise interview answer:

"SQL follows a logical execution order rather than the written order. SQL first identifies data sources, filters rows, creates groups, filters groups, selects columns, removes duplicates, sorts the result, and finally limits the output. Understanding execution order explains alias behavior, aggregate functions, and WHERE vs HAVING."