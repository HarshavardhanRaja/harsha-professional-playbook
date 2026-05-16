# distinct()

## Goal

Remove duplicate rows.

Example:

```python
dup_df.distinct().show()
```

Output:

```txt
Harsha
Ravi
```

Duplicates removed.

---

Equivalent SQL:

```sql
SELECT DISTINCT name
FROM employees
```

---

Real-world Usage

Remove duplicate:

customers

transactions

events

logs

---

Fun Analogy

distinct()

≈ Security guard checking duplicate tickets

Same person entered twice?

Keep one.

---

Interview Question

Q:
What does distinct() do?

Answer:

Returns unique rows by removing duplicates.

---

## count()

Code:

```python
dup_df.count()

dup_df.distinct().count()
```

Output:

```txt
Before: 3
After: 2
```

Observation:

Duplicates removed.

---

Important:

count()

is an ACTION.

Actions trigger execution.

Examples:

```python
show()

count()

collect()
```

Transformations:

```python
filter()

select()

distinct()
```

---

Interview Question

Q:
Is count() transformation or action?

Answer:

count() is an action because it triggers execution and returns result.