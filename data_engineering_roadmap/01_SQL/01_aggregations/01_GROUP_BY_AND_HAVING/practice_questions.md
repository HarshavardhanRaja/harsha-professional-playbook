# GROUP BY & HAVING - Practice Questions

> Goal: Test your understanding of GROUP BY, HAVING, execution order, grouped queries, and common interview traps.
>
> Rule: Try answering first before looking at the answer.

================================================================================

# 🟢 LEVEL 1 - FUNDAMENTALS

================================================================================

## Question 1

Business requirement:

> Show the number of employees in each department.

Which clause is required?

```text
GROUP BY

OR

HAVING
```

---

Answer:

✅ `GROUP BY`

The data must first be grouped by department before counting employees.

================================================================================

## Question 2

Suppose the table is:

| Employee | Department |
| -------- | ---------- |
| Harsha   | IT         |
| Ravi     | HR         |
| Priya    | IT         |
| Hari     | IT         |
| Amit     | Finance    |

Conceptually, what is the **first thing** SQL does after reaching `GROUP BY department`?

---

Answer:

SQL identifies the unique department values.

```text
IT

HR

Finance
```

These become the groups.

================================================================================

## Question 3

After identifying the groups, what does SQL do next?

---

Answer:

SQL partitions the rows into separate groups (conceptual buckets).

```text
IT
------------
Harsha
Priya
Hari

HR
------------
Ravi

Finance
------------
Amit
```

Aggregate functions are then applied independently to each group.

================================================================================

## Question 4

Complete the GROUP BY execution flow.

```text
One Big Table

↓

?

↓

?

↓

?

↓

One Row Per Group
```

---

Answer:

```text
One Big Table

↓

Identify Unique Groups

↓

Split Rows Into Buckets

↓

Run Aggregate Function
On Each Bucket

↓

One Row Per Group
```

================================================================================

# 🟡 LEVEL 2 - INTERVIEW TRAPS

================================================================================

## Question 5

Will this query work?

```sql
SELECT
    department,
    salary
FROM employees
GROUP BY department;
```

Why?

---

Answer:

❌ No.

`salary` is neither:

* grouped
* aggregated

After grouping, SQL has multiple salary values within a department and cannot determine which one to return.

================================================================================

## Question 6

Will this query work?

```sql
SELECT
    department,
    MAX(salary)
FROM employees
GROUP BY department;
```

Why?

---

Answer:

✅ Yes.

* `department` identifies the group.
* `MAX(salary)` reduces multiple salary values into a single value.

Every selected column now produces exactly one value per group.

================================================================================

## Question 7

Will this query work?

```sql
SELECT
    department,
    COUNT(*),
    name
FROM employees
GROUP BY department;
```

---

Answer:

❌ No.

`name` is neither grouped nor aggregated.

SQL cannot determine which employee name to return for each department.

================================================================================

## Question 8

Which rule is violated in Questions 5 and 7?

---

Answer:

The Golden Rule:

After `GROUP BY`, every selected column must be:

* In the GROUP BY
* OR aggregated

================================================================================

# 🔴 LEVEL 3 - WHERE vs HAVING

================================================================================

## Question 9

Business requirement:

> Show employees earning more than ₹100000.

Which clause should be used?

---

Answer:

✅ `WHERE`

This is a row-level filter.

================================================================================

## Question 10

Business requirement:

> Show departments whose average salary is greater than ₹100000.

Which clause should be used?

---

Answer:

✅ `HAVING`

The average salary exists only after grouping and aggregation.

================================================================================

## Question 11

Will this query work?

```sql
SELECT
    department,
    COUNT(*)
FROM employees
WHERE COUNT(*) > 2
GROUP BY department;
```

---

Answer:

❌ No.

`WHERE` executes before grouping.

`COUNT(*)` has not been calculated yet.

Use:

```sql
HAVING COUNT(*) > 2
```

================================================================================

## Question 12

Review this query.

```sql
SELECT
    department,
    AVG(salary)
FROM employees
WHERE salary > 50000
GROUP BY department
HAVING AVG(salary) > 100000;
```

Explain the execution order.

---

Answer:

Step 1

```text
FROM employees
```

Step 2

```text
WHERE salary > 50000
```

Filter individual rows.

Step 3

```text
GROUP BY department
```

Create department groups.

Step 4

```text
AVG(salary)
```

Calculate average salary for each group.

Step 5

```text
HAVING AVG(salary) > 100000
```

Filter groups.

Step 6

```text
SELECT
```

Return the final result.

================================================================================

# 🧠 MASTERY CHALLENGE

================================================================================

## Question 13

Review the following query like a Senior Data Engineer.

```sql
SELECT
    department,
    COUNT(*),
    AVG(salary),
    MAX(salary),
    employee_name
FROM employees
GROUP BY department;
```

Would you approve this query?

Explain your reasoning.

---

Expected Answer

❌ No.

Reason:

After `GROUP BY`, SQL returns one row per department.

Evaluate each selected column:

```text
department

↓

Grouped

↓

Valid

----------------------

COUNT(*)

↓

Aggregate

↓

Valid

----------------------

AVG(salary)

↓

Aggregate

↓

Valid

----------------------

MAX(salary)

↓

Aggregate

↓

Valid

----------------------

employee_name

↓

Not Grouped

↓

Not Aggregated

↓

Multiple Values Exist

↓

Invalid
```

The query violates the Golden Rule:

> Every selected column must either be grouped or aggregated.

================================================================================

# ✅ Completion Criteria

If you can answer all 13 questions confidently and explain **why** each query is valid or invalid, you have mastered:

* GROUP BY
* HAVING
* GROUP BY execution
* WHERE vs HAVING
* One Row Per Group rule
* Golden Rule of GROUP BY
* Group-level vs Row-level filtering
* Common SQL interview traps
