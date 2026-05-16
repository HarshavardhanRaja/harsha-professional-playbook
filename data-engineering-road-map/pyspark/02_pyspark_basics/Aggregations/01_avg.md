# Average Aggregation (avg)

## Goal

Calculate average values.

Example:

```python
explicit_df.groupBy().avg("salary").show()
```

Output:

```txt
avg(salary)

160000
```

Calculation:

```txt
(230000 + 90000)

↓

160000
```

---

Equivalent SQL:

```sql
SELECT AVG(salary)
FROM employees
```

---

Real-world Usage

Average:

salary

customer spend

session duration

transaction value

---

Interview Question

Q:
Why use groupBy().avg() instead of looping manually?

Answer:

Spark performs distributed aggregation efficiently across partitions.