# Skew

Data skew happens when some partitions contain much more data than others.

## Symptoms

- A few tasks run much longer than the rest.
- Executors appear idle while one task continues.
- Shuffle stages are slow.

## Common Fixes

- Salting keys.
- Broadcast joins.
- AQE skew join handling.
- Better partitioning strategy.
