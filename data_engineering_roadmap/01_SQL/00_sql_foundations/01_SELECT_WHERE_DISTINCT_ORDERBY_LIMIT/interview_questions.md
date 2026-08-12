# SQL Query Basics - Interview Questions

---

# ⭐⭐⭐⭐⭐ MUST KNOW

---

## Q1. What does the SELECT clause do?

### Ideal Answer

The `SELECT` clause defines the final output of a SQL query. It specifies which columns should be returned after SQL has finished processing the data.

### Why Interviewer Asked

To verify you understand SQL execution order and don't think SELECT retrieves data first.

### Common Wrong Answer

> SELECT fetches data from the table.

### Follow-up Questions

* Does SELECT execute first?
* Why can't WHERE use SELECT aliases?

---

## Q2. Why should we avoid SELECT * in production?

### Ideal Answer

I avoid `SELECT *` because it:

* Reads unnecessary columns
* Increases I/O and cloud cost
* May expose sensitive columns
* Couples applications to schema changes
* Makes queries harder to read and maintain

### Why Interviewer Asked

To evaluate production engineering knowledge beyond SQL syntax.

### Common Wrong Answer

> It is slower.

### Follow-up Questions

* What is schema evolution?
* How does SELECT * increase cloud cost?
* Can it break APIs?

---

## Q3. What is the difference between WHERE and HAVING?

### Ideal Answer

WHERE filters individual rows before grouping.

HAVING filters groups after GROUP BY.

### Why Interviewer Asked

To test understanding of SQL execution order.

### Common Wrong Answer

> WHERE and HAVING both filter data.

### Follow-up Questions

* Why can't COUNT() be used in WHERE?
* Which executes first?

---

## Q4. Why can't aggregate functions be used in WHERE?

### Ideal Answer

Aggregate functions are calculated after GROUP BY, whereas WHERE executes before grouping. Therefore, aggregate values do not exist when WHERE is evaluated.

### Why Interviewer Asked

Tests execution order understanding.

### Common Wrong Answer

> SQL doesn't allow it.

### Follow-up Questions

* Which clause should be used instead?
* Explain the execution order.

---

## Q5. Why should we avoid functions in the WHERE clause?

### Ideal Answer

Applying functions on indexed or partitioned columns may prevent efficient index usage or partition pruning. Using range filters usually performs better.

### Why Interviewer Asked

Tests production SQL optimization.

### Common Wrong Answer

> Functions are slower.

### Follow-up Questions

* Rewrite `YEAR(order_date)=2025`.
* What is partition pruning?

---

## Q6. DISTINCT vs GROUP BY?

### Ideal Answer

If I only need unique values, I prefer DISTINCT because it clearly expresses the intent.

If I need aggregations such as COUNT(), SUM(), or AVG(), I use GROUP BY.

### Why Interviewer Asked

Tests understanding of SQL semantics.

### Common Wrong Answer

> They are exactly the same.

### Follow-up Questions

* Do they always produce identical results?
* Which is more readable?

---

## Q7. Why is DISTINCT sometimes considered a code smell?

### Ideal Answer

DISTINCT can hide problems caused by incorrect JOINs or data quality issues. Before using DISTINCT, I first understand why duplicates are being generated.

### Why Interviewer Asked

Tests debugging and production thinking.

### Common Wrong Answer

> DISTINCT removes duplicates, so it's always fine.

### Follow-up Questions

* What would you check first?
* When is DISTINCT appropriate?

---

## Q8. Why should LIMIT usually be used with ORDER BY?

### Ideal Answer

Without ORDER BY, SQL tables are logically unordered, so LIMIT may return different rows across executions.

ORDER BY makes the result deterministic.

### Why Interviewer Asked

Tests understanding of SQL behavior.

### Common Wrong Answer

> LIMIT returns the first N rows.

### Follow-up Questions

* Why can results change?
* Does SQL store rows in order?

---

## Q9. What is OFFSET? Why does it become slow?

### Ideal Answer

OFFSET skips rows before returning the requested rows.

As OFFSET increases, the database must process and discard more rows, making the query slower.

### Why Interviewer Asked

Tests pagination knowledge.

### Common Wrong Answer

> OFFSET jumps directly to that row.

### Follow-up Questions

* How would you paginate millions of rows?
* What is Cursor Pagination?

---

## Q10. Explain Cursor Pagination.

### Ideal Answer

Instead of skipping rows, Cursor Pagination uses the last retrieved value (usually an indexed column) to fetch the next set of rows.

It scales much better than OFFSET.

### Why Interviewer Asked

Tests real-world API and database knowledge.

### Common Wrong Answer

> It is another name for OFFSET.

### Follow-up Questions

* Why is it faster?
* When would you use it?

---

# ⭐⭐⭐⭐ FREQUENTLY ASKED

---

## Q11. Can ORDER BY use aliases?

**Ideal Answer**

Yes.

ORDER BY executes after SELECT, so aliases already exist.

---

## Q12. Can WHERE use aliases?

**Ideal Answer**

No.

WHERE executes before SELECT, so aliases are not available.

---

## Q13. What is the default sorting order?

**Ideal Answer**

ASC (Ascending).

---

## Q14. How does SQL sort multiple columns?

**Ideal Answer**

The first column is the primary sort key.

Subsequent columns break ties.

---

## Q15. Can ORDER BY use an index?

**Ideal Answer**

Yes, if the ordering matches the indexed column(s). Otherwise, the database performs a sort.

---

## Q16. What is Top-N optimization?

**Ideal Answer**

For queries using ORDER BY with LIMIT, modern databases often avoid sorting the entire dataset and instead use optimized algorithms to retrieve only the required top rows.

---

# ⭐⭐⭐ NICE TO KNOW

---

## Q17. Does SELECT execute first?

**Ideal Answer**

No.

SELECT executes after FROM, WHERE, GROUP BY, and HAVING.

---

## Q18. Why is explicit column selection considered a best practice?

**Ideal Answer**

It improves readability, performance, maintainability, and reduces cloud cost and security risks.

---

## Q19. What happens if a new column is added to a table using SELECT *?

**Ideal Answer**

The query automatically returns the new column, which may break APIs, downstream pipelines, or expose sensitive information.

---

## Q20. How would you review this query?

```sql
SELECT DISTINCT *
FROM orders
WHERE YEAR(order_date)=2025
LIMIT 100;
```

### Ideal Answer

Issues:

* Avoid SELECT *
* Avoid YEAR() in WHERE
* DISTINCT may hide data issues
* LIMIT should usually be paired with ORDER BY

I would first understand the business requirement before rewriting the query.

---

# Final Interview Tip

Don't just explain **what** SQL does.

Explain:

* Why it works
* When to use it
* When not to use it
* How it behaves in production

That's what differentiates a Senior Data Engineer from someone who only knows SQL syntax.
