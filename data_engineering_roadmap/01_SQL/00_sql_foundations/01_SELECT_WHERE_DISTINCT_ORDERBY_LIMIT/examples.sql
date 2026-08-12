-- ============================================================
-- SQL Query Basics - Examples
-- Topic:
-- SELECT | WHERE | DISTINCT | ORDER BY | LIMIT
-- ============================================================

---

## -- Setup

CREATE TABLE employees (
employee_id INT,
name VARCHAR(50),
department VARCHAR(50),
salary INT,
joining_date DATE
);

INSERT INTO employees VALUES
(1, 'Harsha', 'IT', 120000, '2021-01-10'),
(2, 'Ravi', 'HR', 90000, '2020-08-15'),
(3, 'Priya', 'IT', 150000, '2019-06-20'),
(4, 'Amit', 'Finance', 110000, '2022-03-18'),
(5, 'Kiran', 'HR', 95000, '2023-05-12'),
(6, 'Sneha', 'Finance', 130000, '2018-09-25');

-- ============================================================
-- SELECT
-- ============================================================

-- Example 1
-- Retrieve only required columns.

SELECT employee_id,
name
FROM employees;

-- Expected Output
-- employee_id | name

-- Example 2
-- Avoid SELECT * in production.

SELECT *
FROM employees;

-- Discussion:
-- Good for quick exploration.
-- Avoid in production due to:
-- - unnecessary columns
-- - schema coupling
-- - security concerns
-- - increased cloud cost

-- ============================================================
-- WHERE
-- ============================================================

-- Example 3
-- Filter rows.

SELECT name,
salary
FROM employees
WHERE salary > 100000;

-- Expected Output
-- Harsha
-- Priya
-- Amit
-- Sneha

-- Example 4
-- Multiple conditions.

SELECT *
FROM employees
WHERE department = 'IT'
AND salary > 100000;

-- Example 5
-- Avoid functions on filtered columns.

-- Avoid

SELECT *
FROM employees
WHERE YEAR(joining_date) = 2021;

-- Prefer

SELECT *
FROM employees
WHERE joining_date >= '2021-01-01'
AND joining_date < '2022-01-01';

-- ============================================================
-- DISTINCT
-- ============================================================

-- Example 6
-- Unique departments.

SELECT DISTINCT department
FROM employees;

-- Example 7
-- Same result using GROUP BY.

SELECT department
FROM employees
GROUP BY department;

-- Discussion:
-- Prefer DISTINCT when only uniqueness is required.

-- ============================================================
-- ORDER BY
-- ============================================================

-- Example 8
-- Ascending order.

SELECT name,
salary
FROM employees
ORDER BY salary;

-- Example 9
-- Descending order.

SELECT name,
salary
FROM employees
ORDER BY salary DESC;

-- Example 10
-- Multiple sorting columns.

SELECT department,
name,
salary
FROM employees
ORDER BY department,
salary DESC;

-- Discussion:
-- department -> Primary Sort Key
-- salary -> Secondary Sort Key

-- ============================================================
-- LIMIT
-- ============================================================

-- Example 11
-- Top 3 highest-paid employees.

SELECT name,
salary
FROM employees
ORDER BY salary DESC
LIMIT 3;

-- Example 12
-- LIMIT without ORDER BY.

SELECT *
FROM employees
LIMIT 3;

-- Discussion:
-- Result is non-deterministic.
-- Never rely on this in production.

-- ============================================================
-- OFFSET
-- ============================================================

-- Example 13
-- Pagination.

SELECT *
FROM employees
ORDER BY employee_id
LIMIT 2 OFFSET 2;

-- Meaning:
-- Skip first 2 rows.
-- Return next 2 rows.

-- ============================================================
-- Cursor Pagination
-- ============================================================

-- Example 14
-- Better than OFFSET for large datasets.

SELECT *
FROM employees
WHERE employee_id > 2
ORDER BY employee_id
LIMIT 2;

-- Discussion:
-- Efficient for large tables.
-- Commonly used in APIs.

-- ============================================================
-- Mini Exercises
-- ============================================================

-- Exercise 1
-- Retrieve employee name and department only.

-- Your Query:

---

-- Exercise 2
-- Retrieve employees earning more than 100000.

-- Your Query:

---

-- Exercise 3
-- Display unique departments.

-- Your Query:

---

-- Exercise 4
-- Display employees sorted by salary (highest first).

-- Your Query:

---

-- Exercise 5
-- Retrieve the latest three joined employees.

-- Your Query:

---

-- Exercise 6
-- Retrieve the second page of employees assuming
-- page size is 2.

-- Your Query:

-- ============================================================
-- End of Topic 2
-- ============================================================
