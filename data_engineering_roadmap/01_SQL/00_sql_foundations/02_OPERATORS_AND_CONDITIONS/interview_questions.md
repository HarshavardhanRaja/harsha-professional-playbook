# Operators and Conditions - Interview Questions

---

# ⭐⭐⭐⭐⭐ MUST KNOW

---

## Q1. What are comparison operators in SQL?

### Ideal Answer

Comparison operators compare two values and return either TRUE, FALSE, or UNKNOWN (when NULL is involved). They are primarily used in the WHERE clause to filter rows.

### Why Interviewer Asked

To verify your understanding of row-level filtering.

### Common Wrong Answer

> They compare columns.

### Follow-up Questions

* What does the WHERE clause return?
* What happens when NULL is involved?

---

## Q2. What is the difference between `!=` and `<>`?

### Ideal Answer

Both represent "Not Equal To" and behave the same in most modern databases. `<>` is the ANSI SQL standard, while `!=` is widely supported by most database engines.

### Why Interviewer Asked

To check SQL standards knowledge.

### Common Wrong Answer

> `!=` is faster.

### Follow-up Questions

* Which one would you use in production?
* Why is `<>` considered standard SQL?

---

## Q3. How does SQL evaluate multiple conditions in a WHERE clause?

### Ideal Answer

SQL evaluates the WHERE condition independently for each row. It evaluates each expression, applies the logical operators (`AND`, `OR`, `NOT`), and keeps only rows where the final result is TRUE.

### Why Interviewer Asked

To verify understanding of row-by-row evaluation.

### Common Wrong Answer

> SQL compares rows with each other.

### Follow-up Questions

* Does WHERE compare rows?
* What happens to FALSE rows?

---

## Q4. What is the operator precedence in SQL?

### Ideal Answer

SQL evaluates logical operators in the following order:

```text
NOT

↓

AND

↓

OR
```

When multiple operators are mixed, SQL follows this precedence unless parentheses are used.

### Why Interviewer Asked

This is one of the most common SQL interview topics.

### Common Wrong Answer

> SQL evaluates conditions from left to right.

### Follow-up Questions

* Would you rely on operator precedence?
* Why are parentheses recommended?

---

## Q5. Why should we use parentheses even when SQL already knows the precedence?

### Ideal Answer

Parentheses improve readability and clearly communicate the intended business logic. Although SQL evaluates the query correctly, future developers should not have to remember operator precedence to understand the query.

### Why Interviewer Asked

To assess production coding practices.

### Common Wrong Answer

> Parentheses are unnecessary because SQL already knows the order.

### Follow-up Questions

* Have you requested this change during a PR review?
* Why is readability important?

---

## Q6. Is BETWEEN inclusive or exclusive?

### Ideal Answer

BETWEEN is inclusive.

```sql
WHERE salary BETWEEN 50000 AND 100000
```

is equivalent to:

```sql
WHERE salary >= 50000
AND salary <= 100000
```

### Why Interviewer Asked

Classic SQL interview question.

### Common Wrong Answer

> BETWEEN is exclusive.

### Follow-up Questions

* Would you use BETWEEN for TIMESTAMP columns?

---

## Q7. Why should BETWEEN be avoided for TIMESTAMP ranges?

### Ideal Answer

Because the upper bound is typically interpreted as midnight (`00:00:00`). This can unintentionally exclude records later on the final day. I prefer half-open ranges using:

```sql
>= start_date
AND < next_date
```

### Why Interviewer Asked

Tests production experience.

### Common Wrong Answer

> BETWEEN always returns every record in the range.

### Follow-up Questions

* How would you filter all records for the year 2025?
* Would your answer change for DATE columns?

---

## Q8. IN vs multiple OR conditions?

### Ideal Answer

Both are logically equivalent. I prefer `IN` when checking multiple values for the same column because it is easier to read and maintain.

### Why Interviewer Asked

Tests coding style and maintainability.

### Common Wrong Answer

> IN is always faster.

### Follow-up Questions

* When would you still use OR?
* Does the optimizer treat them differently?

---

## Q9. What is the NOT IN and NULL trap?

### Ideal Answer

If the list used by `NOT IN` contains a NULL, comparisons become UNKNOWN and the query can return unexpected results, often returning no rows. I verify that NULL values are not present or use `NOT EXISTS` when appropriate.

### Why Interviewer Asked

Very common senior-level interview question.

### Common Wrong Answer

> NULL values are ignored.

### Follow-up Questions

* Why does this happen?
* What would you use instead?

---

## Q10. Explain the difference between:

```sql
LIKE 'Har%'
```

and

```sql
LIKE '%Har%'
```

### Ideal Answer

`LIKE 'Har%'` performs a prefix search and can often use an index efficiently.

`LIKE '%Har%'` searches anywhere within the string and usually prevents efficient index usage.

### Why Interviewer Asked

Tests performance knowledge.

### Common Wrong Answer

> They perform the same.

### Follow-up Questions

* Which query scales better?
* Why?

---

## Q11. What do `%` and `_` mean in LIKE?

### Ideal Answer

* `%` matches zero or more characters.
* `_` matches exactly one character.

### Why Interviewer Asked

Tests knowledge of wildcard operators.

### Common Wrong Answer

> Both represent any number of characters.

### Follow-up Questions

* Give an example using `_`.
* When would you use `%`?

---

## Q12. What is a SARGable condition?

### Ideal Answer

A SARGable condition allows the database to efficiently use an index when searching for rows. It usually follows the pattern:

```sql
column operator value
```

Example:

```sql
WHERE salary > 100000
```

### Why Interviewer Asked

Tests SQL optimization knowledge.

### Common Wrong Answer

> It means the query is optimized.

### Follow-up Questions

* Give an example of a Non-SARGable condition.
* Why does it affect index usage?

---

## Q13. Why is this query considered Non-SARGable?

```sql
WHERE employee_id + 1 = 101
```

### Ideal Answer

The database must calculate `employee_id + 1` for each row before evaluating the condition, which often prevents efficient index usage.

It is better to rewrite it as:

```sql
WHERE employee_id = 100
```

### Why Interviewer Asked

Tests understanding of query optimization.

### Common Wrong Answer

> Because addition is slow.

### Follow-up Questions

* Would the execution plan change?
* Can the index still be used?

---

# ⭐⭐⭐⭐ FREQUENTLY ASKED

---

## Q14. Should you cast columns in the WHERE clause?

**Ideal Answer**

Only when necessary. Unnecessary casts on filtered columns may prevent efficient index usage.

---

## Q15. Is this comparison valid?

```sql
WHERE salary = 100000
```

when `salary` is DECIMAL.

**Ideal Answer**

Yes.

The database performs an implicit conversion of the numeric literal when appropriate. Explicit casting is usually unnecessary.

---

## Q16. Would you choose readability or shorter SQL?

**Ideal Answer**

Readability.

SQL is read far more often than it is written. I always optimize for maintainability.

---

# ⭐⭐⭐ NICE TO KNOW

---

## Q17. Is LIKE always slow?

**Ideal Answer**

No.

Prefix searches (`LIKE 'Har%'`) are often efficient.

Leading wildcard searches (`LIKE '%Har%'`) are usually much slower on large datasets.

---

## Q18. Which is better?

```sql
WHERE NOT salary > 100000
```

or

```sql
WHERE salary <= 100000
```

**Ideal Answer**

The second version.

Both are equivalent, but the second is easier to read and understand.

---

# Final Interview Tip

Don't answer only with syntax.

Explain:

* How SQL evaluates the condition.
* Why one approach is better.
* Production implications.
* Readability and maintainability considerations.

That is what interviewers expect from a Senior Data Engineer.
