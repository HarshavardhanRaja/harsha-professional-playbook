# Window Functions — Introduction

## Goal

Perform calculations within a group without collapsing rows.

Example data:

```txt
Engineering → Harsha → 230000
Engineering → Anu    → 180000
Analytics   → Ravi   → 90000


Why Window Functions?

Unlike groupBy, window functions keep row-level details.

Useful for:

ranking
deduplication
latest record per user
running totals
moving averages
Interview Question

Q: Difference between groupBy and window functions?

Answer:

groupBy collapses rows into one result per group.

Window functions calculate within groups while keeping original rows.


---

## row_number()

Code:

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

window_spec = Window.partitionBy("department").orderBy(rank_df.salary.desc())

ranked_df = rank_df.withColumn(
    "rank_in_department",
    row_number().over(window_spec)
)

ranked_df.show()
```

Output:

```txt
Analytics   Ravi   90000   1
Engineering Harsha 230000  1
Engineering Anu    180000  2
```

## Explanation

`partitionBy("department")`

means:

Create separate ranking groups per department.

`orderBy(salary.desc())`

means:

Inside each department, sort salary highest to lowest.

`row_number()`

means:

Assign unique sequence number.

## Fun Analogy

Window function is like ranking students inside each classroom.

Classroom = department

Marks = salary

Rank = row number

## Interview Question

Q: What does partitionBy do in window functions?

Answer:

It defines groups within which the window calculation is applied.

## Interview Question

Q: Difference between groupBy and window?

Answer:

groupBy collapses rows.

Window functions keep original rows and add calculated values.


---

## Top 1 Record Per Group

Code:

```python
ranked_df.filter(
    ranked_df.rank_in_department == 1
).show()
```

Output:

```txt
Analytics   Ravi    90000
Engineering Harsha 230000
```

## Real-world Usage

Find:

- latest record per customer
- highest salary per department
- most recent order per user
- top transaction per account

## Interview Question

Q: How do you find the highest salary per department in PySpark?

Answer:

Use a window partitioned by department, ordered by salary descending, then filter row_number = 1.

---

## Execution Plan for Window Function

Code:

```python
ranked_df.explain()
```

Output contained:

```txt
Exchange
Sort
Window
```

Interpretation:

Scan data

↓

Shuffle rows (Exchange)

↓

Sort rows

↓

Apply ranking

---

Important Concept:

Exchange = Shuffle

Shuffle means:

Move data across partitions.

Shuffle is expensive.

---

Interview Question

Q:
Why are window functions expensive?

Answer:

Window functions often require shuffle and sorting operations, increasing execution cost.

---

Key Takeaway

Window functions are powerful but can trigger expensive Spark operations.