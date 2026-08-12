# Operators and Conditions - Cheatsheet

---

# Comparison Operators

| Operator | Meaning                          |
| -------- | -------------------------------- |
| =        | Equal To                         |
| !=       | Not Equal To                     |
| <>       | Not Equal To (ANSI SQL Standard) |
| >        | Greater Than                     |
| >=       | Greater Than or Equal To         |
| <        | Less Than                        |
| <=       | Less Than or Equal To            |

---

## Best Practices

✅ Compare compatible data types.

✅ Keep the filtered column unchanged.

❌ Avoid unnecessary casting.

❌ Avoid calculations on filtered columns.

---

## Good

```sql
WHERE employee_id = 100
```

## Avoid

```sql
WHERE employee_id + 1 = 101
```

---

# Logical Operators

| Operator | Meaning                             |
| -------- | ----------------------------------- |
| AND      | All conditions must be TRUE         |
| OR       | At least one condition must be TRUE |
| NOT      | Reverses the result                 |

---

## Operator Precedence

```text
NOT
↓

AND
↓

OR
```

---

## Best Practice

Always use parentheses when mixing `AND` and `OR`.

Instead of:

```sql
WHERE department='IT'
AND salary>100000
OR department='Finance'
```

Prefer:

```sql
WHERE (
        department='IT'
        AND salary>100000
      )
OR department='Finance'
```

---

# BETWEEN

Returns values within a range.

Equivalent to:

```sql
WHERE salary >= 50000
AND salary <= 100000
```

---

## Remember

✅ BETWEEN is **inclusive**.

---

## TIMESTAMP Best Practice

Instead of:

```sql
WHERE order_timestamp BETWEEN
'2025-01-01'
AND
'2025-12-31'
```

Prefer:

```sql
WHERE order_timestamp >= '2025-01-01'
AND order_timestamp < '2026-01-01'
```

---

# IN

Instead of:

```sql
WHERE department='IT'
OR department='HR'
OR department='Finance'
```

Prefer:

```sql
WHERE department IN (
    'IT',
    'HR',
    'Finance'
)
```

---

# NOT IN

⚠ Be careful if the list contains `NULL`.

```sql
WHERE department NOT IN (...)
```

We'll study this in detail in the NULL Handling topic.

---

# LIKE

## %

Matches **zero or more characters**

Examples

```sql
LIKE 'Har%'
```

Starts with Har

---

```sql
LIKE '%sha'
```

Ends with sha

---

```sql
LIKE '%ar%'
```

Contains ar

---

## _

Matches **exactly one character**

Example

```sql
LIKE 'H_rsha'
```

Matches:

```text
Harsha
```

---

# Performance Tips

✅ Prefix search

```sql
LIKE 'Har%'
```

Generally index-friendly.

---

❌ Leading wildcard

```sql
LIKE '%Har%'
```

Usually cannot efficiently use the index.

---

# SARGable Conditions

## Good

```sql
WHERE salary > 100000
```

```sql
WHERE employee_id = 100
```

```sql
WHERE joining_date >= '2025-01-01'
```

---

## Avoid

```sql
WHERE salary * 2 > 200000
```

```sql
WHERE employee_id + 1 = 101
```

```sql
WHERE YEAR(joining_date)=2025
```

---

# Production Best Practices

✅ Compare directly with the column.

✅ Use parentheses with AND/OR.

✅ Use IN for multiple values.

✅ Use prefix LIKE searches when possible.

✅ Use half-open ranges for TIMESTAMP columns.

❌ Avoid calculations on filtered columns.

❌ Avoid leading wildcards when performance matters.

❌ Be careful with NOT IN when NULL values are possible.

---

# Quick Revision

```text
Comparison Operators
↓

Compare values

-----------------------

AND

↓

All TRUE

-----------------------

OR

↓

Any TRUE

-----------------------

NOT

↓

Reverse result

-----------------------

BETWEEN

↓

Inclusive range

-----------------------

IN

↓

Multiple values

-----------------------

LIKE

↓

Pattern matching

-----------------------

%

↓

Zero or more characters

-----------------------

_

↓

Exactly one character

-----------------------

SARGable

↓

Column OP Value

-----------------------

Non-SARGable

↓

Function/Calculation on Column
```
