# DAG

A DAG, or directed acyclic graph, represents the sequence of Spark transformations needed to compute a result.

Spark builds the DAG lazily and executes it only when an action is called.
