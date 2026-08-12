-- ============================================================
-- NULL Handling & CASE - Examples
-- Topic:
-- NULL | IS NULL | COALESCE | Aggregate Functions
-- CASE | Conditional Aggregation
-- ============================================================

---

## -- Setup

CREATE TABLE employees (
employee_id INT,
name VARCHAR(50),
department VARCHAR(50),
salary INT,
bonus INT
);

INSERT INTO employees VALUES
(1,'Harsha','IT',120000,10000),
(2,'Ravi','HR',90000,NULL),
(3,'Priya','IT',150000,5000),
(4,'Amit','Finance',80000,NULL),
(5,'Hari','IT',95000,15000),
(6,'Kiran','Finance',130000,NULL);

-- ============================================================
-- IS NULL / IS NOT NULL
-- ============================================================

-- Example 1
-- Employees whose bonus is missing.

SELECT *
FROM employees
WHERE bonus IS NULL;

-- Example 2
-- Employees whose bonus exists.

SELECT *
FROM employees
WHERE bonus IS NOT NULL;

-- ============================================================
-- Incorrect NULL Comparison
-- ============================================================

-- Example 3
-- Incorrect

SELECT *
FROM employees
WHERE bonus = NULL;

-- Discussion:
-- Returns no rows.
-- Always use IS NULL.

-- Example 4
-- Incorrect

SELECT *
FROM employees
WHERE bonus <> NULL;

-- Discussion:
-- Returns no rows.
-- Use IS NOT NULL.

-- ============================================================
-- COALESCE
-- ============================================================

-- Example 5
-- Replace NULL bonus with zero.

SELECT
employee_id,
name,
bonus,
COALESCE(bonus,0) AS bonus_after_coalesce
FROM employees;

-- Example 6
-- Use COALESCE in calculations.

SELECT
employee_id,
salary,
bonus,
salary + COALESCE(bonus,0) AS total_compensation
FROM employees;

-- Example 7
-- Multiple arguments.

SELECT
COALESCE(NULL,NULL,NULL,100,200);

-- ============================================================
-- Aggregate Functions
-- ============================================================

-- Example 8

SELECT
COUNT(*) AS total_rows
FROM employees;

-- Example 9

SELECT
COUNT(bonus) AS employees_with_bonus
FROM employees;

-- Example 10

SELECT
SUM(bonus),
AVG(bonus),
MIN(bonus),
MAX(bonus)
FROM employees;

-- ============================================================
-- CASE Expression
-- ============================================================

-- Example 11

SELECT
employee_id,
salary,
CASE
WHEN salary >=150000 THEN 'Excellent'
WHEN salary >=100000 THEN 'High'
WHEN salary >=50000 THEN 'Medium'
ELSE 'Low'
END AS salary_band
FROM employees;

-- Example 12
-- CASE without ELSE

SELECT
CASE
WHEN salary>=100000 THEN 'High'
END
FROM employees;

-- Discussion:
-- Employees earning less than 100000
-- receive NULL.

-- ============================================================
-- CASE in ORDER BY
-- ============================================================

-- Example 13

SELECT *
FROM employees
ORDER BY
CASE
WHEN department='IT' THEN 1
WHEN department='Finance' THEN 2
ELSE 3
END;

-- ============================================================
-- Conditional Aggregation
-- ============================================================

-- Example 14

SELECT
department,
COUNT(*) AS total_employees,
SUM(
CASE
WHEN salary>=100000 THEN 1
ELSE 0
END
) AS high_salary_count
FROM employees
GROUP BY department;

-- Example 15

SELECT
department,
SUM(
CASE
WHEN bonus IS NULL THEN 1
ELSE 0
END
) AS employees_without_bonus
FROM employees
GROUP BY department;

-- ============================================================
-- Mini Exercises
-- ============================================================

-- Exercise 1
-- Retrieve employees whose bonus is NULL.

-- Your Query:

---

-- Exercise 2
-- Retrieve employees whose bonus is NOT NULL.

-- Your Query:

---

-- Exercise 3
-- Replace NULL bonus values with zero.

-- Your Query:

---

-- Exercise 4
-- Calculate total compensation
-- (salary + bonus),
-- treating NULL bonus as zero.

-- Your Query:

---

-- Exercise 5
-- Categorize employees into:

-- Excellent (>=150000)
-- High (>=100000)
-- Medium (>=50000)
-- Low (<50000)

-- Your Query:

---

-- Exercise 6
-- Count employees with a bonus.

-- Your Query:

---

-- Exercise 7
-- Show department-wise:

-- Total Employees

-- Employees earning >=100000

-- Your Query:

---

-- Exercise 8
-- Show department-wise employees
-- whose bonus is NULL.

-- Your Query:

---

-- Exercise 9
-- Sort departments in this order:

-- IT
-- Finance
-- HR
-- Others

-- Your Query:

---

-- Exercise 10
-- Replace NULL average bonus with zero.

-- Hint:
-- Use COALESCE with AVG().

-- Your Query:

-- ============================================================
-- End of Topic 4
-- ============================================================
