# Left Semi Join

## Goal

Return rows from LEFT table only when matching keys exist in RIGHT table.

Example:

```python
emp_df.join(
 salary_df,
 on="id",
 how="left_semi"
).show()
```

Output:

```txt
Harsha
```

Observation:

Only LEFT columns returned.

---

Difference:

Inner Join:

returns both table columns

Semi Join:

returns only left table columns

---

Real-world Usage

Find customers having orders

Find employees with salaries

Find applications having jobs

---

Interview Question

Q:
Difference between inner join and left_semi join?

Answer:

Inner join returns columns from both datasets.

left_semi returns only left dataset rows having matches.