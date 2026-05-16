# orderBy()

## Goal

Sort rows.

Example:

```python
explicit_df.orderBy("salary").show()
```

Output:

```txt
90000
230000
```

Observation:

Default sorting = ascending

---

Equivalent SQL:

```sql
SELECT *
FROM employees
ORDER BY salary ASC
```

---

Real-world Usage

Sort:

top customers

highest salaries

latest events

transactions

---

Fun Analogy

orderBy()

≈ Ranking students by marks

Lowest → Highest

---

Interview Question

Q:
What is default sorting order in orderBy()?

Answer:

Ascending.

---

## Descending Sort

Example:

```python
explicit_df.orderBy(
    explicit_df.salary.desc()
).show()
```

Output:

Highest salary appears first.

Equivalent SQL:

```sql
ORDER BY salary DESC
```

---

Interview Question

Q:
How do you sort descending in Spark?

Answer:

Use:

```python
col.desc()
```

inside orderBy().