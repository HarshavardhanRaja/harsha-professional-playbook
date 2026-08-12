# Operators and Conditions - Practice Questions

> Goal: Test your understanding of comparison operators, logical operators, BETWEEN, IN, LIKE and production SQL practices.
>
> Rule: Try answering first before looking at the answer.

================================================================================

# 🟢 LEVEL 1 - FUNDAMENTALS

================================================================================

## Question 1

```sql
SELECT *
FROM employees
WHERE department <> 'HR';
```

What rows will this query return?

Is `<>` different from `!=`?

---

Answer:

The query returns every employee except those in the HR department.

`<>` and `!=` both represent **Not Equal To** in most modern databases.

`<>` is the ANSI SQL standard.

================================================================================

## Question 2

```sql
SELECT *
FROM employees
WHERE department = 'IT'
AND salary > 100000;
```

How does SQL evaluate this condition?

---

Answer:

For each row:

1. Check if `department = 'IT'`.
2. Check if `salary > 100000`.
3. Apply the `AND` operator.
4. Keep the row only if both conditions are TRUE.

Each row is evaluated independently.

================================================================================

## Question 3

```sql
SELECT *
FROM employees
WHERE NOT salary > 100000;
```

Would you approve this query?

---

Answer:

⚠ It is logically correct.

However, I would rewrite it as:

```sql
WHERE salary <= 100000;
```

The second version is easier to read and better communicates the business intent.

================================================================================

## Question 4

```sql
SELECT *
FROM employees
WHERE salary BETWEEN 50000 AND 100000;
```

Will employees with salaries exactly equal to **50000** or **100000** be returned?

---

Answer:

✅ Yes.

`BETWEEN` is inclusive.

Equivalent query:

```sql
WHERE salary >= 50000
AND salary <= 100000;
```

================================================================================

# 🟡 LEVEL 2 - INTERVIEW TRAPS

================================================================================

## Question 5

Review this query.

```sql
SELECT *
FROM orders
WHERE order_timestamp BETWEEN
'2025-01-01'
AND
'2025-12-31';
```

Would you approve it?

---

Answer:

❌ No.

If `order_timestamp` is a TIMESTAMP column, records later on `2025-12-31` may be excluded.

Prefer:

```sql
WHERE order_timestamp >= '2025-01-01'
AND order_timestamp < '2026-01-01'
```

================================================================================

## Question 6

Will these two queries return the same result?

```sql
WHERE department IN ('IT', 'Finance')
```

```sql
WHERE department = 'IT'
OR department = 'Finance'
```

Which would you choose?

---

Answer:

✅ Both return the same result.

I prefer `IN` because it is easier to read, maintain and extend when the list grows.

================================================================================

## Question 7

Review this query.

```sql
SELECT *
FROM employees
WHERE department NOT IN ('IT', 'HR', NULL);
```

Would you approve it?

---

Answer:

❌ No.

If the list contains `NULL`, `NOT IN` can produce unexpected results and may return no rows.

I would first verify that the list cannot contain `NULL`, or consider using `NOT EXISTS` if appropriate.

================================================================================

## Question 8

Which query is likely to perform better?

Query A

```sql
WHERE name LIKE 'Har%'
```

Query B

```sql
WHERE name LIKE '%Har%'
```

Explain your answer.

---

Answer:

Query A.

The database can often use an index efficiently because every matching value starts with `"Har"`.

Query B usually cannot efficiently use the index because the wildcard appears at the beginning.

================================================================================

# 🔴 LEVEL 3 - PRODUCTION THINKING

================================================================================

## Question 9

Review this query.

```sql
SELECT *
FROM employees
WHERE employee_id + 1 = 101;
```

Would you approve it?

---

Answer:

❌ No.

The database must calculate `employee_id + 1` for every row before evaluating the condition.

Rewrite it as:

```sql
WHERE employee_id = 100;
```

This is SARGable and allows efficient index usage.

================================================================================

## Question 10

Review this query.

```sql
SELECT *
FROM employees
WHERE salary * 2 > 200000;
```

How would you improve it?

---

Answer:

Rewrite it as:

```sql
WHERE salary > 100000;
```

This avoids calculations on the filtered column and improves the chances of efficient index usage.

================================================================================

## Question 11

Review this query.

```sql
SELECT *
FROM employees
WHERE department='IT'
AND salary>100000
OR department='Finance';
```

Would you approve this PR?

---

Answer:

⚠ Although SQL evaluates it correctly because `AND` has higher precedence than `OR`, I would request a small change.

Rewrite it as:

```sql
WHERE (
        department='IT'
        AND salary>100000
      )
OR department='Finance'
```

This makes the business logic much easier to understand.

================================================================================

# 🧠 MASTERY CHALLENGE

================================================================================

## Question 12

Review the following query like a Senior Data Engineer.

```sql
SELECT *
FROM employees
WHERE department IN ('IT', 'Finance')
AND joining_date BETWEEN '2025-01-01' AND '2025-12-31'
AND name LIKE '%Har%';
```

Identify every potential concern and explain whether you would approve the query.

---

Expected Answer

Observations:

1. `IN` is a good choice for checking multiple department values.
2. If `joining_date` is a DATE column, `BETWEEN` is acceptable.
3. If `joining_date` is a TIMESTAMP column, prefer:

```sql
joining_date >= '2025-01-01'
AND joining_date < '2026-01-01'
```

4. `LIKE '%Har%'` may not efficiently use an index on large tables.

Overall, I would approve only after confirming the data types and performance requirements.

================================================================================

# ✅ Completion Criteria

If you can confidently answer all 12 questions without looking at the answers, you have mastered:

* Comparison Operators
* Logical Operators
* Operator Precedence
* BETWEEN
* IN
* NOT IN
* LIKE
* SARGable vs Non-SARGable Conditions
* Production SQL Filtering Best Practices
