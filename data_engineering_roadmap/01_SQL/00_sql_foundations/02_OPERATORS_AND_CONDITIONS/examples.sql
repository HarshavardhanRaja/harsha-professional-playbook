-- ============================================================
-- Operators and Conditions - Examples
-- Topic:
-- Comparison Operators | Logical Operators | BETWEEN
-- IN | LIKE | SARGable Conditions
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
(3, 'Priya', 'Finance', 150000, '2019-06-20'),
(4, 'Amit', 'Sales', 80000, '2022-03-18'),
(5, 'Hari', 'IT', 95000, '2023-05-12'),
(6, 'Harish', 'Finance', 130000, '2018-09-25');

-- ============================================================
-- Comparison Operators
-- ============================================================

-- Example 1
-- Employees earning at least 100000.

SELECT *
FROM employees
WHERE salary >= 100000;

-- Example 2
-- Employees not belonging to HR.

SELECT *
FROM employees
WHERE department <> 'HR';

-- Example 3
-- Same result using !=

SELECT *
FROM employees
WHERE department != 'HR';

-- Discussion:
-- <> is ANSI SQL standard.
-- != is supported by most modern databases.

-- ============================================================
-- Logical Operators
-- ============================================================

-- Example 4
-- AND

SELECT *
FROM employees
WHERE department='IT'
AND salary>100000;

-- Example 5
-- OR

SELECT *
FROM employees
WHERE department='IT'
OR department='Finance';

-- Example 6
-- NOT

SELECT *
FROM employees
WHERE NOT salary > 100000;

-- Better

SELECT *
FROM employees
WHERE salary <=100000;

-- ============================================================
-- Operator Precedence
-- ============================================================

-- Example 7

SELECT *
FROM employees
WHERE department='IT'
AND salary>100000
OR department='Finance';

-- Better

SELECT *
FROM employees
WHERE (
department='IT'
AND salary>100000
)
OR department='Finance';

-- ============================================================
-- BETWEEN
-- ============================================================

-- Example 8

SELECT *
FROM employees
WHERE salary BETWEEN 90000 AND 120000;

-- Example 9

SELECT *
FROM employees
WHERE joining_date BETWEEN
'2020-01-01'
AND
'2022-12-31';

-- Discussion:
-- BETWEEN is inclusive.

-- ============================================================
-- IN
-- ============================================================

-- Example 10

SELECT *
FROM employees
WHERE department IN (
'IT',
'Finance'
);

-- Equivalent

SELECT *
FROM employees
WHERE department='IT'
OR department='Finance';

-- ============================================================
-- NOT IN
-- ============================================================

-- Example 11

SELECT *
FROM employees
WHERE department NOT IN (
'IT',
'HR'
);

-- Discussion:
-- Be careful if NULL values can appear
-- inside the list or subquery.

-- ============================================================
-- LIKE
-- ============================================================

-- Example 12
-- Starts with Har

SELECT *
FROM employees
WHERE name LIKE 'Har%';

-- Example 13
-- Ends with sha

SELECT *
FROM employees
WHERE name LIKE '%sha';

-- Example 14
-- Contains ari

SELECT *
FROM employees
WHERE name LIKE '%ari%';

-- Example 15
-- Exactly one character

SELECT *
FROM employees
WHERE name LIKE 'H_r%';

-- ============================================================
-- SARGable vs Non-SARGable
-- ============================================================

-- Example 16
-- Good

SELECT *
FROM employees
WHERE employee_id=3;

-- Example 17
-- Avoid

SELECT *
FROM employees
WHERE employee_id+1=4;

-- Example 18
-- Good

SELECT *
FROM employees
WHERE salary>100000;

-- Example 19
-- Avoid

SELECT *
FROM employees
WHERE salary*2>200000;

-- ============================================================
-- Mini Exercises
-- ============================================================

-- Exercise 1
-- Retrieve employees who are not in Sales.

-- Your Query:

---

-- Exercise 2
-- Retrieve employees from IT or Finance.

-- Your Query:

---

-- Exercise 3
-- Retrieve employees earning between
-- 90000 and 130000.

-- Your Query:

---

-- Exercise 4
-- Retrieve employees whose names start
-- with "Har".

-- Your Query:

---

-- Exercise 5
-- Retrieve employees whose names end
-- with "i".

-- Your Query:

---

-- Exercise 6
-- Rewrite the following query into a
-- SARGable version.

SELECT *
FROM employees
WHERE salary*2>240000;

-- Your Query:

---

-- Exercise 7
-- Rewrite the following query using IN.

SELECT *
FROM employees
WHERE department='IT'
OR department='Finance'
OR department='Sales';

-- Your Query:

---

-- Exercise 8
-- Rewrite the following query to improve
-- readability.

SELECT *
FROM employees
WHERE department='IT'
AND salary>100000
OR department='Finance';

-- Your Query:

-- ============================================================
-- End of Topic 3
-- ============================================================
