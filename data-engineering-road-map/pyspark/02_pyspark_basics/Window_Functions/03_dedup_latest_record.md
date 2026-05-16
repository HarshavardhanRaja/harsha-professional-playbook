# Deduplication — Latest Record Per Key

## Goal

Keep only the latest record per id.

## Input

```txt
1 Harsha 2025-01-01
1 Harsha 2025-02-01
2 Ravi   2025-01-15

from pyspark.sql.functions import row_number
from pyspark.sql.window import Window

user_window = Window.partitionBy("id").orderBy(user_df.updated_at.desc())

latest_user_df = user_df.withColumn(
    "rn",
    row_number().over(user_window)
)

latest_user_df.show()

Interview Question

Q: How do you get the latest record per user in PySpark?

Answer:

Use row_number() over a window partitioned by user id and ordered by timestamp descending, then filter rn = 1.