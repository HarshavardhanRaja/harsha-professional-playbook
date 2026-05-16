# withColumn()

## Goal

Create or modify columns.

Think:

withColumn() = Add new calculated field

---

Example:

```python
df.withColumn(
    "salary_in_lakhs",
    df.salary / 100000
).show()
```

Output:

```txt
+---+------+-------------+------+---------------+
| id|  name|         role|salary|salary_in_lakhs|
+---+------+-------------+------+---------------+
|  1|Harsha|Data Engineer|230000|            2.3|
|  2|  Ravi| Data Analyst| 90000|            0.9|
|  3|   Anu|  ML Engineer|180000|            1.8|
+---+------+-------------+------+---------------+
```

---

Equivalent SQL:

```sql
SELECT *,
       salary/100000 AS salary_in_lakhs
FROM employees
```

---

Real-world Examples

Convert:

```txt
milliseconds → timestamp
```

Create:

```txt
discounted_price
tax
flags
partitions
status columns
```

---

Fun Analogy

withColumn()

≈ Adding a new formula column in Excel

Existing:

salary

New:

salary_in_lakhs

---

Interview Question

Q:
Difference between select() and withColumn()?

Answer:

select()

→ chooses columns

withColumn()

→ creates or modifies columns

---

Key Takeaway

withColumn() is one of the most common transformations in ETL pipelines.


---

## Overwriting Existing Columns

Example:

```python
df.withColumn(
    "salary",
    df.salary + 10000
).show()
```

Output:

```txt
salary:

230000 → 240000
90000 → 100000
```

Observation:

Existing column replaced.

Important Rule:

```txt
Existing column name
        ↓
Overwrite

New column name
        ↓
Create column
```

Interview Question:

Q:
Can withColumn() modify existing columns?

Answer:

Yes.

If column exists, Spark replaces it.

If column does not exist, Spark creates it.