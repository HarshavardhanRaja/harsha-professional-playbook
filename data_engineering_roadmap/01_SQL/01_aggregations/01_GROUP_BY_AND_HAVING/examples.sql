```sql
-- ============================================================
-- GROUP BY & HAVING - Examples
-- Topic:
-- GROUP BY | HAVING | WHERE vs HAVING
-- ============================================================

---------------------------------------------------------------
-- Setup
---------------------------------------------------------------

CREATE TABLE employees (
    employee_id INT,
    name VARCHAR(50),
    department VARCHAR(50),
    city VARCHAR(50),
    salary INT,
    bonus INT
);

INSERT INTO employees VALUES
(1,'Harsha','IT','Hyderabad',120000,10000),
(2,'Ravi','HR','Bangalore',90000,NULL),
(3,'Priya','IT','Hyderabad',150000,5000),
(4,'Amit','Finance','Chennai',80000,NULL),
(5,'Hari','IT','Bangalore',95000,15000),
(6,'Kiran','Finance','Chennai',130000,NULL),
(7,'Sneha','HR','Hyderabad',110000,8000);

-- ============================================================
-- GROUP BY
-- ============================================================

-- Example 1
-- Count employees in each department.

SELECT
    department,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department;



-- Example 2
-- Average salary by department.

SELECT
    department,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department;



-- Example 3
-- Highest salary by department.

SELECT
    department,
    MAX(salary) AS highest_salary
FROM employees
GROUP BY department;



-- Example 4
-- Lowest salary by department.

SELECT
    department,
    MIN(salary) AS lowest_salary
FROM employees
GROUP BY department;



-- Example 5
-- Total salary paid by department.

SELECT
    department,
    SUM(salary) AS total_salary
FROM employees
GROUP BY department;



-- ============================================================
-- Multiple Aggregates
-- ============================================================

-- Example 6

SELECT
    department,
    COUNT(*) AS employee_count,
    SUM(salary) AS total_salary,
    AVG(salary) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary
FROM employees
GROUP BY department;



-- ============================================================
-- GROUP BY Multiple Columns
-- ============================================================

-- Example 7
-- Count employees by department and city.

SELECT
    department,
    city,
    COUNT(*) AS employee_count
FROM employees
GROUP BY
    department,
    city;



-- ============================================================
-- WHERE + GROUP BY
-- ============================================================

-- Example 8
-- Average salary of employees earning
-- more than 100000.

SELECT
    department,
    AVG(salary) AS avg_salary
FROM employees
WHERE salary > 100000
GROUP BY department;



-- ============================================================
-- HAVING
-- ============================================================

-- Example 9
-- Departments having more than
-- 2 employees.

SELECT
    department,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 2;



-- Example 10
-- Departments whose average salary
-- is greater than 100000.

SELECT
    department,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 100000;



-- ============================================================
-- WHERE + HAVING Together
-- ============================================================

-- Example 11

SELECT
    department,
    AVG(salary) AS avg_salary
FROM employees
WHERE salary > 50000
GROUP BY department
HAVING AVG(salary) > 100000;



-- ============================================================
-- Invalid Queries
-- ============================================================

-- Example 12
-- Invalid

SELECT
    department,
    salary
FROM employees
GROUP BY department;

-- Discussion:
-- salary is neither grouped
-- nor aggregated.



-- Example 13
-- Invalid

SELECT
    department,
    COUNT(*)
FROM employees
WHERE COUNT(*) > 2
GROUP BY department;

-- Discussion:
-- Aggregate functions do not exist
-- during WHERE execution.



-- ============================================================
-- Mini Exercises
-- ============================================================

-- Exercise 1
-- Count employees in each department.

-- Your Query:



---------------------------------------------------------------

-- Exercise 2
-- Calculate average salary
-- for each department.

-- Your Query:



---------------------------------------------------------------

-- Exercise 3
-- Find the highest salary
-- in each department.

-- Your Query:



---------------------------------------------------------------

-- Exercise 4
-- Find the total salary
-- paid by each department.

-- Your Query:



---------------------------------------------------------------

-- Exercise 5
-- Count employees by
-- department and city.

-- Your Query:



---------------------------------------------------------------

-- Exercise 6
-- Show departments having
-- more than 1 employee.

-- Your Query:



---------------------------------------------------------------

-- Exercise 7
-- Show departments whose
-- average salary is greater
-- than 100000.

-- Your Query:



---------------------------------------------------------------

-- Exercise 8
-- Among employees earning
-- more than 90000,
-- show departments having
-- an average salary greater
-- than 120000.

-- Your Query:



---------------------------------------------------------------

-- Exercise 9
-- Why is the following query invalid?

SELECT
    department,
    name
FROM employees
GROUP BY department;

-- Explain your answer.



---------------------------------------------------------------

-- Exercise 10
-- Explain why this query works.

SELECT
    department,
    COUNT(*),
    AVG(salary),
    MAX(salary)
FROM employees
GROUP BY department;

-- Explain your reasoning.



-- ============================================================
-- End of Topic 6
-- ============================================================
```
