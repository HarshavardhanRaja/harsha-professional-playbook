# where()

## Goal

Filter rows using SQL-style syntax.

Example:

```python
df.where(df.role == "Data Engineer").show()
```

Output:

```txt
+---+------+-------------+------+
| id| name |    role     |salary|
+---+------+-------------+------+
| 1 |Harsha|Data Engineer|230000|
+---+------+-------------+------+
```

Equivalent SQL:

```sql
SELECT *
FROM employees
WHERE role='Data Engineer';
```

Important:

`where()` and `filter()` are aliases.

These produce identical execution plans.

Use whichever improves readability.

Interview Question:

Q:
Difference between filter() and where()?

Answer:

No functional difference.
`where()` is an alias for `filter()`.

Real-world Usage:

Filtering customers

Filtering transactions

Filtering logs

Filtering events