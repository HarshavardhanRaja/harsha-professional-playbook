# Broadcast Joins

Broadcast joins send a small table to all executors so Spark can avoid shuffling a large table.

Use them when one side of the join is small enough to fit safely in executor memory.
