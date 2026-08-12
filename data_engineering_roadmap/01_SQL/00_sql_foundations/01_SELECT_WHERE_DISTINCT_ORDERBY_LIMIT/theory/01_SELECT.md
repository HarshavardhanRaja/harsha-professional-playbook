# SELECT

## What Is SELECT?

The `SELECT` clause defines what should appear in the final output of a SQL query.

It tells SQL:

> "After processing all the data, these are the columns I want to display."

Example:

```sql
SELECT employee_id,
       name
FROM employees;
```

SQL returns only the requested columns.

---

## Why Do We Need SELECT?

SELECT helps us:

* Retrieve only required columns
* Reduce unnecessary data transfer
* Improve query readability
* Reduce cloud costs in columnar databases
* Build stable APIs and data pipelines

---

## Mental Model

Think of SQL as preparing a report.

* **FROM** decides where the data comes from.
* **WHERE** decides which rows remain.
* **GROUP BY / HAVING** organize and filter groups.
* **SELECT** decides what finally appears in the report.

SELECT defines the **output**, not the processing.

---

## Example

Employee Table

| employee_id | name   | salary | department |
| ----------- | ------ | ------ | ---------- |
| 1           | Harsha | 120000 | IT         |
| 2           | Ravi   | 90000  | HR         |

Query

```sql
SELECT employee_id,
       name
FROM employees;
```

Output

| employee_id | name   |
| ----------- | ------ |
| 1           | Harsha |
| 2           | Ravi   |

Although `salary` and `department` exist, they are not returned because they were not selected.

---

## SELECT *

`SELECT *` returns every column from a table.

Example:

```sql
SELECT *
FROM employees;
```

Although convenient during exploration, it is generally discouraged in production.

---

## Why SELECT * Is Discouraged

### 1. Reads Unnecessary Columns

The application often needs only a few columns.

Reading all columns increases:

* Disk I/O
* Memory usage
* Network transfer
* CPU usage

---

### 2. Higher Cloud Cost

Columnar warehouses like BigQuery and Snowflake read only the required columns.

Using `SELECT *` may scan significantly more data, increasing query cost.

---

### 3. Schema Evolution

Suppose a new column is added later.

```text
salary
department
aadhaar_number
```

`SELECT *` automatically starts returning the new column.

This may unexpectedly affect downstream applications.

---

### 4. Breaks API Contracts

APIs should return only expected fields.

If new columns are added to the table, `SELECT *` may expose them without any code changes.

---

### 5. Security Risk

Sensitive columns like:

* PAN
* Aadhaar
* SSN
* Credit Card Number

may be returned unintentionally.

Explicit column selection avoids accidental exposure.

---

### 6. Harder To Read

Compare:

```sql
SELECT *
FROM employees;
```

vs

```sql
SELECT employee_id,
       name,
       department
FROM employees;
```

The second query immediately tells the reader what information is required.

---

## Best Practice

Instead of

```sql
SELECT *
FROM employees;
```

Write

```sql
SELECT employee_id,
       name,
       department
FROM employees;
```

Only retrieve the columns you actually need.

---

## Production Scenario

Suppose a dashboard only displays:

* Employee Name
* Department

Using

```sql
SELECT *
```

still reads every column from the table.

Instead,

```sql
SELECT name,
       department
FROM employees;
```

allows the database to read only the required columns, reducing cost and improving performance.

---

## Common Mistakes

### Mistake 1

Using `SELECT *` in production.

---

### Mistake 2

Selecting columns that are never used.

---

### Mistake 3

Returning sensitive columns unnecessarily.

---

### Mistake 4

Using `SELECT *` in APIs and ETL pipelines, making them tightly coupled to future schema changes.

---

## Interview Explanation

A concise interview answer:

> "The SELECT clause defines the final output of a SQL query. In production, I avoid `SELECT *` because it increases I/O, cloud cost, and security risks while tightly coupling applications to schema changes. I prefer explicitly selecting only the required columns for better performance, readability, and maintainability."

---

## Key Takeaways

* SELECT defines the final output.
* SELECT does not decide which rows are filtered.
* Avoid `SELECT *` in production.
* Explicit column selection improves performance, readability, security, and maintainability.
* Always retrieve only the columns required by the business.
