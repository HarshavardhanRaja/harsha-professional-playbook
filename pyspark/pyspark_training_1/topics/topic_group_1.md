### What is SPARK ?
----
It is a general purpose in memory computation engine 

### What are benefits of Apache SPARK ?
----
1. It is faster than mapreduce (as processing happens in-memory)
2. Developer Friendly (natively supports java, python, scala, R)
3. multiple workloads

### Spark Architecture (Master Slave architecture)
----

It uses distributed processing i.e if it takes 1 hour to process xGB of data for a machine if we can divide the data to into small chunks and use multiple machines to process each chunk we can reduce the processing time by a lot. So It doesn't makes sense to use pyspark for smaller datasets but for larger datasets using spark's distributed framework we can process data very fast compared to traditional approach. 

Cluster: A group of machines that work together to analyse and process data. A cluster consists of multiple **Nodes** (kind of like machines) one of the node acts as master and the rest acts as slave. 

