# Explicit Schema

## Goal

Tell Spark exactly what data types to use.

---

Code:

```python
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType
)

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("salary", IntegerType(), True)
])

explicit_df = spark.createDataFrame(
    data,
    schema=schema
)

explicit_df.printSchema()
```

Output:

```txt
root
 |-- id: integer
 |-- name: string
 |-- salary: integer
```

---

Why use explicit schemas?

Avoid:

Wrong inference

Unexpected strings

Failed aggregations

Pipeline failures

---

Fun Analogy

Schema inference:

Spark guesses your order.

Explicit schema:

You tell restaurant exactly what you want.

---

Interview Question

Q:
Why prefer explicit schema over inference?

Answer:

Explicit schemas improve reliability, performance, and prevent incorrect type inference.

---

Key Takeaway

Production Spark pipelines commonly define schemas explicitly.

---

## Explicit Schema Catches Bad Data Early

Example:

```python
bad_data = [
    (1, "Harsha", "abc")
]

spark.createDataFrame(
    bad_data,
    schema=schema
).show()
```

Error:

```txt
field salary: IntegerType() can not accept object 'abc' in type <class 'str'>
```

## Why this is good

Spark rejected bad data immediately.

Without explicit schema, Spark may infer salary as string and fail later during calculations.

## Fun Analogy

Explicit schema is like a strict security guard.

Rule:

```txt
salary must be integer
```

Input:

```txt
abc
```

Result:

```txt
Rejected at gate
```

## Interview Question

Q: How does explicit schema help in production Spark pipelines?

Answer:

It validates expected data types early, prevents incorrect schema inference, and reduces downstream failures.