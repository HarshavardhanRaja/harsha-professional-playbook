# alias()

## Goal

Rename columns temporarily in output.

Example:

```python
explicit_df.select(
    "name",
    explicit_df.salary.alias("employee_salary")
).show()
```

Output:

```txt
+------+---------------+
| name |employee_salary|
+------+---------------+
|Harsha|230000         |
|Ravi  |90000          |
+------+---------------+
```

---

Equivalent SQL:

```sql
SELECT
name,
salary AS employee_salary
FROM employees;
```

---

Fun Analogy

alias()

≈ Nickname

Real name:

salary

Displayed as:

employee_salary

---

Important

alias()

does NOT permanently rename columns.

Only changes output representation.

---

Interview Question

Q:
Difference between alias() and withColumnRenamed()?

Answer:

alias()

→ temporary output rename

withColumnRenamed()

→ permanently changes column name in DataFrame


---

## alias() does NOT modify schema

Check:

```python
explicit_df.printSchema()
```

Output:

```txt
root
 |-- salary: integer
```

Observation:

Schema still contains:

salary

not:

employee_salary

Therefore:

alias()

changes presentation only.

---

Interview Question

Q:
Does alias() permanently rename columns?

Answer:

No.

alias() only changes output representation.

Schema remains unchanged.