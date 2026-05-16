# Partitions

## Goal

Understand how Spark splits data.

Code:

```python
explicit_df.rdd.getNumPartitions()
```

Output:

```txt
10
```

Observation:

Spark divided data into partitions.

---

What is a partition?

A partition is a chunk of data processed independently.

Think:

1 TB data

↓

Split into:

250 GB
250 GB
250 GB
250 GB

↓

Processed in parallel

---

Why Spark is fast?

Parallel processing.

Multiple partitions

↓

Multiple executors/workers

↓

Faster computation

---

Fun Analogy

Partition = pizza slice

Whole pizza:

slow to eat

Slices:

multiple people eat simultaneously

---

Interview Question

Q:
What is a partition in Spark?

Answer:

A partition is a logical chunk of distributed data processed independently by Spark tasks.

---

Interview Question

Q:
Why do partitions improve performance?

Answer:

Partitions enable parallel execution across executors.


---

## Partitions Can Be Empty

Code:

```python
explicit_df.rdd.glom().collect()
```

Output:

```txt
[[], [], [], [], [Harsha], [], [], [], [], [Ravi]]
```

Meaning:

Spark created 10 partitions, but most are empty.

Important:

```txt
Partitions are containers, not records.
```

## Fun Analogy

10 delivery workers.

Only 2 packages.

Some workers get work.

Others stay idle.

## Interview Question

Q: Can Spark partitions be empty?

Answer:

Yes. Spark can create more partitions than available records, especially with small datasets or default parallelism.

---

## repartition()

Code:

```python
explicit_df.repartition(2).rdd.glom().collect()

[[Harsha, Ravi], []]

Meaning:

Spark created 2 partitions.

One partition has data.

One partition is empty.

Key Takeaway

repartition(n) controls number of partitions.

It does not guarantee every partition will have rows, especially for tiny datasets.

Interview Question

Q: What does repartition(n) do?

Answer:

It creates a new DataFrame with n partitions and usually causes a shuffle.

---

## repartition() Causes Shuffle

Code:

```python
explicit_df.repartition(2).explain()
```

Output contains:

```txt
Exchange RoundRobinPartitioning(2)
```

Meaning:

`Exchange` indicates data movement/shuffle.

## Interview Question

Q: Is repartition() expensive?

Answer:

Yes. `repartition()` usually causes a shuffle because Spark redistributes data across partitions.