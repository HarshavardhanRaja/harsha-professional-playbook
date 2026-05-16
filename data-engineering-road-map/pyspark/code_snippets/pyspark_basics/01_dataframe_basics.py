from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, avg, max, row_number, rank, dense_rank
from pyspark.sql.window import Window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

spark = SparkSession.builder \
    .appName("pyspark_dataframe_basics") \
    .master("local[*]") \
    .getOrCreate()

# -----------------------------
# 1. Create DataFrame
# -----------------------------
data = [
    (1, "Harsha", "Data Engineer", 230000),
    (2, "Ravi", "Data Analyst", 90000),
    (3, "Anu", "ML Engineer", 180000)
]

columns = ["id", "name", "role", "salary"]

df = spark.createDataFrame(data, columns)

print("1. Original DataFrame")
df.show()

print("2. Schema")
df.printSchema()

# -----------------------------
# 2. select()
# -----------------------------
print("3. select()")
df.select("name", "salary").show()

# -----------------------------
# 3. filter() / where()
# -----------------------------
print("4. filter()")
df.filter(df.salary > 100000).show()

print("5. where()")
df.where(df.role == "Data Engineer").show()

# -----------------------------
# 4. withColumn()
# -----------------------------
print("6. withColumn() - add new column")
df.withColumn("salary_in_lakhs", df.salary / 100000).show()

print("7. withColumn() - overwrite column")
df.withColumn("salary", df.salary + 10000).show()

# -----------------------------
# 5. alias()
# -----------------------------
print("8. alias()")
df.select(
    "name",
    df.salary.alias("employee_salary")
).show()

# -----------------------------
# 6. withColumnRenamed()
# -----------------------------
print("9. withColumnRenamed()")
renamed_df = df.withColumnRenamed("salary", "employee_salary")
renamed_df.show()

# -----------------------------
# 7. drop()
# -----------------------------
print("10. drop()")
df.drop("salary").show()

# -----------------------------
# 8. distinct() and count()
# -----------------------------
dup_df = spark.createDataFrame(
    [("Harsha",), ("Harsha",), ("Ravi",)],
    ["name"]
)

print("11. distinct()")
dup_df.distinct().show()

print("Before distinct:", dup_df.count())
print("After distinct:", dup_df.distinct().count())

# -----------------------------
# 9. orderBy()
# -----------------------------
print("12. orderBy ascending")
df.orderBy("salary").show()

print("13. orderBy descending")
df.orderBy(df.salary.desc()).show()

# -----------------------------
# 10. Schema inference issue
# -----------------------------
bad_df = spark.createDataFrame(
    [(1, "Harsha", "230000"), (2, "Ravi", "90000")],
    ["id", "name", "salary"]
)

print("14. Schema inference")
bad_df.printSchema()

print("15. Implicit casting")
bad_df.withColumn("salary_plus_bonus", bad_df.salary + 10000).show()

ugly_df = spark.createDataFrame(
    [(1, "Harsha", "230000"), (2, "Ravi", "unknown")],
    ["id", "name", "salary"]
)

print("16. Safe casting with try_cast")
ugly_df.withColumn(
    "salary_clean",
    expr("try_cast(salary as BIGINT)")
).show()

# -----------------------------
# 11. Explicit schema
# -----------------------------
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("salary", IntegerType(), True)
])

explicit_df = spark.createDataFrame(
    [(1, "Harsha", 230000), (2, "Ravi", 90000)],
    schema=schema
)

print("17. Explicit schema")
explicit_df.printSchema()
explicit_df.show()

# -----------------------------
# 12. Aggregations
# -----------------------------
dept_df = spark.createDataFrame(
    [
        ("Engineering", 230000),
        ("Engineering", 180000),
        ("Analytics", 90000)
    ],
    ["department", "salary"]
)

print("18. Average salary")
explicit_df.groupBy().avg("salary").show()

print("19. groupBy avg")
dept_df.groupBy("department").avg("salary").show()

print("20. groupBy count")
dept_df.groupBy("department").count().show()

print("21. agg()")
dept_df.groupBy("department").agg(
    avg("salary"),
    max("salary")
).show()

# -----------------------------
# 13. Joins
# -----------------------------
emp_df = spark.createDataFrame(
    [(1, "Harsha"), (2, "Ravi")],
    ["id", "name"]
)

salary_df = spark.createDataFrame(
    [(1, 230000)],
    ["id", "salary"]
)

print("22. Inner join")
emp_df.join(salary_df, on="id", how="inner").show()

print("23. Left join")
emp_df.join(salary_df, on="id", how="left").show()

print("24. Left anti join")
emp_df.join(salary_df, on="id", how="left_anti").show()

print("25. Left semi join")
emp_df.join(salary_df, on="id", how="left_semi").show()

# -----------------------------
# 14. Window functions
# -----------------------------
rank_df = spark.createDataFrame(
    [
        ("Engineering", "Harsha", 230000),
        ("Engineering", "Anu", 230000),
        ("Engineering", "Raj", 180000)
    ],
    ["department", "name", "salary"]
)

window_spec = Window.partitionBy("department").orderBy(rank_df.salary.desc())

print("26. row_number()")
rank_df.withColumn("row_number", row_number().over(window_spec)).show()

print("27. rank()")
rank_df.withColumn("rank", rank().over(window_spec)).show()

print("28. dense_rank()")
rank_df.withColumn("dense_rank", dense_rank().over(window_spec)).show()

# -----------------------------
# 15. Dedup latest record
# -----------------------------
user_df = spark.createDataFrame(
    [
        (1, "Harsha", "2025-01-01"),
        (1, "Harsha", "2025-02-01"),
        (2, "Ravi", "2025-01-15")
    ],
    ["id", "name", "updated_at"]
)

user_window = Window.partitionBy("id").orderBy(user_df.updated_at.desc())

latest_user_df = user_df.withColumn(
    "rn",
    row_number().over(user_window)
)

print("29. Latest record per user")
latest_user_df.filter("rn = 1").drop("rn").show()

# -----------------------------
# 16. Null handling
# -----------------------------
null_df = spark.createDataFrame(
    [
        ("Harsha", 230000),
        ("Ravi", None),
        ("Anu", 180000)
    ],
    ["name", "salary"]
)

print("30. Null data")
null_df.show()

print("31. dropna()")
null_df.dropna().show()

print("32. fillna()")
null_df.fillna({"salary": 0}).show()

spark.stop()