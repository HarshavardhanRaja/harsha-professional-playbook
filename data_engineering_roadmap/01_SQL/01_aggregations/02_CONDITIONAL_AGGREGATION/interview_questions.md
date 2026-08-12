# Conditional Aggregation - Interview Questions

---

# ⭐⭐⭐⭐⭐ MUST KNOW

---

## Q1. What is Conditional Aggregation?

### Ideal Answer

Conditional aggregation combines aggregate functions with `CASE` expressions to calculate metrics only for rows that satisfy specific conditions.

It allows multiple KPIs to be calculated in a single query.

### Why Interviewer Asked

Tests knowledge of one of the most commonly used SQL reporting techniques.

### Common Wrong Answer

> It is another way of filtering rows.

### Follow-up Questions

* Why not use multiple queries?
* Where have you used it in production?

---

## Q2. What is the most common Conditional Aggregation pattern?

### Ideal Answer

```sql
SUM(
    CASE
        WHEN condition THEN 1
        ELSE 0
    END
)
```

This counts rows satisfying a condition.

### Why Interviewer Asked

Tests familiarity with the standard SQL pattern.

### Common Wrong Answer

> Use WHERE with COUNT().

### Follow-up Questions

* Why does this work?
* Why use 1 and 0?

---

## Q3. Why does `SUM(CASE...)` work for counting?

### Ideal Answer

The `CASE` expression converts each row into either:

* `1` for matching rows
* `0` for non-matching rows

`SUM()` then adds these values together.

Example:

```text
1
0
1
0
1

↓

SUM

↓

3
```

### Why Interviewer Asked

Tests conceptual understanding.

### Common Wrong Answer

> SUM automatically counts rows.

---

## Q4. Why is `SUM(CASE...)` preferred over multiple queries?

### Ideal Answer

A single query can calculate multiple KPIs in one table scan.

This improves performance and simplifies dashboard queries.

### Why Interviewer Asked

Tests production thinking.

### Common Wrong Answer

> It only makes the SQL shorter.

### Follow-up Questions

* Why is one scan better?
* How does this help dashboards?

---

## Q5. Can Conditional Aggregation be combined with GROUP BY?

### Ideal Answer

Yes.

`GROUP BY` creates the groups, and conditional aggregation calculates multiple metrics independently inside each group.

Example:

```sql
SELECT
    department,
    COUNT(*) AS total,
    SUM(CASE WHEN salary > 100000 THEN 1 ELSE 0 END) AS high_salary
FROM employees
GROUP BY department;
```

### Why Interviewer Asked

Tests understanding of combining SQL concepts.

---

## Q6. Why is `ELSE 0` commonly used?

### Ideal Answer

It explicitly states that non-matching rows contribute zero.

Although `SUM()` ignores `NULL`, `ELSE 0` makes the query easier to understand and avoids ambiguity.

### Why Interviewer Asked

Tests SQL best practices.

### Common Wrong Answer

> ELSE 0 is mandatory.

---

## Q7. What happens if `ELSE` is omitted?

### Ideal Answer

SQL treats it as:

```sql
ELSE NULL
```

Since `SUM()` ignores `NULL`, the query often still works.

However, using `ELSE 0` is generally clearer.

### Why Interviewer Asked

Tests understanding of CASE expressions.

---

# ⭐⭐⭐⭐ FREQUENTLY ASKED

---

## Q8. What is the difference between `SUM(CASE...)` and `COUNT(CASE...)`?

### Ideal Answer

Both can perform conditional counting.

`SUM(CASE...)` is generally preferred because:

* It is more flexible.
* The same pattern works for counts and numeric totals.
* It is easier to extend for business metrics.

### Why Interviewer Asked

Tests SQL style and practical experience.

### Common Wrong Answer

> COUNT(CASE...) is always faster.

---

## Q9. Where have you used Conditional Aggregation in production?

### Ideal Answer

Examples include:

* KPI dashboards
* Success vs failure counts
* Revenue by payment type
* Active vs inactive users
* Customer segmentation
* Financial reports
* Order status summaries

---

## Q10. Why not use WHERE for every KPI?

### Ideal Answer

Using `WHERE` would require separate queries for each metric.

Conditional aggregation calculates multiple metrics in one query, reducing repeated table scans.

---

## Q11. Can Conditional Aggregation calculate sums as well as counts?

### Ideal Answer

Yes.

Example:

```sql
SUM(
    CASE
        WHEN status = 'SUCCESS'
        THEN amount
        ELSE 0
    END
)
```

This returns revenue only from successful orders.

---

## Q12. Why is Conditional Aggregation useful in dashboards?

### Ideal Answer

Dashboards usually display many KPIs together.

Conditional aggregation allows all those metrics to be calculated efficiently in one query, often with a single scan of the data.

---

# ⭐⭐⭐ NICE TO KNOW

---

## Q13. Can Conditional Aggregation be used with AVG()?

### Ideal Answer

Yes.

Example:

```sql
AVG(
    CASE
        WHEN department = 'IT'
        THEN salary
    END
)
```

`AVG()` ignores `NULL`, so non-matching rows are excluded automatically.

---

## Q14. What is the biggest mistake developers make with Conditional Aggregation?

### Ideal Answer

Writing multiple queries for related KPIs instead of calculating them together in one query.

Other common mistakes include:

* Forgetting `ELSE 0`
* Incorrect boundary conditions
* Using `WHERE` instead of conditional logic when multiple metrics are required

---

## Q15. Which pattern do you recommend for conditional counting?

### Ideal Answer

```sql
SUM(
    CASE
        WHEN condition THEN 1
        ELSE 0
    END
)
```

It is explicit, flexible, easy to read, and widely used in production code.

---

# Final Interview Tip

Whenever you see a reporting or dashboard requirement, ask yourself:

1. Can I calculate multiple KPIs in one query?
2. Can I use `SUM(CASE...)` instead of multiple `COUNT()` queries?
3. Should this be combined with `GROUP BY`?
4. Can I reduce the number of table scans?

Thinking this way demonstrates production-level SQL skills rather than just syntax knowledge.
