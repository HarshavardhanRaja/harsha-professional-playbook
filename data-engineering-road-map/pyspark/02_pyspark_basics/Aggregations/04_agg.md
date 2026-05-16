# agg()

## Goal

Apply multiple aggregations together.

Example:

```python
from pyspark.sql.functions import avg, max

dept_df.groupBy(
 "department"
).agg(
 avg("salary"),
 max("salary")
).show()
```

Output:

Engineering:

Average → 205000

Maximum → 230000

---

Equivalent SQL:

```sql
SELECT
department,
AVG(salary),
MAX(salary)

FROM employees

GROUP BY department
```

---

Why use agg()?

Need multiple metrics:

avg

sum

max

min

count

in one operation

---

Real-world Usage

Revenue dashboards

Business reports

Monitoring

KPIs

---

Interview Question

Q:
Why prefer agg()?

Answer:

agg() enables multiple aggregations efficiently in a single grouped operation.