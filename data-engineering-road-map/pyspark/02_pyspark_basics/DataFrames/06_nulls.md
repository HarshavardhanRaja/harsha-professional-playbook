# Null Handling

Input:

```python
null_data = [
 ("Harsha",230000),
 ("Ravi",None),
 ("Anu",180000)
]
```

Output:

```txt
Ravi → NULL
```

Observation:

Python:

```txt
None
```

becomes:

```txt
NULL
```

in Spark.

---

Real-world NULLs:

Missing salaries

Missing emails

Missing timestamps

Incomplete records

---

Interview Question

Q:
How does Spark represent missing values?

Answer:

Missing values appear as NULL.

---

## dropna()

Remove rows containing NULL values.

Example:

```python
null_df.dropna().show()
```

Output:

```txt
Harsha

Anu
```

Ravi removed.

Reason:

salary = NULL

---

Equivalent SQL:

```sql
WHERE salary IS NOT NULL
```

---

Interview Question

Q:
What does dropna() do?

Answer:

Removes rows containing NULL values.


---

## fillna()

Replace NULL values.

Example:

```python
null_df.fillna(
 {"salary":0}
).show()
```

Output:

```txt
Ravi → 0
```

Observation:

NULL replaced.

---

Equivalent SQL:

```sql
COALESCE(salary,0)
```

---

Real-world Usage

Missing salary → 0

Missing city → unknown

Missing count → 0

---

Interview Question

Q:
Difference between dropna() and fillna()?

Answer:

dropna()

removes rows

fillna()

replaces NULL values