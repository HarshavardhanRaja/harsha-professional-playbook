# Creating First DataFrame

DataFrames are Spark's primary abstraction for structured data.

Think:

DataFrame ≈ SQL Table ≈ Excel Sheet ≈ Pandas DataFrame

Example:

```python
data = [
    (1,"Harsha","Data Engineer",230000),
    (2,"Ravi","Data Analyst",90000)
]

columns=["id","name","role","salary"]

df = spark.createDataFrame(data, columns)

df.show()


Interview Question:
Q: What is a DataFrame?
Answer: A DataFrame is a distributed collection of structured data organized into named columns.