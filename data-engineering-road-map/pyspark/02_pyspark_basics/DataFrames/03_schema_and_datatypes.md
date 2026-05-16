# Schema and Data Types

Check schema:

```python
df.printSchema()
```

Output:

```txt
root
 |-- id: long
 |-- name: string
 |-- role: string
 |-- salary: long
```

---

Schema tells:

Column names

Data types

Nullability

Think:

Schema ≈ Table definition in SQL

---

Example:

SQL:

```sql
CREATE TABLE employees(
id BIGINT,
name STRING,
salary BIGINT
)
```

Equivalent Spark:

Schema output

---

nullable=true

Meaning:

NULL values allowed

Example:

```txt
name

Harsha
NULL
Ravi
```

---

Why important?

Wrong schema causes:

Failed joins

Aggregation issues

Parsing failures

Pipeline failures

---

Interview Question

Q:
Why check schema in Spark?

Answer:

Schema validation ensures columns have expected types and prevents runtime errors.

---

Key Takeaway

Always inspect schema before transformations.