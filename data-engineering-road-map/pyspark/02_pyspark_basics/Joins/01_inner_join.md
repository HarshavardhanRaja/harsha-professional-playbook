# Inner Join

## Goal

Combine datasets using common keys.

Example:

```python
emp_df.join(
 salary_df,
 on="id",
 how="inner"
).show()
```

Output:

```txt
id name salary
```

Rows matched by:

id

---

Equivalent SQL:

```sql
SELECT *
FROM emp
INNER JOIN salary
ON emp.id = salary.id
```

---

Real-world Usage

Join:

customers + orders

 applications + jobs

 users + transactions

 events + metadata

---

Fun Analogy

Join()

≈ Merge two Excel sheets using Employee ID

---

Interview Question

Q:
What is an inner join?

Answer:

Returns only rows having matching keys in both datasets.

---

## Missing Keys in Inner Join

Example:

Employee table:

```txt
1 Harsha
2 Ravi
```

Salary table:

```txt
1 230000
```

Output:

```txt
Harsha survives

Ravi removed
```

Reason:

Inner join keeps only matching keys.

---

Interview Question

Q:
What happens if join key is missing?

Answer:

Inner join removes rows without matches.