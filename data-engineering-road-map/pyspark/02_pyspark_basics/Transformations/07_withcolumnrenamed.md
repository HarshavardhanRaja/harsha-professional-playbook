# withColumnRenamed()

## Goal

Permanently rename columns.

Example:

```python
renamed_df = explicit_df.withColumnRenamed(
    "salary",
    "employee_salary"
)

renamed_df.printSchema()
```

Output:

```txt
root
 |-- employee_salary: integer
```

Observation:

Schema changed.

Rename is permanent for new DataFrame.

---

Difference:

alias()

→ temporary rename

withColumnRenamed()

→ schema rename

---

Fun Analogy

alias()

≈ nickname

withColumnRenamed()

≈ legal name change

---

Interview Question

Q:
Difference between alias() and withColumnRenamed()?

Answer:

alias()

changes display/output

withColumnRenamed()

changes actual schema


---

## DataFrames are Immutable

Check original DataFrame:

```python
explicit_df.printSchema()


Key Rule:

Spark DataFrames are immutable.

Interview Question:

Q: Are Spark DataFrames mutable?

Answer:

No. Transformations return new DataFrames instead of modifying existing ones.