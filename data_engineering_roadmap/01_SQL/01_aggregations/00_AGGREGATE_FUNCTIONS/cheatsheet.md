# Aggregate Functions - Cheatsheet

---

# Aggregate Functions

Aggregate functions summarize **multiple rows** into a **single value**.

| Function               | Purpose                      |
| ---------------------- | ---------------------------- |
| COUNT(*)               | Count all rows               |
| COUNT(column)          | Count non-NULL values        |
| COUNT(DISTINCT column) | Count unique non-NULL values |
| SUM()                  | Add values                   |
| AVG()                  | Calculate average            |
| MIN()                  | Smallest value               |
| MAX()                  | Largest value                |

---

# COUNT(*)

Counts every row.

```sql
SELECT COUNT(*)
FROM employees;
```

Includes rows containing NULL values.

---

# COUNT(column)

Counts only non-NULL values.

```sql
SELECT COUNT(bonus)
FROM employees;
```

NULL values are ignored.

---

# COUNT(DISTINCT column)

Counts unique non-NULL values.

```sql
SELECT COUNT(DISTINCT department)
FROM employees;
```

Conceptually:

```text
DISTINCT

↓

Remove Duplicates

↓

COUNT(column)

↓

Ignore NULL

↓

Final Count
```

---

# SUM()

Adds all non-NULL values.

```sql
SELECT SUM(salary)
FROM employees;
```

Ignores NULL values.

---

# AVG()

Calculates the average of non-NULL values.

Conceptually:

```text
SUM(column)

↓

COUNT(column)

↓

SUM / COUNT
```

```sql
SELECT AVG(salary)
FROM employees;
```

Ignores NULL values.

---

# MIN()

Returns the smallest non-NULL value.

```sql
SELECT MIN(salary)
FROM employees;
```

Does **not** sort the data.

Maintains the current minimum while scanning rows.

---

# MAX()

Returns the largest non-NULL value.

```sql
SELECT MAX(salary)
FROM employees;
```

Does **not** sort the data.

Maintains the current maximum while scanning rows.

---

# NULL Handling

| Function        | NULL Handling   |
| --------------- | --------------- |
| COUNT(*)        | Counts all rows |
| COUNT(column)   | Ignores NULL    |
| COUNT(DISTINCT) | Ignores NULL    |
| SUM             | Ignores NULL    |
| AVG             | Ignores NULL    |
| MIN             | Ignores NULL    |
| MAX             | Ignores NULL    |

---

# Conceptual Execution

```text
COUNT(*)

↓

Running Counter

----------------------

SUM

↓

Running Total

----------------------

AVG

↓

Running Sum

+

Running Count

↓

SUM / COUNT

----------------------

MIN

↓

Running Minimum

----------------------

MAX

↓

Running Maximum

----------------------

COUNT(DISTINCT)

↓

Track Unique Values

↓

Count
```

---

# Performance

### Fast

```sql
COUNT(*)
```

Simple row count.

---

### Slower

```sql
COUNT(DISTINCT column)
```

Requires:

* Detect duplicates
* Hashing or sorting
* Extra memory

---

# Production Best Practices

✅ Use `COUNT(*)` to count rows.

✅ Use `COUNT(column)` when NULL values should be excluded.

✅ Use `AVG()` instead of manually writing:

```sql
SUM(column) / COUNT(column)
```

✅ Use `COUNT(DISTINCT)` only when uniqueness is required.

✅ Remember all aggregates except `COUNT(*)` ignore NULL values.

---

# Common Mistakes

❌ Assuming `COUNT(*)` = `COUNT(column)`

❌ Assuming `AVG()` divides by all rows

❌ Thinking `MIN()` and `MAX()` sort the data

❌ Using `COUNT(DISTINCT)` when `COUNT()` is sufficient

---

# Quick Revision

```text
COUNT(*)

↓

Rows

----------------------

COUNT(column)

↓

Non-NULL Rows

----------------------

COUNT(DISTINCT)

↓

Unique Non-NULL Values

----------------------

SUM

↓

Running Total

----------------------

AVG

↓

SUM / COUNT(column)

----------------------

MIN

↓

Running Minimum

----------------------

MAX

↓

Running Maximum

----------------------

COUNT(DISTINCT)

↓

Most Expensive Aggregate
```
