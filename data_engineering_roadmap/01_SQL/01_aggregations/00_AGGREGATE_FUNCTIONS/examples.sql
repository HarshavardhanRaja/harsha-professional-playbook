```sql
-- ============================================================
-- Aggregate Functions - Examples
-- Topic:
-- COUNT | SUM | AVG | MIN | MAX | COUNT(DISTINCT)
-- ============================================================

---------------------------------------------------------------
-- Setup
---------------------------------------------------------------

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
-- COUNT()
-- ============================================================

-- Example 1
-- Count total employees.

SELECT
    COUNT(*)
FROM employees;



-- Example 2
-- Count employees who have received a bonus.

SELECT
    COUNT(bonus)
FROM employees;



-- Example 3
-- Count unique departments.

SELECT
    COUNT(DISTINCT department)
FROM employees;



-- ============================================================
-- SUM()
-- ============================================================

-- Example 4
-- Calculate total salary.

SELECT
    SUM(salary)
FROM employees;



-- Example 5
-- Calculate total bonus paid.

SELECT
    SUM(bonus)
FROM employees;



-- ============================================================
-- AVG()
-- ============================================================

-- Example 6
-- Average salary.

SELECT
    AVG(salary)
FROM employees;



-- Example 7
-- Average bonus.

SELECT
    AVG(bonus)
FROM employees;



-- Example 8
-- Manual average calculation.

SELECT
    SUM(salary) / COUNT(salary) AS average_salary
FROM employees;

-- Discussion:
-- AVG(salary) is preferred.
-- It is cleaner and avoids common mistakes.



-- ============================================================
-- MIN()
-- ============================================================

-- Example 9
-- Lowest salary.

SELECT
    MIN(salary)
FROM employees;



-- ============================================================
-- MAX()
-- ============================================================

-- Example 10
-- Highest salary.

SELECT
    MAX(salary)
FROM employees;



-- ============================================================
-- Multiple Aggregate Functions
-- ============================================================

-- Example 11

SELECT
    COUNT(*) AS total_employees,
    COUNT(bonus) AS employees_with_bonus,
    SUM(salary) AS total_salary,
    AVG(salary) AS average_salary,
    MIN(salary) AS minimum_salary,
    MAX(salary) AS maximum_salary
FROM employees;



-- ============================================================
-- NULL Handling
-- ============================================================

-- Example 12
-- Observe the difference between
-- COUNT(*) and COUNT(column).

SELECT
    COUNT(*) AS total_rows,
    COUNT(bonus) AS bonus_count
FROM employees;



-- Example 13
-- Observe how SUM ignores NULL.

SELECT
    SUM(bonus)
FROM employees;



-- Example 14
-- Observe how AVG ignores NULL.

SELECT
    AVG(bonus)
FROM employees;



-- ============================================================
-- COUNT(DISTINCT)
-- ============================================================

-- Example 15
-- Count unique departments.

SELECT
    COUNT(DISTINCT department)
FROM employees;



-- ============================================================
-- Mini Exercises
-- ============================================================

-- Exercise 1
-- Count total employees.

-- Your Query:



---------------------------------------------------------------

-- Exercise 2
-- Count employees whose bonus is not NULL.

-- Your Query:



---------------------------------------------------------------

-- Exercise 3
-- Count unique departments.

-- Your Query:



---------------------------------------------------------------

-- Exercise 4
-- Calculate the total salary.

-- Your Query:



---------------------------------------------------------------

-- Exercise 5
-- Calculate the average salary.

-- Your Query:



---------------------------------------------------------------

-- Exercise 6
-- Find the minimum salary.

-- Your Query:



---------------------------------------------------------------

-- Exercise 7
-- Find the maximum salary.

-- Your Query:



---------------------------------------------------------------

-- Exercise 8
-- Display all aggregate functions in a single query.

-- Your Query:



---------------------------------------------------------------

-- Exercise 9
-- Compare COUNT(*) and COUNT(bonus).

-- Your Query:



---------------------------------------------------------------

-- Exercise 10
-- Calculate the average bonus manually using
-- SUM() and COUNT().

-- Your Query:



---------------------------------------------------------------

-- Exercise 11
-- Count unique employee names.

-- Your Query:



---------------------------------------------------------------

-- Exercise 12
-- Review the following query.

SELECT
    SUM(salary) / COUNT(*)
FROM employees;

-- Question:
-- Would you approve this query?
-- If not, explain why and write the preferred solution.



-- ============================================================
-- End of Topic 5
-- ============================================================
```
