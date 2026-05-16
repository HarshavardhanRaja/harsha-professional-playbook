# Shuffle

A shuffle redistributes data across partitions and executors.

## Common Causes

- Joins.
- GroupBy aggregations.
- Distinct.
- Repartition.
- OrderBy.

Shuffles are expensive because they involve network and disk I/O.
