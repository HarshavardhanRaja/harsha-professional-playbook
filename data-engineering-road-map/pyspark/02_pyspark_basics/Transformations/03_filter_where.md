# filter() / where()

## Goal

Filter rows based on a condition.

## Example

```python
df.filter(df.salary > 100000).show()
```

## Output

```txt
+---+------+-------------+------+
| id|  name|         role|salary|
+---+------+-------------+------+
|  1|Harsha|Data Engineer|230000|
|  3|   Anu|  ML Engineer|180000|
+---+------+-------------+------+
```

## SQL Equivalent

```sql
SELECT *
FROM employees
WHERE salary > 100000;
```

## Fun Analogy

`filter()` is like a security guard at an event.

Only people matching the rule are allowed inside.

Rule:

```txt
salary > 100000
```

Allowed:

```txt
Harsha
Anu
```

Blocked:

```txt
Ravi
```

## Interview Question

Q: What is the difference between `filter()` and `where()` in PySpark?

Answer:

There is no functional difference. `where()` is an alias for `filter()`. Both are used to filter rows based on conditions.

## Key Takeaway

Use `filter()` or `where()` when you want to reduce rows.