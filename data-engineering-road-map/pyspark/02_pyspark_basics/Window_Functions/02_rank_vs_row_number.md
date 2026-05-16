## dense_rank()

If values are tied, they get the same rank.

Unlike rank(), dense_rank() does not skip numbers.

Example:

```txt
Harsha 230000 → 1
Anu    230000 → 1
Raj    180000 → 2


Interview Question

Q: Difference between rank() and dense_rank()?

Answer:

rank() gives same rank for ties but skips the next rank.

dense_rank() gives same rank for ties and does not skip ranks.


## row_number()

Assigns unique sequence numbers.

Example:

```txt
Harsha 230000 → 1
Anu    230000 → 2
Raj    180000 → 3
```

Observation:

Same salary

↓

Different row numbers

---

Use Cases

Deduplication

Latest record per user

Top 1 record per group

---

Interview Question

Q:
When would you prefer row_number()?

Answer:

Use row_number() when unique ordering is required, such as deduplication or selecting latest records.