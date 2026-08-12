# Logical Operators

## What Are Logical Operators?

Logical operators combine one or more conditions into a single condition.

They determine whether a row satisfies multiple conditions before it is returned.

SQL supports three logical operators:

| Operator | Purpose                             |
| -------- | ----------------------------------- |
| AND      | All conditions must be TRUE         |
| OR       | At least one condition must be TRUE |
| NOT      | Reverses the result of a condition  |

---

## AND

The `AND` operator returns a row only when **all conditions evaluate to TRUE**.

Example:

```sql
SELECT *
FROM employees
WHERE department = 'IT'
AND salary > 100000;
```

Execution for each row:

1. Check if `department = 'IT'`.
2. Check if `salary > 100000`.
3. Return the row only if both conditions are TRUE.

---

## OR

The `OR` operator returns a row when **at least one condition evaluates to TRUE**.

Example:

```sql
SELECT *
FROM employees
WHERE department = 'IT'
OR department = 'Finance';
```

This query returns employees belonging to either IT or Finance.

---

## NOT

The `NOT` operator reverses the result of a condition.

Example:

```sql
SELECT *
FROM employees
WHERE NOT department = 'HR';
```

This is equivalent to:

```sql
SELECT *
FROM employees
WHERE department <> 'HR';
```

Another example:

```sql
WHERE NOT salary > 100000
```

is equivalent to:

```sql
WHERE salary <= 100000
```

Although both queries produce the same result, the second version is usually easier to read.

---

## Operator Precedence

When multiple logical operators are used together, SQL follows a predefined evaluation order.

```text
Highest

NOT

↓

AND

↓

OR

Lowest
```

Example:

```sql
WHERE department = 'IT'
AND salary > 100000
OR department = 'Finance'
```

SQL evaluates it as:

```sql
WHERE (department = 'IT'
       AND salary > 100000)
OR department = 'Finance'
```

because `AND` has higher precedence than `OR`.

---

## Why Parentheses Matter

Although SQL correctly applies operator precedence, relying on it can make queries harder to understand.

Instead of:

```sql
WHERE department = 'IT'
AND salary > 100000
OR department = 'Finance'
```

Prefer:

```sql
WHERE (
        department = 'IT'
        AND salary > 100000
      )
OR department = 'Finance'
```

The result is the same, but the intent is much clearer for anyone reading the query.

---

## Row-by-Row Evaluation

The `WHERE` clause evaluates conditions independently for every row.

Example:

```sql
SELECT *
FROM employees
WHERE department = 'IT'
AND salary > 100000;
```

For each row:

1. Evaluate `department = 'IT'`.
2. Evaluate `salary > 100000`.
3. Apply the `AND` operator.
4. Keep the row only if the final result is TRUE.

Rows are never compared with one another.

---

## Production Best Practices

### Use Parentheses

Whenever a query mixes `AND` and `OR`, explicitly use parentheses.

This improves readability and avoids misunderstanding.

---

### Prefer Positive Conditions

Instead of:

```sql
WHERE NOT salary > 100000
```

Prefer:

```sql
WHERE salary <= 100000
```

The second version is easier to understand and maintain.

---

### Write SQL for Humans

SQL is read much more often than it is written.

Always choose the version that clearly expresses the business requirement.

---

## Common Mistakes

### Mistake 1

Assuming SQL evaluates conditions from left to right.

SQL follows operator precedence.

---

### Mistake 2

Mixing `AND` and `OR` without parentheses.

Even if SQL evaluates the query correctly, the intent may not be obvious to future readers.

---

### Mistake 3

Using `NOT` when a simpler comparison operator communicates the intent more clearly.

---

## Interview Explanation

A concise interview answer:

> "Logical operators combine multiple conditions in the WHERE clause. SQL evaluates them using operator precedence: NOT first, then AND, then OR. Whenever I mix AND and OR in production queries, I explicitly use parentheses to improve readability and reduce the risk of logical errors."

---

## Key Takeaways

* `AND` requires all conditions to be TRUE.
* `OR` requires at least one condition to be TRUE.
* `NOT` reverses a condition.
* SQL evaluates `NOT → AND → OR`.
* Use parentheses when mixing `AND` and `OR`.
* Write queries that are easy for other engineers to understand.
