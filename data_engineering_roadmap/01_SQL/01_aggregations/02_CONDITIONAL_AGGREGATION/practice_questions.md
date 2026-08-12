# Conditional Aggregation - Practice Questions

> Goal: Master conditional aggregation by reasoning through real-world KPI and reporting scenarios.
>
> Rule: Try answering first before looking at the answer.

================================================================================

# 🟢 LEVEL 1 - FUNDAMENTALS

================================================================================

## Question 1

Business requirement:

> Count employees earning more than ₹100000.

Write the conditional aggregation expression.

---

Answer:

```sql
SUM(
    CASE
        WHEN salary > 100000 THEN 1
        ELSE 0
    END
)
```

================================================================================

## Question 2

Given:

| Employee | Salary |
| -------- | -----: |
| Harsha   | 120000 |
| Ravi     |  90000 |
| Priya    | 150000 |
| Amit     |  80000 |

What values does the following CASE expression produce?

```sql
CASE
    WHEN salary > 100000 THEN 1
    ELSE 0
END
```

---

Answer:

| Employee | CASE Result |
| -------- | ----------: |
| Harsha   |           1 |
| Ravi     |           0 |
| Priya    |           1 |
| Amit     |           0 |

`SUM()` would return:

```text
2
```

================================================================================

## Question 3

Business asks:

> Show:

* Employees earning more than ₹100000
* Employees earning ₹100000 or less

Can this be done in one query?

---

Answer:

Yes.

```sql
SELECT
    SUM(CASE WHEN salary > 100000 THEN 1 ELSE 0 END) AS high_salary,

    SUM(CASE WHEN salary <= 100000 THEN 1 ELSE 0 END) AS normal_salary
FROM employees;
```

================================================================================

## Question 4

Why is this better than writing two separate queries?

---

Answer:

Because both KPIs are calculated during a single scan of the table, reducing work and improving performance.

================================================================================

# 🟡 LEVEL 2 - INTERVIEW TRAPS

================================================================================

## Question 5

Review the following query.

```sql
SELECT
    SUM(
        CASE
            WHEN salary > 100000 THEN 1
        END
    ) AS high_salary
FROM employees;
```

Will it work?

Why?

---

Answer:

Yes.

The missing `ELSE` is treated as:

```sql
ELSE NULL
```

`SUM()` ignores `NULL`, so only matching rows contribute to the total.

================================================================================

## Question 6

Review the following query.

```sql
SELECT
    COUNT(
        CASE
            WHEN salary > 100000 THEN 1
        END
    )
FROM employees;
```

Will it work?

---

Answer:

Yes.

Matching rows return `1`.

Non-matching rows return `NULL`.

`COUNT(column)` ignores `NULL`, so it counts only matching rows.

================================================================================

## Question 7

Which pattern would you recommend for conditional counting?

```text
COUNT(CASE...)

OR

SUM(CASE...)
```

Why?

---

Answer:

Prefer:

```sql
SUM(CASE WHEN condition THEN 1 ELSE 0 END)
```

Reasons:

* Easier to read
* More flexible
* Same pattern works for sums and counts
* Widely used in production

================================================================================

## Question 8

Business asks:

> Calculate revenue only from successful orders.

Write the expression.

---

Answer:

```sql
SUM(
    CASE
        WHEN status = 'SUCCESS'
        THEN amount
        ELSE 0
    END
)
```

================================================================================

# 🔴 LEVEL 3 - GROUP BY + CONDITIONAL AGGREGATION

================================================================================

## Question 9

Business asks:

> For each department, show:

* Total employees
* Employees earning more than ₹100000

Write the query.

---

Answer:

```sql
SELECT
    department,

    COUNT(*) AS total_employees,

    SUM(
        CASE
            WHEN salary > 100000 THEN 1
            ELSE 0
        END
    ) AS high_salary

FROM employees
GROUP BY department;
```

================================================================================

## Question 10

Business asks:

> For each department, show:

* High salary employees
* Normal salary employees

Write the query.

---

Answer:

```sql
SELECT
    department,

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

================================================================================

## Question 11

Business asks:

> Build a dashboard showing:

* Total Orders
* Successful Orders
* Failed Orders
* Cancelled Orders
* Successful Revenue

Should you write five queries?

---

Answer:

No.

One query with conditional aggregation should calculate all KPIs.

================================================================================

## Question 12

Review the following query.

```sql
SELECT
    department,

    SUM(
        CASE
            WHEN salary > 100000 THEN 1
            ELSE 0
        END
    ) AS high_salary

FROM employees
GROUP BY department;
```

Explain conceptually what SQL does.

---

Answer:

Execution flow:

```text
Read Table

↓

Create Department Groups

↓

Evaluate CASE
Inside Each Group

↓

Generate 1 / 0 Flags

↓

SUM Flags

↓

Return One Row Per Department
```

================================================================================

# 🧠 MASTERY CHALLENGE

================================================================================

## Question 13

The `orders` table contains:

| order_id | status    | amount |
| -------: | --------- | -----: |
|        1 | SUCCESS   |   1000 |
|        2 | FAILED    |    500 |
|        3 | SUCCESS   |   2000 |
|        4 | CANCELLED |    700 |
|        5 | FAILED    |    300 |

Write one query that returns:

* Total Orders
* Successful Orders
* Failed Orders
* Cancelled Orders
* Successful Revenue
* Failed Revenue

---

Expected Answer

```sql
SELECT
    COUNT(*) AS total_orders,

    SUM(
        CASE
            WHEN status = 'SUCCESS'
            THEN 1
            ELSE 0
        END
    ) AS success_orders,

    SUM(
        CASE
            WHEN status = 'FAILED'
            THEN 1
            ELSE 0
        END
    ) AS failed_orders,

    SUM(
        CASE
            WHEN status = 'CANCELLED'
            THEN 1
            ELSE 0
        END
    ) AS cancelled_orders,

    SUM(
        CASE
            WHEN status = 'SUCCESS'
            THEN amount
            ELSE 0
        END
    ) AS success_revenue,

    SUM(
        CASE
            WHEN status = 'FAILED'
            THEN amount
            ELSE 0
        END
    ) AS failed_revenue

FROM orders;
```

================================================================================

# ✅ Completion Criteria

If you can confidently solve all 13 questions, you have mastered:

* Conditional counting
* Conditional summing
* `SUM(CASE...)`
* `COUNT(CASE...)`
* `GROUP BY` + Conditional Aggregation
* Dashboard KPI generation
* One-query reporting patterns
* Production SQL reporting techniques
