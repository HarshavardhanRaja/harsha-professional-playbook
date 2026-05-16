# Distributed Computing

Distributed computing splits work across multiple machines so large workloads can run faster and handle more data.

## Concepts

- Cluster: group of machines working together.
- Driver: coordinates the application.
- Executors: run tasks on worker nodes.
- Partition: slice of data processed independently.
- Task: smallest unit of execution in Spark.

## Mental Model

Spark divides data into partitions, creates tasks for those partitions, and runs those tasks across executors.
