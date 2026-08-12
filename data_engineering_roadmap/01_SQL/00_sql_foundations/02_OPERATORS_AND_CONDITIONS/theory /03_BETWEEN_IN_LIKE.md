# BETWEEN, IN and LIKE

## BETWEEN

The `BETWEEN` operator filters values that fall within a specified range.

Example:

```sql
SELECT *
FROM employees
WHERE salary BETWEEN 50000 AND 100000;
```

This query is equivalent to:

```sql
WHERE salary >= 50000
AND salary <= 100000;
```

### Important

`BETWEEN` is **inclusive**.

Both boundary values are included.

Example:

| Salary | Returned? |
| ------ | --------- |
| 49999  | ❌ No      |
| 50000  | ✅ Yes     |
| 75000  | ✅ Yes     |
| 100000 | ✅ Yes     |
| 100001 | ❌ No      |

---

## BETWEEN with TIMESTAMP

Although `BETWEEN` works well for numeric values and DATE columns, extra care is required when filtering TIMESTAMP columns.

Example:

```sql
WHERE order_timestamp BETWEEN
'2025-01-01'
AND
'2025-12-31'
```

This may unintentionally exclude records occurring later on `2025-12-31` because the upper bound is typically interpreted as:

```text
2025-12-31 00:00:00
```

Instead, prefer:

```sql
WHERE order_timestamp >= '2025-01-01'
AND order_timestamp < '2026-01-01'
```

This pattern includes every timestamp within the year.

---

## IN

The `IN` operator checks whether a value exists in a list of values.

Example:

```sql
SELECT *
FROM employees
WHERE department IN ('IT', 'Finance');
```

This query is equivalent to:

```sql
WHERE department = 'IT'
OR department = 'Finance'
```

---

## Why Use IN?

`IN` improves readability when checking multiple values for the same column.

Instead of:

```sql
WHERE department = 'IT'
OR department = 'HR'
OR department = 'Finance'
OR department = 'Sales'
```

Prefer:

```sql
WHERE department IN (
    'IT',
    'HR',
    'Finance',
    'Sales'
)
```

This is easier to read, maintain and extend.

---

## NOT IN

`NOT IN` returns rows whose values are not present in the specified list.

Example:

```sql
SELECT *
FROM employees
WHERE department NOT IN ('IT', 'HR');
```

---

## Production Trap

Be careful when the list contains `NULL`.

Example:

```sql
WHERE department NOT IN ('IT', 'HR', NULL)
```

Because comparisons with `NULL` evaluate to **UNKNOWN**, this query can produce unexpected results and may return no rows.

This topic is covered in detail under **NULL Handling**.

---

## LIKE

The `LIKE` operator performs pattern matching on text.

Example:

```sql
SELECT *
FROM employees
WHERE name LIKE 'Har%';
```

---

## Wildcards

### %

Represents **zero or more characters**.

Examples:

```sql
LIKE 'Har%'
```

Starts with `Har`.

---

```sql
LIKE '%sha'
```

Ends with `sha`.

---

```sql
LIKE '%ar%'
```

Contains `ar`.

---

### _

Represents **exactly one character**.

Example:

```sql
LIKE 'H_rsha'
```

Matches:

```text
Harsha
```

because `_` replaces exactly one character.

---

## LIKE and Performance

Prefix searches can often use an index efficiently.

Example:

```sql
WHERE name LIKE 'Har%'
```

The database knows every matching value starts with `Har`, allowing it to efficiently locate the relevant portion of the index.

However,

```sql
WHERE name LIKE '%Har%'
```

is typically less efficient because the match can occur anywhere in the string, making it difficult to use the index effectively.

---

## Production Best Practices

### Use BETWEEN Carefully

* Safe for numeric ranges.
* Safe for DATE columns.
* Prefer half-open ranges (`>= start AND < next`) for TIMESTAMP columns.

---

### Prefer IN

Use `IN` when checking multiple values for the same column.

It improves readability and maintainability.

---

### Avoid NOT IN with NULL

If the list or subquery can contain `NULL`, verify the logic carefully.

---

### Use Prefix Searches When Possible

```sql
LIKE 'Har%'
```

is generally more efficient than:

```sql
LIKE '%Har%'
```

---

## Common Mistakes

### Mistake 1

Assuming `BETWEEN` is exclusive.

It is inclusive.

---

### Mistake 2

Using `BETWEEN` for TIMESTAMP ranges without considering the time component.

---

### Mistake 3

Writing long chains of `OR` instead of using `IN`.

---

### Mistake 4

Ignoring the effect of `NULL` when using `NOT IN`.

---

### Mistake 5

Assuming all `LIKE` queries perform equally.

Leading wildcards often prevent efficient index usage.

---

## Interview Explanation

A concise interview answer:

> "`BETWEEN` is inclusive and works well for numeric values and DATE columns. For TIMESTAMP columns, I prefer half-open ranges (`>= start AND < next`) to avoid missing records on the upper boundary. I use `IN` instead of long `OR` chains for readability and maintainability. For text searches, prefix searches such as `LIKE 'Har%'` are generally more index-friendly than searches with leading wildcards."

---

## Key Takeaways

* `BETWEEN` includes both boundary values.
* Avoid `BETWEEN` for TIMESTAMP ranges.
* Use `IN` for multiple values of the same column.
* Be careful with `NOT IN` when `NULL` is involved.
* `%` matches zero or more characters.
* `_` matches exactly one character.
* `LIKE 'text%'` is generally more efficient than `LIKE '%text%'`.
