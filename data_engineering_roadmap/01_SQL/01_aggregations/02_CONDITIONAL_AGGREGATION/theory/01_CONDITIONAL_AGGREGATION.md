# Conditional Aggregation

## What is Conditional Aggregation?

Conditional aggregation means applying aggregate functions only for rows that satisfy a condition.

It is commonly used to calculate multiple business metrics in a single query.

Example:

```sql
SELECT
    COUNT(*) AS total_orders,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS success_orders,
    SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) AS failed_orders
FROM orders;
```

This query calculates multiple KPIs in one scan.

---

## Why Do We Need Conditional Aggregation?

Without conditional aggregation, we may write multiple queries.

Example:

```sql
SELECT COUNT(*)
FROM orders;
```

```sql
SELECT COUNT(*)
FROM orders
WHERE status = 'SUCCESS';
```

```sql
SELECT COUNT(*)
FROM orders
WHERE status = 'FAILED';
```

This works, but it scans the table multiple times.

Conditional aggregation lets us calculate all metrics in one query.

---

## Core Pattern

For counting conditionally:

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

## Mental Model

Think of conditional aggregation as creating temporary flags.

| Employee | Salary | Salary > 100000? | Flag |
| -------- | -----: | ---------------- | ---: |
| Harsha   | 120000 | Yes              |    1 |
| Ravi     |  90000 | No               |    0 |
| Priya    | 150000 | Yes              |    1 |
| Amit     |  80000 | No               |    0 |

Then SQL adds the flag column.

```text
1 + 0 + 1 + 0 = 2
```

So the count is:

```text
2
```

---

## Counting with SUM(CASE)

Example:

```sql
SELECT
    SUM(
        CASE
            WHEN salary > 100000 THEN 1
            ELSE 0
        END
    ) AS high_salary_count
FROM employees;
```

This returns the number of employees earning more than 100000.

---

## Counting Multiple Conditions

Business asks:

> Show employees earning more than 100000 and employees earning 100000 or less.

Query:

```sql
SELECT
    SUM(
        CASE
            WHEN salary > 100000 THEN 1
            ELSE 0
        END
    ) AS earn_more,

    SUM(
        CASE
            WHEN salary <= 100000 THEN 1
            ELSE 0
        END
    ) AS earn_less
FROM employees;
```

This returns both metrics in one query.

---

## Dashboard Example

Business asks:

> Show total orders, successful orders, failed orders, cancelled orders, and successful revenue.

Query:

```sql
SELECT
    COUNT(*) AS total_orders,

    SUM(
        CASE
            WHEN status = 'SUCCESS' THEN 1
            ELSE 0
        END
    ) AS success_orders,

    SUM(
        CASE
            WHEN status = 'FAILED' THEN 1
            ELSE 0
        END
    ) AS failed_orders,

    SUM(
        CASE
            WHEN status = 'CANCELLED' THEN 1
            ELSE 0
        END
    ) AS cancelled_orders,

    SUM(
        CASE
            WHEN status = 'SUCCESS' THEN amount
            ELSE 0
        END
    ) AS success_revenue
FROM orders;
```

This is a classic production use case.

One query can calculate many KPIs.

---

## Conditional Aggregation with GROUP BY

Conditional aggregation becomes even more powerful with `GROUP BY`.

Business asks:

> For each department, show total employees, employees earning more than 100000, and employees earning 100000 or less.

Query:

```sql
SELECT
    department,

    COUNT(*) AS total_employees,

    SUM(
        CASE
            WHEN salary > 100000 THEN 1
            ELSE 0
        END
    ) AS earn_more,

    SUM(
        CASE
            WHEN salary <= 100000 THEN 1
            ELSE 0
        END
    ) AS earn_less
FROM employees
GROUP BY department;
```

SQL creates department groups first, then calculates each metric inside every group.

---

## GROUP BY Mental Model

```text
Create Groups

↓

Inside Each Group

↓

Create CASE Flags

↓

SUM The Flags

↓

Return One Row Per Group
```

Example:

```text
IT Group

120000 → 1
150000 → 1
95000  → 0

SUM = 2
```

---

## COUNT(CASE) Pattern

Conditional counting can also be written using `COUNT(CASE...)`.

Example:

```sql
COUNT(
    CASE
        WHEN salary > 100000 THEN 1
    END
) AS high_salary_count
```

This works because:

```text
Matching rows     → 1      → counted

Non-matching rows → NULL   → ignored
```

---

## SUM(CASE) vs COUNT(CASE)

Both can work for conditional counting.

### COUNT(CASE)

```sql
COUNT(
    CASE
        WHEN condition THEN 1
    END
)
```

Counts only non-NULL CASE results.

---

### SUM(CASE)

```sql
SUM(
    CASE
        WHEN condition THEN 1
        ELSE 0
    END
)
```

Adds 1 for matching rows and 0 for non-matching rows.

---

## Which One Should You Prefer?

For interviews and production, prefer:

```sql
SUM(CASE WHEN condition THEN 1 ELSE 0 END)
```

Reasons:

* More explicit
* Easier to read
* Easier to extend
* Works for counting and summing
* Clearly shows what non-matching rows contribute

---

## Summing Conditionally

Conditional aggregation is not only for counting.

Business asks:

> What is the revenue from successful orders?

Query:

```sql
SELECT
    SUM(
        CASE
            WHEN status = 'SUCCESS' THEN amount
            ELSE 0
        END
    ) AS success_revenue
FROM orders;
```

Here, matching rows contribute the amount.

Non-matching rows contribute zero.

---

## Why ELSE 0 Matters

Without `ELSE 0`:

```sql
SUM(
    CASE
        WHEN salary > 100000 THEN 1
    END
)
```

SQL treats it as:

```sql
SUM(
    CASE
        WHEN salary > 100000 THEN 1
        ELSE NULL
    END
)
```

Since `SUM()` ignores NULL values, this may still return the correct count.

But using `ELSE 0` is clearer and safer.

Preferred:

```sql
SUM(
    CASE
        WHEN salary > 100000 THEN 1
        ELSE 0
    END
)
```

---

## Production Best Practices

### Use One Query for Multiple KPIs

Conditional aggregation helps avoid multiple table scans.

Good:

```sql
SELECT
    COUNT(*) AS total_orders,
    SUM(CASE WHEN status='SUCCESS' THEN 1 ELSE 0 END) AS success_orders,
    SUM(CASE WHEN status='FAILED' THEN 1 ELSE 0 END) AS failed_orders
FROM orders;
```

Avoid writing separate queries for each metric unless required.

---

### Use Clear Aliases

Good aliases make dashboards easier to understand.

```sql
success_orders
failed_orders
cancelled_orders
success_revenue
```

Avoid vague aliases like:

```sql
count1
count2
metric_a
```

---

### Always Check Boundary Conditions

Be careful with:

```sql
salary > 100000
```

vs

```sql
salary >= 100000
```

Business wording matters.

---

### Use ELSE 0

When using `SUM(CASE...)` for counts or totals, prefer `ELSE 0`.

It makes the intent clear.

---

## Common Mistakes

### Mistake 1

Using multiple queries instead of one conditional aggregation query.

---

### Mistake 2

Forgetting `ELSE 0`.

---

### Mistake 3

Using `<` instead of `<=` and missing boundary values.

---

### Mistake 4

Using `WHERE` and accidentally removing rows needed for other metrics.

---

### Mistake 5

Forgetting `GROUP BY` when metrics are required per category.

---

## Interview Explanation

A concise interview answer:

> "Conditional aggregation means combining aggregate functions with CASE expressions to calculate metrics only for rows matching certain conditions. The most common pattern is `SUM(CASE WHEN condition THEN 1 ELSE 0 END)`, which counts rows satisfying a condition. It is heavily used in dashboards because it allows multiple KPIs to be calculated in a single query and often in one scan of the table."

---

## Key Takeaways

* Conditional aggregation calculates conditional metrics.
* Main pattern: `SUM(CASE WHEN condition THEN 1 ELSE 0 END)`.
* It is useful for dashboards, reports, and KPIs.
* It avoids multiple scans of the same table.
* It works with `GROUP BY` for category-wise metrics.
* `SUM(CASE...)` is usually preferred over `COUNT(CASE...)`.
* Use `ELSE 0` for clarity and safer reporting.
