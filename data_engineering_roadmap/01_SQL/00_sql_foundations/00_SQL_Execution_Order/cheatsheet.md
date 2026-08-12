# SQL Execution Order Cheat Sheet

## Execution Order

```text
FROM
JOIN
WHERE
GROUP BY
HAVING
SELECT
DISTINCT
ORDER BY
LIMIT
```

---

## Easy Memory Trick

```text
Rows
↓
Groups
↓
Output
```

### Rows

```text
FROM
JOIN
WHERE
```

### Groups

```text
GROUP BY
HAVING
```

### Output

```text
SELECT
DISTINCT
ORDER BY
LIMIT
```

---

## WHERE vs HAVING

| WHERE | HAVING |
|---------|---------|
| Filters Rows | Filters Groups |
| Before GROUP BY | After GROUP BY |
| Cannot Use Aggregates | Can Use Aggregates |

---

## Alias Rules

❌ Invalid

```sql
SELECT salary AS sal
FROM employees
WHERE sal > 100000;
```

✅ Valid

```sql
SELECT salary AS sal
FROM employees
ORDER BY sal;
```

---

## Interview Triggers

Question mentions:

- Filter rows → WHERE
- Filter groups → HAVING
- Alias issue → Execution Order
- Aggregate issue → Execution Order

---

## Gotchas

❌ Alias in WHERE

❌ COUNT(*) in WHERE

❌ SUM() in WHERE

❌ AVG() in WHERE

✅ Alias in ORDER BY

✅ COUNT(*) in HAVING