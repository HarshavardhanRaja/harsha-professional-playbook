# Spark Architecture

Spark applications run using a driver process and executor processes.

## Main Components

- Driver program: owns the SparkSession and builds the execution plan.
- Cluster manager: allocates resources.
- Executors: run tasks and cache data.
- Jobs: triggered by actions.
- Stages: groups of tasks separated by shuffle boundaries.
- Tasks: units of work sent to executors.

## Execution Flow

1. User code defines transformations.
2. An action triggers execution.
3. Spark builds a logical plan.
4. Spark optimizes and creates a physical plan.
5. Tasks run across executors.
