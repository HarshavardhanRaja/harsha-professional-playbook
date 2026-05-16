from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

spark = SparkSession.builder \
    .appName("window_dedup") \
    .master("local[*]") \
    .getOrCreate()

dup_users = [
    (1,"Harsha","2025-01-01"),
    (1,"Harsha","2025-02-01"),
    (2,"Ravi","2025-01-15")
]

user_df = spark.createDataFrame(
    dup_users,
    ["id","name","updated_at"]
)

window = Window.partitionBy(
    "id"
).orderBy(
    user_df.updated_at.desc()
)

latest = user_df.withColumn(
    "rn",
    row_number().over(window)
)

latest.filter(
    "rn = 1"
).drop(
    "rn"
).show()

spark.stop()