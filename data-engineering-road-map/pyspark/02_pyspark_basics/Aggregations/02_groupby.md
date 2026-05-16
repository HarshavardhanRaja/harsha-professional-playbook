# groupBy()

## Goal

Aggregate data by categories.

Example:

```python
dept_df.groupBy(
 "department"
).avg("salary").show()
```

Output:

```txt
Engineering → 205000

Analytics → 90000
```

---

Equivalent SQL:

```sql
SELECT
department,
AVG(salary)

FROM employees

GROUP BY department
```

---

Real-world Usage

Average salary by department

Orders by country

Revenue by product

Transactions by user

---

Fun Analogy

groupBy()

≈ Create buckets

Engineering bucket

Analytics bucket

Then calculate metrics.

---

Interview Question

Q:
What happens internally during groupBy()?

Answer:

Spark performs shuffle operations to group similar keys together before aggregation.