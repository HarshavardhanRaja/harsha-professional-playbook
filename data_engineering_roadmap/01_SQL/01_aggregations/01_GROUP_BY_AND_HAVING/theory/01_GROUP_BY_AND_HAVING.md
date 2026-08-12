# GROUP BY and HAVING

## What is GROUP BY?

`GROUP BY` is used to group rows that have the same value in one or more columns.

It allows aggregate functions like:

* `COUNT()`
* `SUM()`
* `AVG()`
* `MIN()`
* `MAX()`

to run independently for each group.

Example:

```sql
SELECT
    department,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department;
```

This returns the number of employees in each department.

---

## Why Do We Need GROUP BY?

Without `GROUP BY`, aggregate functions summarize the entire table.

Example:

```sql
SELECT COUNT(*)
FROM employees;
```

This returns one count for the whole table.

But if the business asks:

> "How many employees are there in each department?"

we need to split the data by department first.

That is why `GROUP BY` exists.

---

## Mental Model

Think of `GROUP BY` as creating buckets.

Original table:

| Employee | Department | Salary |
| -------- | ---------- | -----: |
| Harsha   | IT         | 120000 |
| Ravi     | HR         |  90000 |
| Priya    | IT         | 150000 |
| Amit     | Finance    |  80000 |
| Hari     | IT         |  95000 |
| Kiran    | Finance    | 130000 |

After:

```sql
GROUP BY department
```

SQL creates groups:

```text
IT
----------------
Harsha
Priya
Hari
```

```text
HR
----------------
Ravi
```

```text
Finance
----------------
Amit
Kiran
```

Then aggregate functions run independently inside each group.

---

## GROUP BY Execution Flow

Conceptually:

```text
One Big Table

↓

Identify Unique Groups

↓

Split Rows Into Buckets

↓

Run Aggregate Function On Each Bucket

↓

Return One Row Per Group
```

---

## Example 1: Count Employees Per Department

```sql
SELECT
    department,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department;
```

Output:

| Department | Employee Count |
| ---------- | -------------: |
| IT         |              3 |
| HR         |              1 |
| Finance    |              2 |

SQL does:

```text
IT       → COUNT(*) → 3
HR       → COUNT(*) → 1
Finance  → COUNT(*) → 2
```

---

## Example 2: Average Salary Per Department

```sql
SELECT
    department,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department;
```

SQL does:

```text
IT
120000, 150000, 95000
AVG → 121666.67

HR
90000
AVG → 90000

Finance
80000, 130000
AVG → 105000
```

---

## Golden Rule of GROUP BY

After `GROUP BY`, every selected column must produce exactly **one value per group**.

A selected column must be either:

1. Present in the `GROUP BY`
2. Wrapped inside an aggregate function

---

## Invalid Query

```sql
SELECT
    department,
    salary
FROM employees
GROUP BY department;
```

This query is invalid.

Why?

After grouping by department, SQL has multiple salaries inside each department.

For IT:

```text
120000
150000
95000
```

SQL does not know which salary to return.

`salary` is:

* Not in the `GROUP BY`
* Not aggregated

So the query fails.

---

## Valid Query

```sql
SELECT
    department,
    MAX(salary) AS max_salary
FROM employees
GROUP BY department;
```

This works because:

* `department` identifies the group
* `MAX(salary)` reduces many salaries into one value per group

---

## Multiple Aggregates

```sql
SELECT
    department,
    COUNT(*) AS employee_count,
    AVG(salary) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary
FROM employees
GROUP BY department;
```

This works because:

* `department` is grouped
* `COUNT(*)` returns one value per group
* `AVG(salary)` returns one value per group
* `MIN(salary)` returns one value per group
* `MAX(salary)` returns one value per group

Every selected expression produces one value per group.

---

## What is HAVING?

`HAVING` filters groups after aggregation.

Example:

```sql
SELECT
    department,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 2;
```

This returns only departments having more than 2 employees.

---

## Why Do We Need HAVING?

`WHERE` filters rows before grouping.

`HAVING` filters groups after grouping.

Business requirement:

> "Show departments having more than 2 employees."

This cannot be solved using `WHERE`, because the count does not exist before grouping.

---

## WHERE vs HAVING

### WHERE

Filters individual rows.

```sql
SELECT *
FROM employees
WHERE salary > 100000;
```

Use `WHERE` when filtering row-level data.

---

### HAVING

Filters grouped results.

```sql
SELECT
    department,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 100000;
```

Use `HAVING` when filtering aggregate results.

---

## Execution Order

For grouped queries, SQL logically executes like this:

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

This explains why aggregate functions cannot be used in `WHERE`.

---

## Invalid WHERE Example

```sql
SELECT
    department,
    COUNT(*) AS employee_count
FROM employees
WHERE COUNT(*) > 2
GROUP BY department;
```

This is invalid.

Reason:

`WHERE` executes before grouping.

At that point, `COUNT(*)` does not exist yet.

---

## Correct HAVING Example

```sql
SELECT
    department,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 2;
```

This works because `HAVING` executes after grouping and aggregation.

---

## WHERE and HAVING Together

Sometimes both are needed.

Business requirement:

> "Among employees earning more than 50000, show departments whose average salary is greater than 100000."

Query:

```sql
SELECT
    department,
    AVG(salary) AS avg_salary
FROM employees
WHERE salary > 50000
GROUP BY department
HAVING AVG(salary) > 100000;
```

Execution:

```text
1. FROM employees

2. WHERE salary > 50000
   Filter individual employees

3. GROUP BY department
   Create department groups

4. AVG(salary)
   Calculate average salary per group

5. HAVING AVG(salary) > 100000
   Filter groups

6. SELECT final columns
```

---

## Common Mistakes

### Mistake 1

Selecting a non-grouped, non-aggregated column.

```sql
SELECT department, name
FROM employees
GROUP BY department;
```

Invalid because `name` has multiple values inside each department.

---

### Mistake 2

Using aggregate functions in WHERE.

```sql
WHERE COUNT(*) > 2
```

Invalid because `WHERE` executes before aggregation.

---

### Mistake 3

Using HAVING for row-level filters.

```sql
HAVING salary > 100000
```

If the condition is row-level, use `WHERE`.

---

### Mistake 4

Forgetting that GROUP BY returns one row per group.

After grouping, SQL no longer returns one row per original record.

It returns one row per group.

---

## Interview Explanation

A concise interview answer:

> "`GROUP BY` groups rows that share the same values and allows aggregate functions to run independently for each group. After grouping, every selected column must either be part of the GROUP BY or be aggregated, because each group must produce exactly one output row. `WHERE` filters rows before grouping, while `HAVING` filters groups after aggregation."

---

## Key Takeaways

* `GROUP BY` creates groups of rows.
* Aggregate functions run independently inside each group.
* `GROUP BY` returns one row per group.
* Every selected column must be grouped or aggregated.
* `WHERE` filters rows.
* `HAVING` filters groups.
* Aggregate functions cannot be used in `WHERE`.
* Use `HAVING` to filter aggregate results.
