# Aggregate Functions - Practice Questions

> Goal: Test your understanding of aggregate functions, NULL handling, COUNT variations, performance, and production scenarios.
>
> Rule: Try answering first before looking at the answer.

================================================================================

# 🟢 LEVEL 1 - FUNDAMENTALS

================================================================================

## Question 1

```sql
SELECT
    COUNT(*)
FROM employees;
```

What does `COUNT(*)` count?

---

Answer:

✅ `COUNT(*)` counts every row in the result set.

NULL values do not matter because it counts rows, not column values.

================================================================================

## Question 2

```sql
SELECT
    COUNT(bonus)
FROM employees;
```

What does `COUNT(bonus)` count?

---

Answer:

✅ `COUNT(bonus)` counts only non-NULL values in the `bonus` column.

================================================================================

## Question 3

Suppose the `salary` column contains:

```text
100
200
NULL
300
```

What will the following query return?

```sql
SELECT SUM(salary);
```

---

Answer:

```text
600
```

`SUM()` ignores NULL values.

================================================================================

## Question 4

Using the same data:

```text
100
200
NULL
300
```

What will the following query return?

```sql
SELECT AVG(salary);
```

---

Answer:

```text
200
```

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

================================================================================

# 🟡 LEVEL 2 - INTERVIEW TRAPS

================================================================================

## Question 5

Review the following query.

```sql
SELECT
    SUM(salary) / COUNT(*)
FROM employees;
```

Would you approve it?

Why?

---

Answer:

⚠ Not immediately.

Potential issues:

* `COUNT(*)` includes NULL rows.
* Manual average calculation can be incorrect.
* Some databases may perform integer division.

Preferred solution:

```sql
SELECT AVG(salary)
FROM employees;
```

================================================================================

## Question 6

Suppose the `department` column contains:

```text
IT
IT
HR
Finance
NULL
NULL
```

What will this return?

```sql
SELECT
COUNT(DISTINCT department)
FROM employees;
```

---

Answer:

```text
3
```

Reason:

Step 1:

DISTINCT produces:

```text
IT

HR

Finance

NULL
```

Step 2:

`COUNT(column)` ignores NULL.

Final answer:

```text
3
```

================================================================================

## Question 7

Review the following statement.

> "MIN() sorts the data and returns the first row."

Is this statement correct?

---

Answer:

❌ No.

`MIN()` scans the rows while maintaining the smallest value seen so far.

Sorting is not required.

================================================================================

## Question 8

Which aggregate function is generally more expensive?

```sql
COUNT(*)
```

or

```sql
COUNT(DISTINCT customer_id)
```

Explain why.

---

Answer:

`COUNT(DISTINCT customer_id)` is generally more expensive.

SQL must:

* Detect duplicate values
* Track unique values
* Use hashing or sorting
* Allocate additional memory

================================================================================

# 🔴 LEVEL 3 - PRODUCTION THINKING

================================================================================

## Question 9

Review the following query.

```sql
SELECT
    AVG(salary)
FROM employees;
```

Would you approve it over:

```sql
SELECT
    SUM(salary) / COUNT(*)
FROM employees;
```

Why?

---

Answer:

✅ Yes.

`AVG()`:

* Ignores NULL values correctly
* Avoids manual calculation mistakes
* Produces cleaner and more readable SQL
* Avoids integer division issues in some databases

================================================================================

## Question 10

Review the following query.

```sql
SELECT
    COUNT(*),
    COUNT(salary)
FROM employees;
```

When would these two values be different?

---

Answer:

They differ whenever the `salary` column contains NULL values.

Example:

| Salary |
| -----: |
|    100 |
|    200 |
|   NULL |
|    300 |

Results:

```text
COUNT(*)      = 4

COUNT(salary) = 3
```

================================================================================

## Question 11

A table contains **100 million rows**.

Business needs the total number of records.

Which query would you choose?

```sql
COUNT(*)
```

or

```sql
COUNT(DISTINCT customer_id)
```

---

Answer:

Use:

```sql
COUNT(*)
```

It performs a simple row count.

`COUNT(DISTINCT)` should only be used when uniqueness is actually required.

================================================================================

## Question 12

Review the following query.

```sql
SELECT
    MIN(salary),
    MAX(salary)
FROM employees;
```

How do you think SQL computes these values internally?

---

Answer:

SQL scans the rows once.

For `MIN()`:

* Maintain the current smallest value.

For `MAX()`:

* Maintain the current largest value.

Sorting the entire dataset is not required.

================================================================================

# 🧠 MASTERY CHALLENGE

================================================================================

## Question 13

Review the following query like a Senior Data Engineer.

```sql
SELECT
    COUNT(*),
    COUNT(bonus),
    COUNT(DISTINCT department),
    AVG(salary)
FROM employees;
```

Explain what each aggregate function is doing internally.

---

Expected Answer

```text
COUNT(*)

↓

Counts every row.

----------------------

COUNT(bonus)

↓

Counts only non-NULL bonus values.

----------------------

COUNT(DISTINCT department)

↓

Identify unique department values

↓

Ignore NULL

↓

Count remaining values.

----------------------

AVG(salary)

↓

SUM(salary)

↓

COUNT(salary)

↓

SUM / COUNT
```

Also note:

* All aggregates except `COUNT(*)` ignore NULL values.
* `COUNT(DISTINCT)` is the most computationally expensive among these functions.

================================================================================

# ✅ Completion Criteria

If you can confidently answer all 13 questions and explain how each aggregate function works conceptually, you have mastered:

* COUNT(*)
* COUNT(column)
* COUNT(DISTINCT)
* SUM()
* AVG()
* MIN()
* MAX()
* NULL handling in aggregates
* Aggregate performance
* Production best practices
