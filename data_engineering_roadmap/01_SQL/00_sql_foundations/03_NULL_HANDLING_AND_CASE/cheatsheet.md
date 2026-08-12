# NULL Handling & CASE - Cheatsheet

---

# NULL

## NULL Means

```text
Unknown

or

Missing Value
```

NULL is **not**:

* 0
* Empty String (`''`)
* FALSE

---

# Three-Valued Logic

SQL has three logical values.

```text
TRUE

FALSE

UNKNOWN
```

Comparisons with NULL return:

```text
UNKNOWN
```

---

# NULL Comparisons

❌ Never write:

```sql
WHERE column = NULL
```

```sql
WHERE column <> NULL
```

✅ Always write:

```sql
WHERE column IS NULL
```

```sql
WHERE column IS NOT NULL
```

---

# WHERE Clause

The WHERE clause keeps only:

```text
TRUE
```

Rows evaluating to:

```text
FALSE

UNKNOWN
```

are discarded.

---

# COALESCE

Returns the **first non-NULL value**.

```sql
COALESCE(value1, value2, value3)
```

Example:

```sql
COALESCE(NULL, NULL, 100, 200)
```

Result:

```text
100
```

---

## Common Use

```sql
salary + COALESCE(bonus, 0)
```

Prevents calculations from returning NULL.

---

# Aggregate Functions

| Function      | NULL Handling          |
| ------------- | ---------------------- |
| COUNT(*)      | Counts all rows        |
| COUNT(column) | Counts non-NULL values |
| SUM           | Ignores NULL           |
| AVG           | Ignores NULL           |
| MIN           | Ignores NULL           |
| MAX           | Ignores NULL           |

---

## All NULL Values

| Function      | Result      |
| ------------- | ----------- |
| COUNT(*)      | Counts rows |
| COUNT(column) | 0           |
| SUM           | NULL        |
| AVG           | NULL        |
| MIN           | NULL        |
| MAX           | NULL        |

---

# CASE

Think of CASE as:

```text
IF

↓

THEN

↓

ELSE
```

Example:

```sql
CASE
    WHEN salary >= 100000 THEN 'High'
    ELSE 'Normal'
END
```

---

# CASE Execution

CASE evaluates:

```text
Top

↓

Bottom
```

Stops at the **first matching condition**.

---

# Condition Order

❌ Avoid

```text
>=50000

>=100000

>=150000
```

✅ Prefer

```text
>=150000

>=100000

>=50000
```

Most specific → Least specific.

---

# ELSE

Without:

```sql
ELSE
```

SQL automatically returns:

```text
NULL
```

---

# Conditional Aggregation

Pattern to remember:

```sql
SUM(
    CASE
        WHEN condition THEN 1
        ELSE 0
    END
)
```

Used for:

* KPIs
* Dashboards
* Reports
* Conditional Counts

---

# CASE vs COALESCE

Use **CASE** for business logic.

```sql
CASE
WHEN condition THEN value
ELSE value
END
```

Use **COALESCE** for replacing NULL values.

```sql
COALESCE(column, default_value)
```

---

# Production Best Practices

✅ Use `IS NULL` and `IS NOT NULL`

✅ Use `COALESCE()` before calculations

✅ Remember `COUNT(*)` ≠ `COUNT(column)`

✅ Order CASE conditions from most specific to least specific

✅ Use `ELSE` when a default value is expected

✅ Use:

```sql
SUM(
CASE
WHEN condition THEN 1
ELSE 0
END
)
```

for conditional counting

---

# Common Mistakes

❌ Using:

```sql
WHERE column = NULL
```

❌ Treating NULL as zero

❌ Forgetting `COALESCE` in calculations

❌ Forgetting `ELSE` in CASE

❌ Writing CASE conditions in the wrong order

---

# Quick Revision

```text
NULL
↓

Unknown Value

----------------------

IS NULL

↓

Check Missing Values

----------------------

COALESCE

↓

First Non-NULL Value

----------------------

COUNT(*)

↓

All Rows

----------------------

COUNT(column)

↓

Non-NULL Rows

----------------------

SUM / AVG / MIN / MAX

↓

Ignore NULL

----------------------

CASE

↓

IF-ELSE

----------------------

CASE

↓

Top to Bottom

↓

First Match Wins

----------------------

Conditional Count

↓

SUM(
CASE
WHEN condition THEN 1
ELSE 0
END
)
```
