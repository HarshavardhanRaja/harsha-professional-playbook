# GROUP BY & HAVING - Interview Questions

---

# ⭐⭐⭐⭐⭐ MUST KNOW

---

## Q1. What is GROUP BY?

### Ideal Answer

`GROUP BY` groups rows having the same values in one or more columns and allows aggregate functions to run independently for each group.

It returns **one row per group**.

### Why Interviewer Asked

Tests understanding of one of SQL's core concepts.

### Common Wrong Answer

> GROUP BY removes duplicate rows.

### Follow-up Questions

* Why do we need GROUP BY?
* What happens without GROUP BY?

---

## Q2. How does GROUP BY work internally?

### Ideal Answer

Conceptually SQL performs these steps:

```text
One Big Table

↓

Identify Unique Groups

↓

Split Rows Into Buckets

↓

Run Aggregate Function
On Each Bucket

↓

Return One Row Per Group
```

### Why Interviewer Asked

Tests conceptual understanding rather than syntax.

### Common Wrong Answer

> GROUP BY simply sorts the data.

### Follow-up Questions

* Does SQL actually create buckets?
* Does GROUP BY always sort the data?

---

## Q3. Why does this query fail?

```sql
SELECT
    department,
    salary
FROM employees
GROUP BY department;
```

### Ideal Answer

After grouping, SQL returns one row per department.

`salary` has multiple values within each department.

Since `salary` is neither grouped nor aggregated, SQL cannot determine which value to return.

### Why Interviewer Asked

One of the most common SQL interview questions.

### Common Wrong Answer

> GROUP BY requires aggregate functions.

### Follow-up Questions

* How can you fix the query?
* Which aggregate function would you use?

---

## Q4. What is the golden rule of GROUP BY?

### Ideal Answer

After `GROUP BY`, every selected column must satisfy one of these conditions:

* It must appear in the `GROUP BY`.
* It must be wrapped inside an aggregate function.

This ensures every group produces exactly one value for every selected column.

### Why Interviewer Asked

Tests deep understanding of grouped queries.

### Common Wrong Answer

> Every column must be in the GROUP BY.

### Follow-up Questions

* Why are aggregate functions allowed?
* What problem does this rule solve?

---

## Q5. Why does this query work?

```sql
SELECT
    department,
    MAX(salary)
FROM employees
GROUP BY department;
```

### Ideal Answer

`department` identifies each group.

`MAX(salary)` reduces multiple salary values into a single value for each group.

Therefore, every selected column produces exactly one value per group.

### Why Interviewer Asked

Tests understanding of aggregation.

### Common Wrong Answer

> Because MAX is an aggregate function.

### Follow-up Questions

* Would AVG() also work?
* Would salary work?

---

## Q6. What is HAVING?

### Ideal Answer

`HAVING` filters groups after aggregation.

Unlike `WHERE`, it operates on grouped results and aggregate values.

### Why Interviewer Asked

Tests understanding of SQL execution order.

### Common Wrong Answer

> HAVING is another form of WHERE.

### Follow-up Questions

* Why can't WHERE do the same?
* When would you use HAVING?

---

## Q7. What is the difference between WHERE and HAVING?

### Ideal Answer

| WHERE                 | HAVING             |
| --------------------- | ------------------ |
| Filters rows          | Filters groups     |
| Before GROUP BY       | After GROUP BY     |
| Cannot use aggregates | Can use aggregates |

### Why Interviewer Asked

One of the most frequently asked SQL interview questions.

### Common Wrong Answer

> HAVING is used only with GROUP BY.

### Follow-up Questions

* Can HAVING be used without GROUP BY?
* Which executes first?

---

## Q8. Why can't aggregate functions be used in WHERE?

### Ideal Answer

`WHERE` executes before `GROUP BY`.

Aggregate functions are calculated after grouping.

Therefore, aggregate values do not exist during the WHERE phase.

### Why Interviewer Asked

Tests execution order understanding.

### Common Wrong Answer

> SQL syntax doesn't allow it.

### Follow-up Questions

* Which clause should be used instead?
* Explain the execution order.

---

# ⭐⭐⭐⭐ FREQUENTLY ASKED

---

## Q9. Explain the execution order of a grouped query.

### Ideal Answer

```text
FROM

↓

WHERE

↓

GROUP BY

↓

Aggregate Functions

↓

HAVING

↓

SELECT

↓

ORDER BY

↓

LIMIT
```

### Why Interviewer Asked

Tests logical query processing.

---

## Q10. Why should row-level filters use WHERE instead of HAVING?

### Ideal Answer

`WHERE` removes unnecessary rows before grouping.

This reduces the amount of data SQL needs to group and aggregate, making the query more efficient.

### Why Interviewer Asked

Tests performance awareness.

### Common Wrong Answer

> WHERE and HAVING have the same performance.

---

## Q11. Can GROUP BY have multiple columns?

### Ideal Answer

Yes.

Example:

```sql
SELECT
    department,
    city,
    COUNT(*)
FROM employees
GROUP BY
    department,
    city;
```

SQL creates one group for every unique `(department, city)` combination.

---

## Q12. Can aggregate functions be used without GROUP BY?

### Ideal Answer

Yes.

Without GROUP BY, the entire result set is treated as a single group.

Example:

```sql
SELECT
    COUNT(*)
FROM employees;
```

Returns one aggregated result for the whole table.

---

# ⭐⭐⭐ NICE TO KNOW

---

## Q13. Can HAVING be used without GROUP BY?

### Ideal Answer

Yes.

If there is no `GROUP BY`, SQL treats the entire result set as one group.

Example:

```sql
SELECT
    COUNT(*)
FROM employees
HAVING COUNT(*) > 0;
```

Although valid, this is much less common than using HAVING with GROUP BY.

---

## Q14. Where have you used GROUP BY in production?

### Ideal Answer

Examples include:

* KPI dashboards
* Sales reports
* Department-wise summaries
* Customer analytics
* Daily metrics
* Monitoring and alerting
* Financial reporting

---

## Q15. Which is generally more efficient: WHERE or HAVING?

### Ideal Answer

If the condition is row-level, `WHERE` is more efficient because it filters rows before grouping.

`HAVING` should only be used when filtering aggregated results.

---

# Final Interview Tip

Whenever you see a `GROUP BY` question, ask yourself:

1. What are the groups?
2. Does every selected column produce exactly one value per group?
3. Is this a row-level filter (`WHERE`) or a group-level filter (`HAVING`)?
4. At what stage of SQL execution does this condition become available?

Answering these four questions correctly will solve the majority of GROUP BY interview problems.
