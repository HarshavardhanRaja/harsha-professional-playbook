# Schema Inference

Example:

```python
bad_data = [
 (1,"Harsha","230000"),
 (2,"Ravi","90000")
]

bad_df = spark.createDataFrame(
 bad_data,
 ["id","name","salary"]
)

bad_df.printSchema()
```

Output:

```txt
salary: string
```

---

Observation:

Salary should be numeric.

Spark inferred:

string

because values were passed as strings.

---

Why dangerous?

Wrong schema causes:

Failed aggregations

Incorrect joins

Slow processing

Unexpected errors

---

Real-world Example

CSV:

```txt
salary

230000
90000
unknown
```

Spark:

```txt
salary → string
```

Pipeline may fail later.

---

Interview Question

Q:
Why avoid relying completely on schema inference?

Answer:

Schema inference may assign incorrect types, causing runtime issues and poor performance.

---

Key Takeaway

Production pipelines often use explicit schemas.

---

## Implicit Type Casting

Example:

```python
bad_df.withColumn(
 "salary_plus_bonus",
 bad_df.salary + 10000
)
```

Observation:

Spark converted strings to numbers automatically.

Output:

```txt
"230000"
↓
240000
```

---

Danger:

Works for:

```txt
230000
90000
```

Fails for:

```txt
abc
unknown
```

---

Interview Question

Q:
Does Spark perform implicit casting?

Answer:

Yes.

Spark may automatically cast compatible types, but relying on implicit casting is risky in production pipelines.


---

## When Implicit Casting Fails

Example:

```python
ugly_data = [
    (1, "Harsha", "230000"),
    (2, "Ravi", "unknown")
]

ugly_df = spark.createDataFrame(
    ugly_data,
    ["id","name","salary"]
)

ugly_df.withColumn(
    "salary_plus_bonus",
    ugly_df.salary + 10000
).show()
```

Error:

```txt
CAST_INVALID_INPUT

The value 'unknown' of the type STRING cannot be cast to BIGINT.
```

## Why it failed

Spark tried to convert salary from string to number.

This works:

```txt
"230000" → 230000
```

This fails:

```txt
"unknown" → number ❌
```

## Fun Analogy

Spark is like a cashier.

If you give:

```txt
"230000"
```

cashier says:

> Fine, this looks like money.

If you give:

```txt
"unknown"
```

cashier says:

> I cannot calculate with this.

## Interview Question

Q: Why can schema inference be dangerous in Spark?

Answer:

Because Spark may infer wrong types, such as reading numeric fields as strings. Later transformations may fail when Spark tries to cast malformed values.

## Key Takeaway

Never blindly trust inferred schemas in production.

---

## Safe Casting with try_cast

Code:

```python
from pyspark.sql.functions import expr

ugly_df.withColumn(
    "salary_clean",
    expr("try_cast(salary as BIGINT)")
).show()
```

Output:

```txt
+---+------+-------+------------+
| id|  name| salary|salary_clean|
+---+------+-------+------------+
|  1|Harsha| 230000|      230000|
|  2|  Ravi|unknown|        NULL|
+---+------+-------+------------+
```

Key Idea:

`try_cast` converts valid values and returns NULL for bad values.

Interview Question:

Q: How do you safely cast malformed numeric strings in Spark?

Answer:

Use `try_cast` so malformed values become NULL instead of failing the job.