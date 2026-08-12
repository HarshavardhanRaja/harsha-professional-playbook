# SQL Execution Order - Interview Questions

---

# 🔥 MUST KNOW QUESTIONS

> If you cannot answer these, your SQL fundamentals are weak.

================================================================================

## 🔥 Q1. What Is SQL Execution Order?

Answer:

FROM
→ JOIN
→ WHERE
→ GROUP BY
→ HAVING
→ SELECT
→ DISTINCT
→ ORDER BY
→ LIMIT

Common Mistake:

❌ Giving the written query order instead of execution order.

--------------------------------------------------------------------------------

## 🔥 Q2. Difference Between WHERE And HAVING?

Answer:

WHERE filters rows.

HAVING filters groups.

Example:

SELECT department,
       COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 10;

Common Mistake:

❌ Using COUNT(*) inside WHERE.

--------------------------------------------------------------------------------

## 🔥 Q3. Why Can't COUNT(*) Be Used In WHERE?

Answer:

WHERE executes before GROUP BY.

COUNT(*) is calculated after GROUP BY.

Therefore COUNT(*) is not available when WHERE executes.

Common Mistake:

❌ Thinking COUNT(*) is created during SELECT.

--------------------------------------------------------------------------------

## 🔥 Q4. Why Doesn't Alias Work In WHERE?

Answer:

Aliases are created during SELECT.

WHERE executes before SELECT.

Example:

SELECT salary AS sal
FROM employees
WHERE sal > 100000;

This fails because sal does not exist yet.

Common Mistake:

❌ Assuming aliases are available everywhere.

--------------------------------------------------------------------------------

## 🔥 Q5. Why Does Alias Work In ORDER BY?

Answer:

ORDER BY executes after SELECT.

The alias already exists.

Example:

SELECT salary AS sal
FROM employees
ORDER BY sal DESC;

================================================================================



# ⭐ FREQUENTLY ASKED QUESTIONS

> Common follow-up questions asked in many SQL interviews.

================================================================================

## ⭐ Q6. Explain The Execution Of This Query Step By Step

Query:

SELECT department,
       COUNT(*) cnt
FROM employees
WHERE salary > 50000
GROUP BY department
HAVING COUNT(*) > 5
ORDER BY cnt DESC;

Answer:

Step 1:
FROM employees

Step 2:
WHERE salary > 50000

Step 3:
GROUP BY department

Step 4:
COUNT(*) calculated

Step 5:
HAVING COUNT(*) > 5

Step 6:
SELECT department, cnt

Step 7:
ORDER BY cnt DESC

--------------------------------------------------------------------------------

## ⭐ Q7. Which Executes First: WHERE Or GROUP BY?

Answer:

WHERE executes first.

Reason:

Rows must be filtered before they can be grouped.

--------------------------------------------------------------------------------

## ⭐ Q8. Which Executes First: GROUP BY Or HAVING?

Answer:

GROUP BY executes first.

Reason:

HAVING filters groups, therefore groups must already exist.

--------------------------------------------------------------------------------

## ⭐ Q9. Can Aggregate Functions Be Used In HAVING?

Answer:

Yes.

Example:

SELECT department,
       COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 10;

================================================================================



# 🚀 SENIOR DATA ENGINEER QUESTIONS

> Common in Senior / Lead / Staff Data Engineer interviews.

================================================================================

## 🚀 Q10. Logical Execution Order vs Physical Execution Order

Answer:

Logical execution order is the conceptual SQL order:

FROM
→ WHERE
→ GROUP BY
→ HAVING
→ SELECT

Physical execution order is determined by the optimizer and may differ internally.

--------------------------------------------------------------------------------

## 🚀 Q11. Why Do Window Functions Fail In WHERE?

Answer:

Window functions are calculated after WHERE.

Example:

SELECT *,
       ROW_NUMBER() OVER()
FROM employees
WHERE ROW_NUMBER() OVER() = 1;

This fails.

Use:

- CTE
- Subquery
- QUALIFY

instead.

--------------------------------------------------------------------------------

## 🚀 Q12. Why Was QUALIFY Introduced?

Answer:

QUALIFY allows filtering window function results.

Example:

SELECT *
FROM employees
QUALIFY ROW_NUMBER() OVER(
            PARTITION BY department
            ORDER BY salary DESC
       ) = 1;

--------------------------------------------------------------------------------

## 🚀 Q13. How Does SQL Execution Order Help Query Optimization?

Answer:

Understanding execution order helps push filters earlier.

Less data processed
→ Faster joins
→ Faster aggregations
→ Better performance

================================================================================



# 🎁 BONUS QUESTIONS

> Rarely asked but useful to know.

================================================================================

## 🎁 Q14. Can HAVING Be Used Without GROUP BY?

Answer:

Yes.

The entire result set becomes one group.

Example:

SELECT COUNT(*)
FROM employees
HAVING COUNT(*) > 100;

--------------------------------------------------------------------------------

## 🎁 Q15. Can GROUP BY Use Aliases?

Answer:

Depends on the database.

Some databases allow aliases.

Others require the original column name.

--------------------------------------------------------------------------------

## 🎁 Q16. Can ORDER BY Use Column Position Numbers?

Answer:

Yes.

Example:

SELECT department,
       COUNT(*)
FROM employees
GROUP BY department
ORDER BY 2 DESC;

--------------------------------------------------------------------------------

## 🎁 Q17. What Happens Internally When SQL Executes A Query?

Answer:

Parser
→ Optimizer
→ Execution Plan
→ Execution Engine
→ Result

================================================================================