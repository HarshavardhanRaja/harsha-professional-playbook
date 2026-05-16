# Left Anti Join

## Goal

Find rows in left table that do NOT have a match in right table.

Example:

```python
emp_df.join(
    salary_df,
    on="id",
    how="left_anti"
).show()
```

Output:

```txt
Ravi
```

## Real-world Usage

Find:

- customers without orders
- employees without salaries
- applications without jobs
- records missing in target table
- data quality gaps

## SQL Equivalent

```sql
SELECT *
FROM emp
WHERE id NOT IN (
    SELECT id FROM salary
)
```

## Fun Analogy

left_anti join is like a missing-report detector.

Question:

> Who is present in employee table but missing salary data?

Answer:

> Ravi

## Interview Question

Q: What is left anti join?

Answer:

Left anti join returns rows from the left dataset that do not have matching keys in the right dataset.