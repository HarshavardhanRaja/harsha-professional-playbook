# ORDER BY

## What Is ORDER BY?

The `ORDER BY` clause sorts the final result set based on one or more columns.

It tells SQL:

> "Display the result in the required order."

Example:

```sql
SELECT name,
       salary
FROM employees
ORDER BY salary DESC;
```

Employees are displayed from highest salary to lowest salary.

---

## Why Do We Need ORDER BY?

ORDER BY helps us:

* Sort data for reports
* Display Top N results
* Retrieve latest records
* Implement pagination
* Produce deterministic results

---

## Mental Model

Think of arranging books on a shelf.

Without ORDER BY:

```text
Book C
Book A
Book D
Book B
```

With ORDER BY:

```text
Book A
Book B
Book C
Book D
```

ORDER BY simply arranges the final output.

---

## Example

Employee Table

| employee_id | name   | salary |
| ----------- | ------ | ------ |
| 1           | Harsha | 120000 |
| 2           | Ravi   | 90000  |
| 3           | Priya  | 150000 |

Query

```sql
SELECT name,
       salary
FROM employees
ORDER BY salary DESC;
```

Output

| name   | salary |
| ------ | ------ |
| Priya  | 150000 |
| Harsha | 120000 |
| Ravi   | 90000  |

---

## ASC vs DESC

Ascending order (Default)

```sql
ORDER BY salary ASC;
```

Output

```text
90000
120000
150000
```

Descending order

```sql
ORDER BY salary DESC;
```

Output

```text
150000
120000
90000
```

---

## Multiple Column Sorting

ORDER BY can sort using multiple columns.

Example:

```sql
SELECT *
FROM employees
ORDER BY department,
         salary DESC;
```

SQL sorts:

1. By department.
2. If departments are the same, by salary in descending order.

Think of it as:

```text
Primary Sort Key
↓

Secondary Sort Key
```

---

## ORDER BY Using Aliases

Valid:

```sql
SELECT salary AS sal
FROM employees
ORDER BY sal;
```

Reason:

ORDER BY executes after SELECT.

The alias already exists.

---

## ORDER BY Without ORDER BY?

Consider:

```sql
SELECT *
FROM employees
LIMIT 10;
```

This does **not** guarantee the first 10 employees.

Tables are logically unordered.

Without ORDER BY, SQL may return different rows across executions depending on the execution plan, storage, indexes, or partitions.

If the order matters, always use ORDER BY.

---

## NULL Ordering

Different databases treat NULL values differently during sorting.

Instead of relying on database defaults, explicitly specify the desired NULL ordering if your database supports it.

This makes queries more predictable and portable.

---

## ORDER BY And Indexes

Suppose:

```sql
SELECT *
FROM employees
ORDER BY employee_id
LIMIT 10;
```

If `employee_id` is indexed, the database can often read the rows directly from the ordered index instead of performing a separate sort.

However,

```sql
ORDER BY salary;
```

cannot use the `employee_id` index because the sorting column is different.

An index only helps when its ordering matches the query.

---

## ORDER BY + LIMIT

A common production pattern:

```sql
SELECT *
FROM employees
ORDER BY salary DESC
LIMIT 10;
```

This returns the top 10 highest-paid employees.

Modern databases often optimize this using **Top-N optimization**, avoiding a full sort of all rows.

---

## Production Scenario

A dashboard shows the latest 20 orders.

Bad:

```sql
SELECT *
FROM orders
LIMIT 20;
```

Good:

```sql
SELECT *
FROM orders
ORDER BY order_date DESC
LIMIT 20;
```

The second query guarantees that the latest 20 orders are returned.

---

## Common Mistakes

### Mistake 1

Using LIMIT without ORDER BY.

---

### Mistake 2

Assuming tables are stored in a fixed order.

---

### Mistake 3

Using the wrong primary sort key in multi-column sorting.

---

### Mistake 4

Assuming every ORDER BY requires a full sort even when a suitable index exists.

---

## Interview Explanation

A concise interview answer:

> "ORDER BY sorts the final result set. It can sort using one or multiple columns, where the first column acts as the primary sort key and subsequent columns are used to break ties. In production, I always use ORDER BY with LIMIT whenever deterministic results are required and consider indexes to avoid unnecessary sorting."

---

## Key Takeaways

* ORDER BY sorts the final output.
* ASC is the default sorting order.
* Multiple columns create primary and secondary sort keys.
* ORDER BY executes after SELECT, so aliases can be used.
* LIMIT without ORDER BY produces non-deterministic results.
* Indexes can help avoid sorting when the ordering matches the indexed column.
* ORDER BY + LIMIT is commonly used for Top-N queries.
