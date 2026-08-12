# NULL Handling

## What is NULL?

`NULL` represents an **unknown** or **missing** value.

It does **not** mean:

* Zero (`0`)
* Empty string (`''`)
* False (`FALSE`)

It simply means that the value is currently unknown or unavailable.

Example:

| Employee | Bonus |
| -------- | ----: |
| Harsha   | 10000 |
| Ravi     |  NULL |
| Priya    |  5000 |

Here, Ravi's bonus is **unknown**, not zero.

---

## NULL vs 0

Consider the following table.

| Employee | Bonus |
| -------- | ----: |
| Harsha   | 10000 |
| Ravi     |     0 |
| Priya    |  NULL |

Ravi's bonus is known and equals **0**.

Priya's bonus is **unknown**.

These represent completely different business meanings.

---

## Why NULL is Special

SQL cannot compare unknown values.

Example:

```sql
NULL = NULL
```

Result:

```text
UNKNOWN
```

Similarly,

```sql
NULL <> NULL
```

also returns:

```text
UNKNOWN
```

Because SQL does not know whether two unknown values are equal.

---

## Three-Valued Logic

Unlike most programming languages, SQL has three logical values.

```text
TRUE

FALSE

UNKNOWN
```

Comparisons involving `NULL` usually return **UNKNOWN**.

---

## WHERE Clause Behavior

The `WHERE` clause only keeps rows where the condition evaluates to **TRUE**.

Rows evaluating to:

* FALSE
* UNKNOWN

are discarded.

Example:

```sql
SELECT *
FROM employees
WHERE bonus = NULL;
```

Returns:

```text
No rows
```

because:

```sql
bonus = NULL
```

evaluates to **UNKNOWN** for every row.

---

## IS NULL

To check whether a value is NULL, use:

```sql
SELECT *
FROM employees
WHERE bonus IS NULL;
```

This returns only rows where the bonus is missing.

---

## IS NOT NULL

To retrieve only existing values:

```sql
SELECT *
FROM employees
WHERE bonus IS NOT NULL;
```

This returns all rows where the bonus is known.

---

## Never Use = NULL

Incorrect:

```sql
WHERE bonus = NULL
```

Incorrect:

```sql
WHERE bonus <> NULL
```

Correct:

```sql
WHERE bonus IS NULL
```

Correct:

```sql
WHERE bonus IS NOT NULL
```

---

## COALESCE

`COALESCE()` returns the first non-NULL value.

Example:

```sql
SELECT
    employee_id,
    COALESCE(bonus, 0) AS bonus
FROM employees;
```

Output:

| Employee | Bonus |
| -------- | ----: |
| Harsha   | 10000 |
| Ravi     |     0 |
| Priya    |  5000 |

---

## How COALESCE Works

Example:

```sql
COALESCE(NULL, NULL, 100, 200)
```

Evaluation:

```text
NULL

↓

NULL

↓

100

↓

Return 100
```

SQL stops at the first non-NULL value.

---

## COALESCE in Calculations

Consider:

```sql
SELECT
    salary + bonus
FROM employees;
```

If `bonus` is NULL, the result becomes NULL.

Instead:

```sql
SELECT
    salary + COALESCE(bonus, 0)
FROM employees;
```

This replaces missing bonuses with zero before performing the calculation.

---

## Aggregate Functions and NULL

Most aggregate functions ignore NULL values.

Example:

| Function      | NULL Handling               |
| ------------- | --------------------------- |
| COUNT(*)      | Counts all rows             |
| COUNT(column) | Counts only non-NULL values |
| SUM           | Ignores NULL values         |
| AVG           | Ignores NULL values         |
| MIN           | Ignores NULL values         |
| MAX           | Ignores NULL values         |

---

## All NULL Values

Suppose every value is NULL.

| Bonus |
| ----: |
|  NULL |
|  NULL |
|  NULL |

Results:

| Function     | Result |
| ------------ | ------ |
| COUNT(*)     | 3      |
| COUNT(bonus) | 0      |
| SUM(bonus)   | NULL   |
| AVG(bonus)   | NULL   |
| MIN(bonus)   | NULL   |
| MAX(bonus)   | NULL   |

---

## Production Best Practices

### Always use IS NULL

Instead of:

```sql
WHERE column = NULL
```

Use:

```sql
WHERE column IS NULL
```

---

### Use COALESCE in Reports

Business users usually expect missing numeric values to appear as zero.

Example:

```sql
COALESCE(bonus, 0)
```

---

### Be Careful with Arithmetic

Example:

```sql
salary + bonus
```

If `bonus` is NULL:

```text
Result = NULL
```

Instead:

```sql
salary + COALESCE(bonus, 0)
```

---

### Understand Aggregate Behavior

Remember:

```text
COUNT(*)

↓

Counts rows

--------------------

COUNT(column)

↓

Counts non-NULL values

--------------------

SUM

AVG

MIN

MAX

↓

Ignore NULL values
```

---

## Common Mistakes

### Mistake 1

Treating NULL as zero.

---

### Mistake 2

Using:

```sql
WHERE column = NULL
```

---

### Mistake 3

Forgetting COALESCE during calculations.

---

### Mistake 4

Expecting SUM of all NULL values to return zero.

It returns NULL.

---

## Interview Explanation

A concise interview answer:

> "NULL represents an unknown or missing value, not zero. Comparisons with NULL return UNKNOWN, which is why `= NULL` and `<> NULL` don't work. SQL provides `IS NULL` and `IS NOT NULL` for NULL checks. I commonly use `COALESCE` to replace NULL values in calculations and reports. I also remember that `COUNT(*)` counts all rows, while `COUNT(column)` counts only non-NULL values."

---

## Key Takeaways

* NULL means unknown or missing.
* NULL is not zero or an empty string.
* Comparisons with NULL return UNKNOWN.
* WHERE keeps only TRUE.
* Use `IS NULL` and `IS NOT NULL`.
* Use `COALESCE` to replace NULL values.
* Aggregate functions ignore NULL values.
* `COUNT(*)` and `COUNT(column)` behave differently.
