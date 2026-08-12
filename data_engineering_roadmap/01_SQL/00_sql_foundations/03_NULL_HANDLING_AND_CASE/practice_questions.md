# NULL Handling & CASE - Practice Questions

> Goal: Test your understanding of NULL handling, COALESCE, aggregate functions, CASE expressions, and conditional aggregation.
>
> Rule: Try answering first before looking at the answer.

================================================================================

# 🟢 LEVEL 1 - FUNDAMENTALS

================================================================================

## Question 1

```sql
SELECT *
FROM employees
WHERE bonus = NULL;
```

Will this query return rows where `bonus` is NULL?

Why?

---

Answer:

❌ No.

Comparisons with NULL return **UNKNOWN**.

The WHERE clause keeps only rows where the condition is **TRUE**.

Use:

```sql
WHERE bonus IS NULL;
```

instead.

================================================================================

## Question 2

```sql
SELECT *
FROM employees
WHERE bonus <> NULL;
```

What will this query return?

---

Answer:

❌ No rows.

`bonus <> NULL` also evaluates to **UNKNOWN** for every row.

Always use:

```sql
WHERE bonus IS NOT NULL;
```

================================================================================

## Question 3

Review this query.

```sql
SELECT
    salary + bonus AS total_salary
FROM employees;
```

Would you approve it?

---

Answer:

⚠ Only if `bonus` is guaranteed to be NOT NULL.

Otherwise:

```text
salary + NULL

↓

NULL
```

Safer version:

```sql
SELECT
    salary + COALESCE(bonus, 0) AS total_salary
FROM employees;
```

================================================================================

## Question 4

What does the following return?

```sql
SELECT
    COALESCE(NULL, NULL, 100, 200);
```

---

Answer:

```text
100
```

`COALESCE` returns the first non-NULL value.

================================================================================

# 🟡 LEVEL 2 - INTERVIEW TRAPS

================================================================================

## Question 5

Suppose every value in `bonus` is NULL.

What is the result?

```sql
SELECT COUNT(*)
FROM employees;
```

---

Answer:

Returns the total number of rows.

`COUNT(*)` counts rows, not values.

================================================================================

## Question 6

Suppose every value in `bonus` is NULL.

What is the result?

```sql
SELECT COUNT(bonus)
FROM employees;
```

---

Answer:

```text
0
```

`COUNT(column)` counts only non-NULL values.

================================================================================

## Question 7

Suppose every value in `bonus` is NULL.

What does this return?

```sql
SELECT
    SUM(bonus),
    AVG(bonus),
    MIN(bonus),
    MAX(bonus)
FROM employees;
```

---

Answer:

```text
SUM → NULL

AVG → NULL

MIN → NULL

MAX → NULL
```

Aggregate functions ignore NULL values.

When every value is NULL, there are no values to aggregate.

================================================================================

## Question 8

Review this query.

```sql
CASE
    WHEN salary >= 50000 THEN 'Medium'
    WHEN salary >= 100000 THEN 'High'
    WHEN salary >= 150000 THEN 'Excellent'
END
```

Would you approve it?

---

Answer:

❌ No.

CASE evaluates from top to bottom.

A salary of 160000 matches the first condition and returns:

```text
Medium
```

Correct order:

```sql
CASE
    WHEN salary >= 150000 THEN 'Excellent'
    WHEN salary >= 100000 THEN 'High'
    WHEN salary >= 50000 THEN 'Medium'
    ELSE 'Low'
END
```

================================================================================

# 🔴 LEVEL 3 - PRODUCTION THINKING

================================================================================

## Question 9

Review this query.

```sql
SELECT
    department,
    COUNT(*)
FROM employees
WHERE salary >= 100000
GROUP BY department;
```

Business requirement:

> Show total employees and employees earning at least ₹100000 for every department.

Would you approve it?

---

Answer:

❌ No.

The WHERE clause removes employees earning less than ₹100000 before grouping.

Departments with no high-salary employees may disappear completely.

Use conditional aggregation instead.

================================================================================

## Question 10

Rewrite the query using conditional aggregation.

---

Answer:

```sql
SELECT
    department,
    COUNT(*) AS total_employees,
    SUM(
        CASE
            WHEN salary >= 100000 THEN 1
            ELSE 0
        END
    ) AS high_salary_employees
FROM employees
GROUP BY department;
```

================================================================================

## Question 11

Review this query.

```sql
SUM(
    CASE
        WHEN salary >= 100000 THEN 1
    END
)
```

Would you approve it?

---

Answer:

⚠ It depends on the business requirement.

Without `ELSE 0`, CASE returns NULL for non-matching rows.

If every row in a group returns NULL:

```text
SUM(NULL)

↓

NULL
```

Most dashboards expect:

```text
0
```

Safer version:

```sql
SUM(
    CASE
        WHEN salary >= 100000 THEN 1
        ELSE 0
    END
)
```

================================================================================

## Question 12

Review this query.

```sql
SELECT
    CASE
        WHEN department = 'IT' THEN 'Technology'
    END AS department_name
FROM employees;
```

Would you approve it?

---

Answer:

⚠ Only if returning NULL for every non-IT employee is acceptable.

Otherwise include:

```sql
ELSE department
```

or another appropriate default value.

================================================================================

# 🧠 MASTERY CHALLENGE

================================================================================

## Question 13

Review the following query like a Senior Data Engineer.

```sql
SELECT
    department,
    SUM(
        CASE
            WHEN bonus > 10000 THEN 1
        END
    ) AS high_bonus_count,
    AVG(bonus) AS average_bonus
FROM employees
GROUP BY department;
```

Identify every potential concern before approving the query.

---

Expected Answer

Observations:

1. `SUM(CASE...)` should include `ELSE 0` if the business expects `0` instead of `NULL`.

2. `AVG(bonus)` ignores NULL values. Verify this matches the business requirement.

3. If every bonus in a department is NULL:

```text
high_bonus_count

↓

NULL
```

```text
average_bonus

↓

NULL
```

If the report expects zeros:

```sql
COALESCE(
    AVG(bonus),
    0
)
```

may be required.

Always confirm the desired business behavior for missing values.

================================================================================

# ✅ Completion Criteria

If you can confidently answer all 13 questions without looking at the answers, you have mastered:

* NULL Handling
* Three-Valued Logic
* IS NULL / IS NOT NULL
* COALESCE
* Aggregate Functions with NULL
* CASE Expressions
* CASE Evaluation Order
* Conditional Aggregation
* Production SQL Best Practices
