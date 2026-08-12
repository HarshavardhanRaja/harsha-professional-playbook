# DISTINCT

## What Is DISTINCT?

The `DISTINCT` keyword removes duplicate rows from the result set.

It tells SQL:

> "Return only unique values."

Example:

```sql
SELECT DISTINCT department
FROM employees;
```

Only unique department names are returned.

---

## Why Do We Need DISTINCT?

DISTINCT helps us:

* Remove duplicate values
* Retrieve unique records
* Simplify reports and dashboards
* Eliminate duplicate results from joins (only when appropriate)

---

## Mental Model

Think of a classroom attendance sheet.

```text
IT
HR
IT
Finance
HR
```

Applying DISTINCT gives:

```text
IT
HR
Finance
```

Duplicates are removed.

---

## Example

Employee Table

| employee_id | name   | department |
| ----------- | ------ | ---------- |
| 1           | Harsha | IT         |
| 2           | Ravi   | HR         |
| 3           | Priya  | IT         |
| 4           | Amit   | Finance    |
| 5           | Kiran  | HR         |

Query

```sql
SELECT DISTINCT department
FROM employees;
```

Output

| department |
| ---------- |
| IT         |
| HR         |
| Finance    |

---

## DISTINCT vs GROUP BY

Both queries produce the same result.

Using DISTINCT:

```sql
SELECT DISTINCT department
FROM employees;
```

Using GROUP BY:

```sql
SELECT department
FROM employees
GROUP BY department;
```

Both return:

```text
IT
HR
Finance
```

---

## Which One Should You Use?

If your goal is simply to retrieve unique values:

✅ Prefer **DISTINCT**.

If you need aggregations such as:

* COUNT()
* SUM()
* AVG()
* MIN()
* MAX()

Then use **GROUP BY**.

---

## Is DISTINCT Expensive?

Yes.

To remove duplicates, the database must compare rows and identify unique values.

On large datasets, this can involve sorting or hashing, making DISTINCT more expensive than a simple SELECT.

---

## DISTINCT Is Sometimes a Code Smell

Suppose you see:

```sql
SELECT DISTINCT c.customer_id,
                c.customer_name
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id;
```

Before approving this query, ask:

> **Why are duplicates being produced in the first place?**

Sometimes duplicates are expected because of a one-to-many relationship.

Other times, they indicate:

* Incorrect JOIN conditions
* Missing JOIN predicates
* Data quality issues

Using DISTINCT may hide the real problem instead of fixing it.

---

## Production Scenario

A developer submits a query using DISTINCT after a JOIN.

Instead of immediately approving it, first understand:

* Is the business requirement one row per customer?
* Are duplicate rows expected?
* Is DISTINCT solving the correct problem?

Always fix the root cause before using DISTINCT.

---

## Common Mistakes

### Mistake 1

Using DISTINCT to hide incorrect JOIN logic.

---

### Mistake 2

Using GROUP BY instead of DISTINCT when no aggregation is required.

---

### Mistake 3

Assuming DISTINCT is free.

It requires additional work to remove duplicates.

---

## Interview Explanation

A concise interview answer:

> "DISTINCT removes duplicate rows from the result set. If I only need unique values, I prefer DISTINCT because it clearly expresses my intent. However, if I see DISTINCT after a JOIN, I first investigate why duplicates are being generated instead of using DISTINCT to hide the issue."

---

## Key Takeaways

* DISTINCT returns unique values.
* Prefer DISTINCT when only uniqueness is required.
* Use GROUP BY when aggregations are needed.
* DISTINCT can be expensive on large datasets.
* Don't use DISTINCT to hide problems caused by incorrect joins.
