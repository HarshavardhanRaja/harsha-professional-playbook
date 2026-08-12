# NULL Handling & CASE - Interview Questions

---

# ⭐⭐⭐⭐⭐ MUST KNOW

---

## Q1. What is NULL in SQL?

### Ideal Answer

NULL represents an unknown or missing value. It is not zero, an empty string, or FALSE. It simply indicates that the value is currently unavailable or unknown.

### Why Interviewer Asked

To verify understanding of one of SQL's core concepts.

### Common Wrong Answer

> NULL means zero.

### Follow-up Questions

* Is NULL the same as an empty string?
* Can NULL participate in arithmetic operations?

---

## Q2. Why doesn't `WHERE column = NULL` work?

### Ideal Answer

Comparisons with NULL return UNKNOWN, not TRUE or FALSE. Since the WHERE clause only keeps rows where the condition evaluates to TRUE, `column = NULL` never returns any rows. SQL provides `IS NULL` and `IS NOT NULL` for NULL checks.

### Why Interviewer Asked

Classic SQL interview question.

### Common Wrong Answer

> It throws an error.

### Follow-up Questions

* Why does SQL return UNKNOWN?
* What should be used instead?

---

## Q3. Explain SQL's Three-Valued Logic.

### Ideal Answer

Unlike most programming languages, SQL has three logical values:

```text id="rb10t6"
TRUE

FALSE

UNKNOWN
```

Comparisons involving NULL usually return UNKNOWN. The WHERE clause only keeps rows where the result is TRUE.

### Why Interviewer Asked

Tests deep understanding of NULL behavior.

### Common Wrong Answer

> SQL only has TRUE and FALSE.

### Follow-up Questions

* How does WHERE treat UNKNOWN?
* Why does `NULL = NULL` return UNKNOWN?

---

## Q4. What is the difference between `IS NULL` and `= NULL`?

### Ideal Answer

`IS NULL` checks whether a value is NULL.

`= NULL` performs a comparison, which evaluates to UNKNOWN.

Always use `IS NULL` or `IS NOT NULL` when checking for NULL values.

### Why Interviewer Asked

Very common SQL interview question.

### Common Wrong Answer

> They are equivalent.

### Follow-up Questions

* Does `<> NULL` work?
* What does it return?

---

## Q5. What is COALESCE?

### Ideal Answer

`COALESCE()` returns the first non-NULL value from the list of expressions.

Example:

```sql id="h9r1mj"
COALESCE(bonus, 0)
```

It is commonly used to replace NULL values in reports and calculations.

### Why Interviewer Asked

Tests practical SQL knowledge.

### Common Wrong Answer

> COALESCE converts NULL into zero.

(It can return any default value, not just zero.)

### Follow-up Questions

* When do you use COALESCE?
* Can COALESCE accept multiple arguments?

---

## Q6. Why is COALESCE commonly used in calculations?

### Ideal Answer

Arithmetic operations involving NULL return NULL.

Using COALESCE replaces NULL with a default value before the calculation.

Example:

```sql id="f1vz4w"
salary + COALESCE(bonus, 0)
```

### Why Interviewer Asked

Tests production experience.

### Common Wrong Answer

> SQL automatically treats NULL as zero.

### Follow-up Questions

* What happens without COALESCE?
* Give a reporting example.

---

## Q7. What is the difference between `COUNT(*)` and `COUNT(column)`?

### Ideal Answer

`COUNT(*)` counts every row.

`COUNT(column)` counts only rows where the specified column is not NULL.

### Why Interviewer Asked

One of the most common SQL interview questions.

### Common Wrong Answer

> Both always return the same result.

### Follow-up Questions

* What happens if every value is NULL?
* Which one would you use to count employees who received a bonus?

---

## Q8. How do aggregate functions handle NULL values?

### Ideal Answer

`SUM`, `AVG`, `MIN`, and `MAX` ignore NULL values.

If every value is NULL:

* SUM returns NULL
* AVG returns NULL
* MIN returns NULL
* MAX returns NULL

### Why Interviewer Asked

Tests understanding of aggregate behavior.

### Common Wrong Answer

> Aggregates treat NULL as zero.

### Follow-up Questions

* Why does AVG not divide by all rows?
* How does COUNT behave differently?

---

## Q9. What is CASE?

### Ideal Answer

CASE is SQL's conditional expression that works like an IF-ELSE statement. It allows SQL to return different values based on specified conditions.

### Why Interviewer Asked

Tests knowledge of SQL conditional logic.

### Common Wrong Answer

> CASE is a loop.

### Follow-up Questions

* Where can CASE be used?
* Does CASE stop after the first match?

---

## Q10. Does the order of CASE conditions matter?

### Ideal Answer

Yes.

CASE evaluates conditions from top to bottom and stops at the first matching condition.

Therefore overlapping conditions should be ordered from most specific to least specific.

### Why Interviewer Asked

Very common interview trap.

### Common Wrong Answer

> SQL evaluates all WHEN clauses.

### Follow-up Questions

* What happens if the conditions are reversed?
* Why is condition order important?

---

## Q11. What happens if ELSE is omitted in CASE?

### Ideal Answer

If no condition matches and ELSE is omitted, SQL returns NULL.

### Why Interviewer Asked

Tests understanding of CASE behavior.

### Common Wrong Answer

> CASE throws an error.

### Follow-up Questions

* Would this affect reports?
* When should ELSE be included?

---

## Q12. Explain Conditional Aggregation.

### Ideal Answer

Conditional aggregation combines CASE with aggregate functions.

Example:

```sql id="jwr3c6"
SUM(
    CASE
        WHEN salary >= 100000 THEN 1
        ELSE 0
    END
)
```

This pattern counts only rows satisfying a condition while preserving all grouped rows.

### Why Interviewer Asked

One of the most common production SQL patterns.

### Common Wrong Answer

> Use WHERE before GROUP BY.

### Follow-up Questions

* Why not use WHERE?
* Why is ELSE 0 important?

---

## Q13. Why do we use ELSE 0 in conditional aggregation?

### Ideal Answer

Without ELSE 0, CASE returns NULL for non-matching rows.

If every row in a group returns NULL, SUM also returns NULL.

Using ELSE 0 ensures the aggregation returns 0 instead of NULL.

### Why Interviewer Asked

Tests production SQL experience.

### Common Wrong Answer

> ELSE 0 is optional.

### Follow-up Questions

* What happens when all rows fail the condition?
* Why is NULL undesirable in dashboards?

---

# ⭐⭐⭐⭐ FREQUENTLY ASKED

---

## Q14. Can COALESCE take more than two arguments?

### Ideal Answer

Yes.

It returns the first non-NULL value from the list.

Example:

```sql id="frnvyw"
COALESCE(NULL, NULL, 'Unknown')
```

Returns:

```text id="sj8p0n"
Unknown
```

---

## Q15. Where have you used CASE in production?

### Ideal Answer

Common use cases include:

* Categorizing customers
* Salary bands
* KPI dashboards
* Conditional counts
* Report labels
* Business rules

---

## Q16. Would you use CASE or COALESCE to replace NULL values?

### Ideal Answer

COALESCE.

CASE can do it, but COALESCE is shorter, cleaner, and specifically designed for replacing NULL values.

---

# ⭐⭐⭐ NICE TO KNOW

---

## Q17. Why does `NOT IN` fail when the list contains NULL?

### Ideal Answer

Comparisons with NULL return UNKNOWN.

Since WHERE only keeps TRUE, the overall condition becomes UNKNOWN and rows are discarded.

### Follow-up Questions

* What alternative would you consider?
* How does three-valued logic explain this behavior?

---

## Q18. Which is better?

```sql id="glsg1i"
CASE
WHEN bonus IS NULL THEN 0
ELSE bonus
END
```

or

```sql id="9vq69j"
COALESCE(bonus, 0)
```

### Ideal Answer

Both are correct.

I prefer COALESCE because it is shorter, more readable, and designed specifically for handling NULL values.

---

# Final Interview Tip

Don't just explain the syntax.

Interviewers expect you to explain:

* Why SQL behaves that way.
* The production impact.
* Common mistakes.
* Better alternatives.
* Readability and maintainability considerations.

That's what differentiates a Senior Data Engineer from someone who only knows SQL syntax.
