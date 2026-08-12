--------------------------------------------------
-- SAMPLE DATA
--------------------------------------------------

CREATE TABLE employees (
    emp_id INT,
    employee_name VARCHAR(50),
    department VARCHAR(50),
    salary INT
);

INSERT INTO employees VALUES
(1,'Harsha','IT',100000),
(2,'Ravi','IT',120000),
(3,'Priya','HR',50000),
(4,'Asha','HR',70000),
(5,'Kiran','Finance',90000),
(6,'Rohit','Finance',110000);

--------------------------------------------------
-- EXAMPLE 1
-- WHERE FILTERS ROWS
--------------------------------------------------

SELECT *
FROM employees
WHERE salary > 80000;

-- Expected Output

/*
1 Harsha IT      100000
2 Ravi   IT      120000
5 Kiran  Finance 90000
6 Rohit  Finance 110000
*/

--------------------------------------------------
-- EXAMPLE 2
-- HAVING FILTERS GROUPS
--------------------------------------------------

SELECT department,
       COUNT(*) AS employee_count
FROM employees
GROUP BY department
HAVING COUNT(*) >= 2;

-- Expected Output

/*
IT       2
HR       2
Finance  2
*/

--------------------------------------------------
-- EXAMPLE 3
-- ALIAS FAILS IN WHERE
--------------------------------------------------

SELECT salary AS sal
FROM employees
WHERE sal > 100000;

-- Error:
-- Alias not available during WHERE execution.

--------------------------------------------------
-- EXAMPLE 4
-- ALIAS WORKS IN ORDER BY
--------------------------------------------------

SELECT salary AS sal
FROM employees
ORDER BY sal DESC;

--------------------------------------------------
-- EXAMPLE 5
-- AGGREGATE FAILS IN WHERE
--------------------------------------------------

SELECT department,
       COUNT(*)
FROM employees
WHERE COUNT(*) > 1
GROUP BY department;

--------------------------------------------------
-- EXAMPLE 6
-- AGGREGATE WORKS IN HAVING
--------------------------------------------------

SELECT department,
       COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 1;