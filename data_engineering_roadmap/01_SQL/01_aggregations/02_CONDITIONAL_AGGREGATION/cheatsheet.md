# Conditional Aggregation - Cheatsheet

---

# What is Conditional Aggregation?

Conditional aggregation applies aggregate functions only to rows that satisfy a condition.

It is commonly used to calculate multiple KPIs in a single query.

---

# Core Pattern

### Conditional Count

```sql
SUM(
    CASE
        WHEN condition THEN 1
        ELSE 0
    END
)
```

Example:

```sql
SUM(
    CASE
        WHEN salary > 100000 THEN 1
        ELSE 0
    END
) AS high_salary_count
```

---

### Conditional Sum

```sql
SUM(
    CASE
        WHEN condition THEN amount
        ELSE 0
    END
)
```

Example:

```sql
SUM(
    CASE
        WHEN status = 'SUCCESS' THEN amount
        ELSE 0
    END
) AS success_revenue
```

---

### Conditional Average

```sql
AVG(
    CASE
        WHEN condition THEN salary
    END
)
```

`AVG()` ignores `NULL`, so no `ELSE` is required.

---

# Mental Model

```text
Scan Rows

↓

CASE Creates Flags

↓

Matching Row

↓

1

Non-Matching Row

↓

0

↓

SUM

↓

Final Count
```

---

# Dashboard Pattern

```sql
SELECT
    COUNT(*) AS total_orders,

    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS success_orders,

    SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) AS failed_orders,

    SUM(CASE WHEN status = 'SUCCESS' THEN amount ELSE 0 END) AS success_revenue
FROM orders;
```

One query.

One table scan.

Multiple KPIs.

---

# Conditional Aggregation + GROUP BY

```sql
SELECT
    department,

    COUNT(*) AS total_employees,

    SUM(
        CASE
            WHEN salary > 100000 THEN 1
            ELSE 0
        END
    ) AS high_salary,

    SUM(
        CASE
            WHEN salary <= 100000 THEN 1
            ELSE 0
        END
    ) AS normal_salary

FROM employees
GROUP BY department;
```

---

# GROUP BY Mental Model

```text
Create Groups

↓

Inside Each Group

↓

Evaluate CASE

↓

SUM()

↓

One KPI Per Group
```

---

# COUNT(CASE) Pattern

```sql
COUNT(
    CASE
        WHEN condition THEN 1
    END
)
```

Works because:

```text
1

↓

Counted

NULL

↓

Ignored
```

---

# SUM(CASE) vs COUNT(CASE)

| SUM(CASE)         | COUNT(CASE)                    |
| ----------------- | ------------------------------ |
| Preferred         | Valid                          |
| More flexible     | Mainly for counting            |
| Explicit `ELSE 0` | Relies on `NULL` being ignored |

---

# Why Prefer SUM(CASE)?

```text
Counting

↓

1 / 0

----------------------

Summing

↓

Amount / 0

----------------------

Same Pattern

↓

Easy to Read

↓

Easy to Extend
```

---

# ELSE 0 vs No ELSE

Preferred:

```sql
SUM(
    CASE
        WHEN condition THEN 1
        ELSE 0
    END
)
```

Without `ELSE`:

```sql
SUM(
    CASE
        WHEN condition THEN 1
    END
)
```

SQL treats it as:

```sql
ELSE NULL
```

`SUM()` ignores `NULL`, so both usually work.

Prefer `ELSE 0` for readability.

---

# Production Best Practices

✅ Calculate multiple KPIs in one query.

✅ Prefer `SUM(CASE...)`.

✅ Use meaningful aliases.

✅ Pay attention to boundary conditions (`>` vs `>=`, `<` vs `<=`).

✅ Combine with `GROUP BY` for category-wise metrics.

---

# Common Mistakes

❌ Writing multiple queries instead of one.

❌ Forgetting `ELSE 0`.

❌ Missing boundary values.

❌ Using `WHERE` when conditional aggregation is required.

❌ Forgetting `GROUP BY` when metrics are required per category.

---

# Quick Revision

```text
Conditional Aggregation

↓

CASE

↓

Create Flags

↓

SUM

↓

Count

----------------------

CASE

↓

Return Amount

↓

SUM

↓

Revenue

----------------------

One Query

↓

Many KPIs

----------------------

GROUP BY

↓

KPIs Per Group

----------------------

Preferred Pattern

↓

SUM(CASE WHEN condition THEN value ELSE 0 END)
```
