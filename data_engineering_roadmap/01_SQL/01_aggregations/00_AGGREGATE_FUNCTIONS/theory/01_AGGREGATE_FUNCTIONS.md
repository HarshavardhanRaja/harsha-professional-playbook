# Aggregate Functions

## What are Aggregate Functions?

Aggregate functions perform calculations on **multiple rows** and return a **single result**.

Unlike normal functions that operate on one row at a time, aggregate functions summarize a set of rows.

Example:

```sql
SELECT
    COUNT(*)
FROM employees;
```

Result:

```text
125
```

The query returns a single value representing the total number of employees.

---

## Common Aggregate Functions

| Function | Purpose                        |
| -------- | ------------------------------ |
| COUNT()  | Counts rows or non-NULL values |
| SUM()    | Adds numeric values            |
| AVG()    | Calculates the average         |
| MIN()    | Returns the smallest value     |
| MAX()    | Returns the largest value      |

---

## COUNT(*)

Counts **every row** in the result set.

Example:

```sql
SELECT
    COUNT(*)
FROM employees;
```

If the table contains:

| Employee |
| -------- |
| Harsha   |
| Ravi     |
| Priya    |
| Amit     |

Result:

```text
4
```

NULL values do not matter because COUNT(*) counts rows.

---

## COUNT(column)

Counts only **non-NULL** values.

Example:

```sql
SELECT
    COUNT(bonus)
FROM employees;
```

Table:

| Bonus |
| ----: |
| 10000 |
|  NULL |
|  5000 |
|  NULL |

Result:

```text
2
```

NULL values are ignored.

---

## COUNT(DISTINCT column)

Counts unique non-NULL values.

Example:

```sql
SELECT
    COUNT(DISTINCT department)
FROM employees;
```

Table:

| Department |
| ---------- |
| IT         |
| IT         |
| HR         |
| Finance    |
| NULL       |
| NULL       |

Step 1:

DISTINCT produces:

```text
IT

HR

Finance

NULL
```

Step 2:

COUNT ignores NULL.

Result:

```text
3
```

---

## SUM()

Adds all non-NULL values.

Example:

```sql
SELECT
    SUM(salary)
FROM employees;
```

Table:

| Salary |
| -----: |
|    100 |
|    200 |
|   NULL |
|    300 |

Result:

```text
600
```

NULL values are ignored.

---

## AVG()

Calculates the average of all non-NULL values.

Example:

```sql
SELECT
    AVG(salary)
FROM employees;
```

Table:

| Salary |
| -----: |
|    100 |
|    200 |
|   NULL |
|    300 |

Conceptually:

```text
SUM(salary)

↓

600

----------------

COUNT(salary)

↓

3

----------------

AVG

↓

600 / 3

↓

200
```

Notice that AVG uses **COUNT(column)**, not **COUNT(*)**.

---

## MIN()

Returns the smallest non-NULL value.

Example:

```sql
SELECT
    MIN(salary)
FROM employees;
```

Result:

```text
100
```

---

## MAX()

Returns the largest non-NULL value.

Example:

```sql
SELECT
    MAX(salary)
FROM employees;
```

Result:

```text
300
```

---

# How SQL Conceptually Computes Aggregate Functions

Understanding how SQL computes aggregates helps explain their performance and behavior.

---

## COUNT(*)

SQL scans every row and increments a counter.

Conceptually:

```text
Row 1

↓

Count = 1

↓

Row 2

↓

Count = 2

↓

...

↓

Final Count
```

---

## SUM()

SQL maintains a running total.

Conceptually:

```text
Current Sum = 0

↓

100

↓

300

↓

600
```

---

## AVG()

AVG is conceptually calculated as:

```text
SUM(column)

↓

COUNT(column)

↓

SUM / COUNT
```

This explains why AVG ignores NULL values.

---

## MIN()

SQL maintains the smallest value seen so far.

Conceptually:

```text
Current Min = NULL

↓

100

↓

Current Min = 100

↓

200

↓

Still 100

↓

50

↓

Current Min = 50
```

Sorting is not required.

---

## MAX()

SQL maintains the largest value seen so far.

Conceptually:

```text
Current Max = NULL

↓

100

↓

Current Max = 100

↓

300

↓

Current Max = 300
```

---

## COUNT(DISTINCT)

Unlike other aggregates, SQL must identify unique values before counting.

Conceptually:

```text
101

↓

Seen = {101}

↓

205

↓

Seen = {101,205}

↓

101

↓

Already Exists

Ignore

↓

310

↓

Seen = {101,205,310}
```

Finally:

```text
Count = 3
```

Because SQL must track unique values, COUNT(DISTINCT) is more expensive than COUNT(*).

---

## NULL Handling

Aggregate functions treat NULL values differently.

| Function               | NULL Handling   |
| ---------------------- | --------------- |
| COUNT(*)               | Counts all rows |
| COUNT(column)          | Ignores NULL    |
| COUNT(DISTINCT column) | Ignores NULL    |
| SUM                    | Ignores NULL    |
| AVG                    | Ignores NULL    |
| MIN                    | Ignores NULL    |
| MAX                    | Ignores NULL    |

---

## Aggregate Execution

Aggregate functions execute after:

```text
FROM

↓

WHERE
```

but before:

```text
SELECT Output
```

This is why aggregate functions cannot be used inside the WHERE clause.

You'll learn this in detail with GROUP BY and HAVING.

---

## Performance Considerations

### COUNT(*)

Very efficient.

Simply counts rows.

---

### COUNT(DISTINCT)

More expensive.

SQL must:

* Detect duplicates
* Track unique values
* Use additional memory
* Perform hashing or sorting internally

---

### AVG()

Prefer using AVG() instead of manually writing:

```sql
SUM(column) / COUNT(column)
```

AVG handles NULL values correctly and avoids common mistakes such as integer division in some databases.

---

## Production Best Practices

### Use AVG()

Instead of manually calculating averages.

---

### Understand COUNT()

Remember:

```text
COUNT(*)

↓

Rows

------------------

COUNT(column)

↓

Non-NULL Values
```

---

### Be Careful with COUNT(DISTINCT)

On very large tables, COUNT(DISTINCT) can become expensive.

Only use it when uniqueness is required.

---

### Remember NULL Behavior

Every aggregate except COUNT(*) ignores NULL values.

---

## Common Mistakes

### Mistake 1

Assuming COUNT(*) and COUNT(column) always return the same value.

---

### Mistake 2

Assuming AVG divides by all rows.

It divides by the number of **non-NULL** values.

---

### Mistake 3

Thinking MIN() and MAX() sort the data.

They simply keep track of the current minimum or maximum while scanning rows.

---

### Mistake 4

Using COUNT(DISTINCT) unnecessarily.

It is significantly more expensive than COUNT(*).

---

## Interview Explanation

A concise interview answer:

> "Aggregate functions summarize multiple rows into a single result. COUNT(*) counts rows, while COUNT(column) counts only non-NULL values. AVG is conceptually computed as SUM divided by COUNT(column), which explains why it ignores NULL values. MIN and MAX track the smallest and largest values during a single scan, while COUNT(DISTINCT) is more expensive because SQL must identify unique values before counting."

---

## Key Takeaways

* Aggregate functions summarize multiple rows.
* COUNT(*) counts rows.
* COUNT(column) ignores NULL values.
* COUNT(DISTINCT) counts unique non-NULL values.
* AVG is conceptually SUM ÷ COUNT(column).
* MIN and MAX do not require sorting.
* COUNT(DISTINCT) is more expensive than COUNT(*).
* Most aggregate functions ignore NULL values.
