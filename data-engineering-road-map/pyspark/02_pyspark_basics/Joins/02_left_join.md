# Left Join

## Goal

Keep all rows from left table.

Example:

```python
emp_df.join(
 salary_df,
 on="id",
 how="left"
).show()
```

Output:

```txt
Harsha → 230000

Ravi → NULL
```

---

Equivalent SQL:

```sql
LEFT JOIN
```

---

Rule:

Keep:

ALL rows from LEFT table

Matched rows from RIGHT

Missing matches:

NULL

---

Fun Analogy

Left join:

Attendance sheet

Keep all employees

Missing salary?

Mark NULL

---

Interview Question

Q:
Difference between inner join and left join?

Answer:

Inner join keeps only matching rows.

Left join keeps all rows from left dataset and fills unmatched values with NULL.