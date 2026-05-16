# SparkSession

## What is it?

SparkSession is the entry point to PySpark.

Without SparkSession:

No DataFrames

No SQL

No Reading files

No Transformations

Think:

SparkSession ≈ BigQuery Client ≈ DB Connection

Example:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("demo") \
    .master("local[*]") \
    .getOrCreate()

```

Interview Question:
Q: What is SparkSession?
Answer:
SparkSession is the unified entry point used to interact with Spark functionality such as DataFrames, SQL, and file operations.