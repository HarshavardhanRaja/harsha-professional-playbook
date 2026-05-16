# select() and Lazy Evaluation

Example:

```python
new_df = df.select("name","salary")

new_df.show()


Interview Question:
Q: What is lazy evaluation?
Answer: Spark delays execution of transformations until an action is triggered, allowing optimization before computation.