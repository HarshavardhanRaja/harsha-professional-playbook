# drop()

## Goal

Remove columns.

Example:

```python
explicit_df.drop("salary").show()
```

Output:

```txt
+---+------+
| id| name |
+---+------+
|1  |Harsha|
|2  |Ravi  |
+---+------+
```

---

Equivalent SQL:

```sql
SELECT id, name
FROM employees
```

---

Real-world Usage

Remove:

PII columns

Temporary columns

Unused fields

Raw payloads

---

Important

Spark DataFrames are immutable.

drop()

creates new DataFrame

Original remains unchanged.

---

Interview Question

Q:
Does drop() modify original DataFrame?

Answer:

No.

drop() returns a new DataFrame without specified columns.

---

## drop() and Immutability

Check original:

```python
explicit_df.printSchema()

root
 |-- salary: integer


---

# New Topic: `distinct()` (very common)

Real-world:

```txt
duplicate users
duplicate orders
duplicate events
duplicate transactions

Observation:

Original DataFrame unchanged.

drop()

creates new DataFrame

Interview Question:

Q:
Why are immutable DataFrames useful?

Answer:

Immutability avoids accidental modifications, improves fault tolerance, and enables Spark optimizations.

