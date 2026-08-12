"""

*Question:** *


"Build a mini aggregation engine. Given a list of records (dicts), a list of columns to group by, and a list of aggregations, 
return one row per group with the aggregates. Support `SUM`, `COUNT`, `AVG`, `MIN`, `MAX`, `COUNT DISTINCT`. 
Group-by can be multiple columns. Assume the data fits in memory for now."*

```python
records = [
  {"region": "US", "product": "A", "revenue": 100, "order_id": 1},
  {"region": "US", "product": "A", "revenue": 50,  "order_id": 1},
  {"region": "US", "product": "B", "revenue": 30,  "order_id": 2},
  {"region": "EU", "product": "A", "revenue": 80,  "order_id": 3},
]
group_by = ["region", "product"]
aggs = [("total_rev", "revenue", "sum"),
        ("orders",    "order_id", "count_distinct")]
```




"""