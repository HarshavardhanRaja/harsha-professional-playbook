```sql
-- ============================================================
-- Conditional Aggregation - Examples
-- Topic:
-- SUM(CASE) | COUNT(CASE) | Dashboard KPIs
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
-- Basic Conditional Count
-- ============================================================

-- Example 1
-- Count employees earning more than 100000.

SELECT
    SUM(
        CASE
            WHEN salary > 100000 THEN 1
            ELSE 0
        END
    ) AS high_salary_count
FROM employees;



-- Example 2
-- Count employees earning 100000 or less.

SELECT
    SUM(
        CASE
            WHEN salary <= 100000 THEN 1
            ELSE 0
        END
    ) AS normal_salary_count
FROM employees;



-- ============================================================
-- Multiple KPIs In One Query
-- ============================================================

-- Example 3

SELECT
    COUNT(*) AS total_employees,

    SUM(
        CASE
            WHEN salary > 100000 THEN 1
            ELSE 0
        END
    ) AS high_salary,

    SUM(
        CASE
            WHEN salary <= 100000 THEN 1
            ELSE 0
        END
    ) AS normal_salary

FROM employees;



-- ============================================================
-- Conditional Sum
-- ============================================================

-- Example 4
-- Total bonus for employees
-- earning more than 100000.

SELECT
    SUM(
        CASE
            WHEN salary > 100000
            THEN bonus
            ELSE 0
        END
    ) AS high_salary_bonus
FROM employees;



-- ============================================================
-- GROUP BY + Conditional Aggregation
-- ============================================================

-- Example 5

SELECT
    department,

    COUNT(*) AS total_employees,

    SUM(
        CASE
            WHEN salary > 100000 THEN 1
            ELSE 0
        END
    ) AS high_salary,

    SUM(
        CASE
            WHEN salary <= 100000 THEN 1
            ELSE 0
        END
    ) AS normal_salary

FROM employees
GROUP BY department;



-- Example 6
-- Department-wise bonus
-- for high salary employees.

SELECT
    department,

    SUM(
        CASE
            WHEN salary > 100000
            THEN bonus
            ELSE 0
        END
    ) AS high_salary_bonus

FROM employees
GROUP BY department;



-- ============================================================
-- COUNT(CASE)
-- ============================================================

-- Example 7

SELECT
    COUNT(
        CASE
            WHEN salary > 100000 THEN 1
        END
    ) AS high_salary_count
FROM employees;



-- Example 8
-- Same result using SUM(CASE).

SELECT
    SUM(
        CASE
            WHEN salary > 100000 THEN 1
            ELSE 0
        END
    ) AS high_salary_count
FROM employees;



-- ============================================================
-- Orders Dashboard Example
-- ============================================================

CREATE TABLE orders (
    order_id INT,
    status VARCHAR(20),
    amount INT
);

INSERT INTO orders VALUES
(1,'SUCCESS',1000),
(2,'FAILED',500),
(3,'SUCCESS',2000),
(4,'CANCELLED',700),
(5,'FAILED',300),
(6,'SUCCESS',800);

-- Example 9

SELECT
    COUNT(*) AS total_orders,

    SUM(
        CASE
            WHEN status = 'SUCCESS' THEN 1
            ELSE 0
        END
    ) AS success_orders,

    SUM(
        CASE
            WHEN status = 'FAILED' THEN 1
            ELSE 0
        END
    ) AS failed_orders,

    SUM(
        CASE
            WHEN status = 'CANCELLED' THEN 1
            ELSE 0
        END
    ) AS cancelled_orders,

    SUM(
        CASE
            WHEN status = 'SUCCESS'
            THEN amount
            ELSE 0
        END
    ) AS success_revenue

FROM orders;



-- ============================================================
-- Multiple Revenue KPIs
-- ============================================================

-- Example 10

SELECT
    SUM(
        CASE
            WHEN status = 'SUCCESS'
            THEN amount
            ELSE 0
        END
    ) AS success_revenue,

    SUM(
        CASE
            WHEN status = 'FAILED'
            THEN amount
            ELSE 0
        END
    ) AS failed_revenue,

    SUM(
        CASE
            WHEN status = 'CANCELLED'
            THEN amount
            ELSE 0
        END
    ) AS cancelled_amount

FROM orders;



-- ============================================================
-- Mini Exercises
-- ============================================================

-- Exercise 1
-- Count employees earning more than 100000.

-- Your Query:



---------------------------------------------------------------

-- Exercise 2
-- Count employees earning
-- 100000 or less.

-- Your Query:



---------------------------------------------------------------

-- Exercise 3
-- Show total employees,
-- high salary employees,
-- and normal salary employees.

-- Your Query:



---------------------------------------------------------------

-- Exercise 4
-- Calculate total bonus
-- for employees earning
-- more than 100000.

-- Your Query:



---------------------------------------------------------------

-- Exercise 5
-- Show department-wise:

-- Total Employees
-- High Salary Employees
-- Normal Salary Employees

-- Your Query:



---------------------------------------------------------------

-- Exercise 6
-- Calculate department-wise
-- bonus paid to employees
-- earning more than 100000.

-- Your Query:



---------------------------------------------------------------

-- Exercise 7
-- Calculate:

-- Total Orders
-- Successful Orders
-- Failed Orders
-- Cancelled Orders

-- Your Query:



---------------------------------------------------------------

-- Exercise 8
-- Calculate:

-- Successful Revenue
-- Failed Revenue
-- Cancelled Revenue

-- Your Query:



---------------------------------------------------------------

-- Exercise 9
-- Rewrite Example 7 using
-- SUM(CASE).

-- Your Query:



---------------------------------------------------------------

-- Exercise 10
-- Build a single dashboard query
-- showing:

-- Total Employees
-- IT Employees
-- HR Employees
-- Finance Employees
-- High Salary Employees
-- Total Bonus Paid

-- Your Query:



-- ============================================================
-- End of Topic 7
-- ============================================================
```
