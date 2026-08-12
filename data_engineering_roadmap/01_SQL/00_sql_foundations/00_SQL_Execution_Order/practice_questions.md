# SQL Execution Order - Practice Questions

> Goal: Test your understanding of SQL execution order, aliases, aggregates, WHERE vs HAVING, and query processing.
>
> Rule: Try answering first before looking at the answer.

================================================================================

# 🟢 LEVEL 1 - FUNDAMENTALS

================================================================================

## Question 1

```sql
SELECT salary AS sal
FROM employees
WHERE sal > 100000;
```

Will this work?

Why?

---

Answer:

❌ No.

WHERE executes before SELECT.

The alias `sal` is created during SELECT, therefore it does not exist when WHERE executes.

================================================================================

## Question 2

```sql
SELECT salary AS sal
FROM employees
ORDER BY sal DESC;
```

Will this work?

Why?

---

Answer:

✅ Yes.

ORDER BY executes after SELECT.

The alias `sal` already exists.

================================================================================

## Question 3

```sql
SELECT department,
       COUNT(*) cnt
FROM employees
GROUP BY department
ORDER BY cnt DESC;
```

Will this work?

Why?

---

Answer:

✅ Yes.

ORDER BY executes after SELECT.

Alias `cnt` already exists.

================================================================================

## Question 4

```sql
SELECT department,
       COUNT(*) cnt
FROM employees
WHERE COUNT(*) > 5
GROUP BY department;
```

Will this work?

Why?

---

Answer:

❌ No.

WHERE executes before GROUP BY.

COUNT(*) is an aggregate and does not exist yet.

================================================================================

## Question 5

```sql
SELECT department,
       COUNT(*) cnt
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;
```

Will this work?

Why?

---

Answer:

✅ Yes.

HAVING executes after GROUP BY.

Aggregate values already exist.

================================================================================

# 🟡 LEVEL 2 - INTERVIEW TRAPS

================================================================================

## Question 6

```sql
SELECT department,
       COUNT(*) cnt
FROM employees
GROUP BY department
WHERE cnt > 5;
```

Will this work?

What are the problems?

---

Answer:

❌ No.

Problem 1:

WHERE executes before SELECT.

Alias `cnt` does not exist.

Problem 2:

Even replacing `cnt` with COUNT(*) would fail because aggregates are not available during WHERE execution.

================================================================================

## Question 7

```sql
SELECT department,
       AVG(salary) avg_sal
FROM employees
GROUP BY department
HAVING avg_sal > 50000;
```

Will this work?

---

Answer:

⚠ Depends on the database.

Some databases allow aliases in HAVING.

Others do not.

Safest version:

```sql
HAVING AVG(salary) > 50000
```

================================================================================

## Question 8

Put the following clauses in execution order:

```text
ORDER BY
GROUP BY
WHERE
HAVING
SELECT
FROM
```

---

Answer:

```text
FROM
WHERE
GROUP BY
HAVING
SELECT
ORDER BY
```

================================================================================

## Question 9

Which is correct?

```sql
SELECT *
FROM employees
WHERE salary > 100000;
```

OR

```sql
SELECT *
FROM employees
HAVING salary > 100000;
```

---

Answer:

✅ WHERE is the correct solution.

HAVING is intended for grouped results.

Some databases may allow the second query, but WHERE should be used for row-level filtering.

================================================================================

# 🔴 LEVEL 3 - ADVANCED

================================================================================

## Question 10

Why is this invalid?

```sql
SELECT *
FROM employees
WHERE ROW_NUMBER() OVER(
          PARTITION BY department
          ORDER BY salary DESC
      ) = 1;
```

---

Answer:

Window functions are calculated after WHERE.

ROW_NUMBER() does not exist when WHERE executes.

Use:

* CTE
* Subquery
* QUALIFY (if supported)

================================================================================

## Question 11

Why does this work?

```sql
SELECT
    department,
    COUNT(*) cnt
FROM employees
GROUP BY department
ORDER BY 2 DESC;
```

---

Answer:

`2` refers to the second column in the SELECT output.

Column positions are known when ORDER BY executes.

Equivalent to:

```sql
ORDER BY cnt DESC
```

================================================================================

## Question 12

Are all three queries valid?

```sql
ORDER BY cnt
```

```sql
ORDER BY COUNT(*)
```

```sql
ORDER BY 2
```

---

Answer:

✅ Yes.

All three sort using the aggregate count.

However:

```sql
ORDER BY cnt
```

is preferred because it is the most readable.

================================================================================

# 🧠 MASTERY CHALLENGE

================================================================================

## Question 13

Explain the execution of this query step-by-step:

```sql
SELECT
    department,
    AVG(salary) avg_sal
FROM employees
WHERE salary > 50000
GROUP BY department
HAVING AVG(salary) > 100000
ORDER BY avg_sal DESC
LIMIT 3;
```

---

Expected Answer:

Step 1:
FROM employees

Step 2:
WHERE salary > 50000

Step 3:
GROUP BY department

Step 4:
Calculate AVG(salary) for each group

Step 5:
HAVING AVG(salary) > 100000

Step 6:
SELECT department, avg_sal

Step 7:
ORDER BY avg_sal DESC

Step 8:
LIMIT 3

================================================================================

# ✅ Completion Criteria

If you can answer Questions 1–12 correctly and explain Question 13 without looking at the answer, you have mastered SQL Execution Order.
