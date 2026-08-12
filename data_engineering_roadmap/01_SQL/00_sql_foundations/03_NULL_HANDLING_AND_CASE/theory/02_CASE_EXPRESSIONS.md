# CASE Expressions

## What is CASE?

`CASE` is SQL's conditional expression.

It allows you to return different values based on one or more conditions.

Think of it as SQL's equivalent of:

```text
IF

↓

THEN

↓

ELSE
```

Example:

```sql
SELECT
    employee_id,
    salary,
    CASE
        WHEN salary >= 100000 THEN 'High Salary'
        ELSE 'Normal Salary'
    END AS salary_category
FROM employees;
```

---

## How CASE Executes

CASE evaluates conditions **from top to bottom**.

As soon as one condition evaluates to TRUE, SQL returns that result and stops evaluating the remaining conditions.

Example:

```sql
CASE
    WHEN salary >= 150000 THEN 'Excellent'
    WHEN salary >= 100000 THEN 'High'
    WHEN salary >= 50000 THEN 'Medium'
    ELSE 'Low'
END
```

For a salary of **160000**:

```text
160000 >= 150000 ?

↓

TRUE

↓

Return "Excellent"

↓

STOP
```

The remaining conditions are never evaluated.

---

## ELSE Clause

The `ELSE` clause provides a default value when none of the conditions match.

Example:

```sql
CASE
    WHEN salary >= 100000 THEN 'High'
    ELSE 'Normal'
END
```

---

## What Happens Without ELSE?

If no `ELSE` clause is specified, SQL automatically returns:

```text
NULL
```

Example:

```sql
CASE
    WHEN salary >= 100000 THEN 'High'
END
```

Employees earning less than 100000 will receive:

```text
NULL
```

---

## Condition Order Matters

Incorrect:

```sql
CASE
    WHEN salary >= 50000 THEN 'Medium'
    WHEN salary >= 100000 THEN 'High'
    WHEN salary >= 150000 THEN 'Excellent'
END
```

A salary of **160000** satisfies the first condition:

```text
160000 >= 50000

↓

TRUE

↓

Return "Medium"

↓

STOP
```

The employee is incorrectly classified.

---

Correct:

```sql
CASE
    WHEN salary >= 150000 THEN 'Excellent'
    WHEN salary >= 100000 THEN 'High'
    WHEN salary >= 50000 THEN 'Medium'
    ELSE 'Low'
END
```

Always place **more specific conditions before broader conditions**.

---

## CASE in SELECT

Most commonly used to create derived columns.

Example:

```sql
SELECT
    employee_id,
    salary,
    CASE
        WHEN salary >= 100000 THEN 'High'
        ELSE 'Normal'
    END AS salary_band
FROM employees;
```

---

## CASE in ORDER BY

CASE can also control custom sorting.

Example:

```sql
SELECT *
FROM employees
ORDER BY
CASE
    WHEN department = 'IT' THEN 1
    WHEN department = 'Finance' THEN 2
    ELSE 3
END;
```

This allows business-defined ordering instead of alphabetical sorting.

---

## Conditional Aggregation

One of the most common production use cases.

Business asks:

> Show total employees and employees earning at least ₹100000 for each department.

Solution:

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

---

## Why ELSE 0?

Without:

```sql
ELSE 0
```

CASE returns:

```text
NULL
```

for non-matching rows.

Example:

```sql
SUM(
    CASE
        WHEN salary >= 100000 THEN 1
    END
)
```

For a department where nobody earns at least ₹100000:

```text
NULL

NULL

NULL
```

↓

```text
SUM(NULL)

↓

NULL
```

Instead of:

```text
0
```

Using:

```sql
ELSE 0
```

ensures:

```text
SUM(0,0,0)

↓

0
```

which is usually what the business expects.

---

## CASE vs COALESCE

Use **CASE** when making decisions based on conditions.

Example:

```sql
CASE
    WHEN salary >= 100000 THEN 'High'
    ELSE 'Normal'
END
```

Use **COALESCE** when replacing NULL values.

Example:

```sql
COALESCE(bonus, 0)
```

---

## Production Best Practices

### Order Conditions Carefully

CASE stops at the first match.

Always place the most restrictive conditions first.

---

### Always Consider ELSE

If a default value is expected, include an ELSE clause.

Otherwise SQL returns NULL.

---

### Use CASE for Business Logic

CASE is excellent for:

* Categorization
* KPI calculations
* Report labels
* Dashboard metrics
* Conditional aggregation

---

### Use Conditional Aggregation

Pattern to remember:

```sql
SUM(
    CASE
        WHEN condition THEN 1
        ELSE 0
    END
)
```

This is one of the most common SQL interview and production patterns.

---

## Common Mistakes

### Mistake 1

Incorrect condition order.

---

### Mistake 2

Forgetting that CASE stops at the first match.

---

### Mistake 3

Omitting ELSE when a default value is required.

---

### Mistake 4

Using nested CASE expressions when a single CASE is sufficient.

---

## Interview Explanation

A concise interview answer:

> "CASE is SQL's conditional expression used to implement business logic. SQL evaluates CASE from top to bottom and stops at the first matching condition. I always order overlapping conditions from most specific to least specific. For reporting and dashboards, I frequently use conditional aggregation with `SUM(CASE WHEN condition THEN 1 ELSE 0 END)`."

---

## Key Takeaways

* CASE works like IF-ELSE.
* CASE evaluates conditions from top to bottom.
* SQL stops at the first matching condition.
* Condition order matters.
* Without ELSE, SQL returns NULL.
* CASE is commonly used for categorization and reporting.
* `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` is a key interview and production pattern.
