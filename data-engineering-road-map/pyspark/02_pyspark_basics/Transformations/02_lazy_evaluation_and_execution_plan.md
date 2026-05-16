# Lazy Evaluation + Execution Plans

## Goal

Understand what Spark does internally before executing code.

---

Code:

```python
new_df = df.select("name", "salary")

new_df.explain()
```

Output:

```txt
== Physical Plan ==
*(1) Project [name#1, salary#3L]
+- *(1) Scan ExistingRDD[id#0L,name#1,role#2,salary#3L]
```

---

# How to Read Execution Plans

Read BOTTOM → TOP

Spark executes:

```txt
Scan data
    ↓
Apply transformation
    ↓
Return result
```

---

## Meaning of Scan

```txt
Scan ExistingRDD
```

Spark:

"I need to read existing data"

Equivalent:

Opening CSV / Parquet / Table

---

## Meaning of Project

```txt
Project [name, salary]
```

Project = select columns

Equivalent SQL:

```sql
SELECT name, salary
FROM employees
```

---

# Important Concept

Transformations:

```python
select()
filter()
join()
withColumn()
```

do NOT execute immediately.

Actions:

```python
show()
count()
collect()
write()
```

trigger execution.

This is called:

# Lazy Evaluation

---

Analogy:

Spark ≈ Swiggy Cart

```txt
Add item
Add item
Apply coupon

↓

No order yet

↓

PAY

↓

Execution happens
```

---

Interview Question:

Q:
What is lazy evaluation?

Answer:

Spark delays execution until an action is triggered, allowing optimization and better execution planning.

---

Interview Question:

Q:
Why use explain()?

Answer:

`explain()` reveals Spark execution plans and helps understand optimization and performance bottlenecks.