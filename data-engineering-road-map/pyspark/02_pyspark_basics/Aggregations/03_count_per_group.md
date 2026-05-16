# Count per Group

## Goal

Count rows within categories.

Example:

```python
dept_df.groupBy(
    "department"
).count().show()
```

Output:

```txt
Engineering → 2
Analytics → 1
```

Equivalent SQL:

```sql
SELECT department,
COUNT(*)
FROM employees
GROUP BY department
```

---

Real-world Usage

Count:

orders

users

 applications

transactions

events

per category

---

Fun Analogy

groupBy()

creates buckets

count()

counts people inside each bucket

---

Interview Question

Q:
What does groupBy().count() do?

Answer:

Groups records by keys and counts rows within each group.