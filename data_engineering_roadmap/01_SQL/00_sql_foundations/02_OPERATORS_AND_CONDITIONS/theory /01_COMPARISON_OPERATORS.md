# Comparison Operators

## What Are Comparison Operators?

Comparison operators compare two values and return either **TRUE**, **FALSE**, or **UNKNOWN** (when `NULL` is involved).

They are primarily used in the `WHERE` clause to filter rows.

Example:

```sql
SELECT *
FROM employees
WHERE salary >= 100000;
```

Only rows where the condition evaluates to **TRUE** are returned.

---

## Comparison Operators

| Operator | Meaning                          |
| -------- | -------------------------------- |
| =        | Equal to                         |
| !=       | Not equal to                     |
| <>       | Not equal to (ANSI SQL Standard) |
| >        | Greater than                     |
| >=       | Greater than or equal to         |
| <        | Less than                        |
| <=       | Less than or equal to            |

---

## How SQL Evaluates Comparison Operators

SQL evaluates comparison conditions **one row at a time**.

Example:

```sql
SELECT *
FROM employees
WHERE salary >= 100000;
```

Execution:

1. Read the `employees` table.
2. For each row, evaluate `salary >= 100000`.
3. Keep rows where the condition is **TRUE**.
4. Discard rows where the condition is **FALSE**.
5. Return the remaining rows.

Comparison operators never compare one row with another. Each row is evaluated independently.

---

## != vs <>

Both operators mean **Not Equal To**.

Example:

```sql
WHERE department != 'HR'
```

```sql
WHERE department <> 'HR'
```

Both queries produce the same result in most modern databases.

`<>` is the ANSI SQL standard, while `!=` is widely supported by popular databases.

---

## Data Type Considerations

Comparison operators work best when both values are of compatible data types.

Example:

```sql
WHERE salary = 100000
```

If `salary` is a `DECIMAL` column, the database typically performs an implicit conversion of the numeric literal.

There is usually no need to explicitly cast the value.

---

## Avoid Unnecessary Casting

Instead of:

```sql
WHERE CAST(salary AS INT) = 100000
```

Prefer:

```sql
WHERE salary = 100000
```

Applying functions or casts directly on filtered columns may prevent efficient index usage.

---

## Production Best Practices

### Keep the column unchanged

Prefer:

```sql
WHERE employee_id = 100
```

Instead of:

```sql
WHERE employee_id + 1 = 101
```

The second query requires the database to calculate the expression for each row before evaluating the condition.

---

### Compare compatible data types

Avoid unnecessary conversions whenever possible.

Let the database compare compatible values directly.

---

## Common Mistakes

### Mistake 1

Applying calculations on filtered columns.

```sql
WHERE salary * 2 > 200000
```

Prefer:

```sql
WHERE salary > 100000
```

---

### Mistake 2

Applying unnecessary casts.

```sql
WHERE CAST(employee_id AS VARCHAR) = '100'
```

Instead, compare compatible data types directly.

---

### Mistake 3

Assuming `!=` and `<>` behave differently.

In most databases they are equivalent.

---

## Interview Explanation

A concise interview answer:

> "Comparison operators evaluate conditions independently for each row and return rows where the condition is TRUE. I prefer keeping the filtered column unchanged because applying calculations or unnecessary casts may prevent efficient index usage. Both `!=` and `<>` represent 'not equal', although `<>` is the ANSI SQL standard."

---

## Key Takeaways

* Comparison operators evaluate one row at a time.
* Rows are returned only when the condition evaluates to TRUE.
* `!=` and `<>` are generally equivalent.
* Avoid calculations and unnecessary casts on filtered columns.
* Compare compatible data types directly whenever possible.
