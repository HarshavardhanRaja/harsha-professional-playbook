# Day 002 — Spark Internals Start

Main realization:

Partitions are NOT records.

Partitions are containers.

Example:

3 records

↓

10 partitions

↓

Many partitions can be empty

Code:

```python
df.rdd.glom().collect()
```

Learning:

Empty partitions are possible.

repartition()

↓

Changes partition count

↓

Usually causes shuffle (Exchange in explain plan)

Key interview takeaway:

Partition = logical chunk of distributed data

Shuffle = movement of data across partitions

Questions to revisit:

- repartition vs coalesce
- shuffle
- executors
- tasks
- stages