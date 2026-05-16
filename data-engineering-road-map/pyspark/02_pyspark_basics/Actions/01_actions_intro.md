# Spark Actions

## What are Actions?

Actions trigger execution.

Spark transformations are lazy.

Spark actions force execution.

Think:

Transformations:

```txt
select()

filter()

join()

withColumn()
```

↓

Plan created

Actions:

```txt
show()

count()

collect()
```

↓

Execution starts

---

Fun Analogy

Spark:

```txt
Add items to cart
Apply coupon
Browse

↓

No purchase

↓

PAY

↓

Execution
```

Actions = PAY button

---

## show()

Example:

```python
df.show()
```

Purpose:

Display rows

Returns:

Console output

---

## count()

Example:

```python
df.count()
```

Purpose:

Count rows

Returns:

Integer

---

Interview Question

Q:
Difference between transformations and actions?

Answer:

Transformations build execution plans lazily.

Actions trigger execution and return results.

---

Interview Question

Q:
Is count() an action?

Answer:

Yes.

count() triggers Spark execution.