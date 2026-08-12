# Aggregate Functions - Interview Questions

---

# ⭐⭐⭐⭐⭐ MUST KNOW

---

## Q1. What are aggregate functions?

### Ideal Answer

Aggregate functions perform calculations on multiple rows and return a single value.

Common aggregate functions are:

* COUNT()
* SUM()
* AVG()
* MIN()
* MAX()

### Why Interviewer Asked

To verify your understanding of aggregation.

### Common Wrong Answer

> Aggregate functions work on one row at a time.

### Follow-up Questions

* Can aggregate functions return multiple rows?
* Which aggregate functions do you use most often?

---

## Q2. What is the difference between COUNT(*) and COUNT(column)?

### Ideal Answer

`COUNT(*)` counts every row.

`COUNT(column)` counts only non-NULL values in that column.

### Why Interviewer Asked

Very common SQL interview question.

### Common Wrong Answer

> Both always return the same result.

### Follow-up Questions

* What happens if every value is NULL?
* Which one would you use to count employees who received a bonus?

---

## Q3. What is COUNT(DISTINCT)?

### Ideal Answer

`COUNT(DISTINCT column)` returns the number of unique non-NULL values.

It first identifies unique values and then counts the non-NULL ones.

### Why Interviewer Asked

Tests understanding of DISTINCT with aggregates.

### Common Wrong Answer

> It counts all distinct values including NULL.

### Follow-up Questions

* How many NULL values are counted?
* Why is COUNT(DISTINCT) slower than COUNT(*)?

---

## Q4. How does AVG() work internally?

### Ideal Answer

Conceptually,

```text
AVG(column)

↓

SUM(column)

↓

COUNT(column)

↓

SUM / COUNT(column)
```

This is why AVG ignores NULL values.

### Why Interviewer Asked

Tests conceptual understanding rather than syntax.

### Common Wrong Answer

> AVG has its own independent algorithm.

### Follow-up Questions

* Why doesn't AVG divide by COUNT(*)?
* How are NULL values handled?

---

## Q5. How do aggregate functions handle NULL values?

### Ideal Answer

All common aggregate functions ignore NULL values except `COUNT(*)`, which counts rows.

| Function      | NULL Handling |
| ------------- | ------------- |
| COUNT(*)      | Counts rows   |
| COUNT(column) | Ignores NULL  |
| SUM           | Ignores NULL  |
| AVG           | Ignores NULL  |
| MIN           | Ignores NULL  |
| MAX           | Ignores NULL  |

### Why Interviewer Asked

Tests one of SQL's most important concepts.

### Common Wrong Answer

> NULL is treated as zero.

### Follow-up Questions

* What happens if every value is NULL?
* How does COUNT(column) behave?

---

## Q6. How do MIN() and MAX() work internally?

### Ideal Answer

They scan the rows once while maintaining the current minimum or maximum value.

Sorting the data is not required.

### Why Interviewer Asked

Tests algorithmic thinking.

### Common Wrong Answer

> SQL sorts the entire table and picks the first or last value.

### Follow-up Questions

* Why is scanning more efficient than sorting?
* Does an index change execution?

---

## Q7. Why is COUNT(DISTINCT) more expensive than COUNT(*)?

### Ideal Answer

`COUNT(*)` simply counts rows.

`COUNT(DISTINCT)` must detect duplicate values before counting, usually using hashing or sorting, which requires additional CPU and memory.

### Why Interviewer Asked

Tests production and performance awareness.

### Common Wrong Answer

> Both perform the same amount of work.

### Follow-up Questions

* What happens on a table with 100 million rows?
* When would you avoid COUNT(DISTINCT)?

---

## Q8. Would you use AVG() or SUM()/COUNT()?

### Ideal Answer

I prefer `AVG()` because it correctly handles NULL values and avoids common mistakes such as integer division.

### Why Interviewer Asked

Tests production experience.

### Common Wrong Answer

> They are always identical.

### Follow-up Questions

* When would you manually calculate the average?
* How would you avoid integer division?

---

# ⭐⭐⭐⭐ FREQUENTLY ASKED

---

## Q9. Explain the difference between COUNT(*) and COUNT(1).

### Ideal Answer

In modern databases, both generally produce the same execution plan and similar performance.

`COUNT(*)` is preferred because it clearly expresses the intention of counting rows.

### Why Interviewer Asked

Common SQL optimization question.

### Common Wrong Answer

> COUNT(1) is always faster.

### Follow-up Questions

* Which databases optimize them the same way?
* Which version do you prefer?

---

## Q10. Why can manually calculating AVG lead to incorrect results?

### Ideal Answer

Using:

```sql
SUM(column) / COUNT(*)
```

can produce incorrect results because:

* COUNT(*) includes NULL rows.
* Some databases perform integer division when both operands are integers.

Using AVG() avoids these issues.

### Why Interviewer Asked

Tests practical SQL knowledge.

### Follow-up Questions

* How would you fix integer division?
* Why is COUNT(column) preferred?

---

## Q11. Which aggregate function is generally the fastest?

### Ideal Answer

`COUNT(*)` is generally the simplest and most efficient because SQL only needs to count rows.

### Follow-up Questions

* Which is usually the slowest?
* Why?

---

## Q12. Can aggregate functions be used in the WHERE clause?

### Ideal Answer

No.

Aggregate functions are computed after the WHERE clause.

Filtering aggregated values should be done using HAVING.

### Why Interviewer Asked

Prepares candidates for GROUP BY and HAVING.

### Follow-up Questions

* Why does SQL process WHERE before aggregates?
* Which clause should be used instead?

---

# ⭐⭐⭐ NICE TO KNOW

---

## Q13. Why doesn't COUNT(DISTINCT) count NULL?

### Ideal Answer

DISTINCT keeps a single NULL value, but COUNT(column) ignores NULL values.

Therefore, COUNT(DISTINCT column) returns the number of unique non-NULL values.

---

## Q14. Where have you used aggregate functions in production?

### Ideal Answer

Examples include:

* Dashboard KPIs
* Financial reports
* User analytics
* Order summaries
* Daily metrics
* Data quality validation
* Monitoring and alerting

---

## Q15. Which aggregate function do you think is the most expensive?

### Ideal Answer

Usually `COUNT(DISTINCT)` because SQL must identify unique values before counting.

The exact cost depends on the execution plan, indexing, and database engine.

---

# Final Interview Tip

Don't stop at explaining **what** an aggregate function does.

Interviewers are often looking for:

* How it works conceptually
* How it handles NULL values
* Performance implications
* Production use cases
* Common pitfalls

Those points distinguish a Senior Data Engineer from someone who has only memorized SQL syntax.
