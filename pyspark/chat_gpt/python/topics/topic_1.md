# Python Topic 01 — Variables & Data Types 🚀

> Beginner-to-interview-level explanation of Variables and Data Types in Python with examples, edge cases, memory understanding, and interview questions.

---

# Table of Contents

1. What is a Variable?
2. Why Variables are Needed
3. Variable Naming Rules
4. Variable Assignment
5. Dynamic Typing in Python
6. Python Data Types Overview
7. Numeric Data Types
8. Strings
9. Boolean Type
10. Type Checking
11. Type Conversion
12. Mutable vs Immutable
13. Memory Behavior in Python
14. Multiple Assignment
15. Important Built-in Functions
16. Common Mistakes
17. Best Practices
18. Real-World Examples
19. Most Important Interview Questions
20. Tricky Interview Questions
21. Practice Questions

---

# 1. What is a Variable?

A variable is a name used to store data in memory.

Think of a variable like a labeled box.

Example:

```python
name = "Harsha"
```

Here:

* `name` → variable name
* `"Harsha"` → value stored

Python stores the value in memory and the variable refers to that memory location.

---

# Real-Life Analogy

Imagine:

```text
Box Label = name
Inside Box = Harsha
```

Whenever you use `name`, Python gives the stored value.

---

# 2. Why Variables are Needed

Without variables:

```python
print("Harsha")
print("Harsha")
print("Harsha")
```

With variables:

```python
name = "Harsha"

print(name)
print(name)
print(name)
```

Benefits:

* Reusability
* Readability
* Easy updates
* Better debugging

---

# 3. Variable Naming Rules

## Valid Variable Names

```python
name = "Harsha"
age = 25
employee_salary = 50000
_name = "Python"
```

---

# Invalid Variable Names

```python
2name = "Wrong"
```

Reason:
Variable cannot start with a number.

---

```python
first-name = "Wrong"
```

Reason:
Hyphen `-` treated as subtraction operator.

---

# Rules

## Allowed

* letters
* numbers
* underscore `_`

---

## Not Allowed

* spaces
* special characters
* starting with number

---

# Case Sensitive

```python
name = "Harsha"
Name = "Python"
```

These are DIFFERENT variables.

---

# Naming Convention (VERY IMPORTANT)

Use snake_case.

Good:

```python
employee_salary = 50000
```

Bad:

```python
EmployeeSalary = 50000
empsal = 50000
```

---

# 4. Variable Assignment

## Basic Assignment

```python
x = 10
```

Python:

1. Creates object `10`
2. Stores in memory
3. Makes `x` point to it

---

# Reassignment

```python
x = 10
x = 20
```

Now `x` points to new value.

---

# Important

Python variables DO NOT store actual values directly.

They store REFERENCES to objects.

This is VERY IMPORTANT for interviews.

---

# 5. Dynamic Typing in Python

Python is dynamically typed.

Meaning:
You do NOT declare datatype explicitly.

---

# Example

```python
x = 10
x = "Harsha"
x = True
```

Same variable can hold different types.

---

# Why?

Because Python decides datatype during runtime.

---

# Compared to Java

Java:

```java
int x = 10;
```

Python:

```python
x = 10
```

Simpler and faster to write.

---

# 6. Python Data Types Overview

Python has multiple built-in data types.

| Category | Data Types          |
| -------- | ------------------- |
| Numeric  | int, float, complex |
| Sequence | str, list, tuple    |
| Set      | set                 |
| Mapping  | dict                |
| Boolean  | bool                |
| Binary   | bytes               |

---

# Most Important for Beginners

* int
* float
* str
* bool
* list
* tuple
* dict
* set

---

# 7. Numeric Data Types

# Integer (int)

Whole numbers.

```python
age = 25
```

---

# Float

Decimal numbers.

```python
salary = 50000.75
```

---

# Complex Numbers

Used rarely.

```python
x = 3 + 4j
```

---

# Arithmetic Operations

```python
print(10 + 5)
print(10 - 5)
print(10 * 5)
print(10 / 5)
print(10 % 3)
print(10 ** 2)
```

---

# Important Difference

## Division

```python
print(5 / 2)
```

Output:

```python
2.5
```

Always returns float.

---

## Floor Division

```python
print(5 // 2)
```

Output:

```python
2
```

Removes decimal.

---

# 8. Strings

Strings are sequences of characters.

```python
name = "Harsha"
```

---

# String Types

```python
single = 'Python'
double = "Python"
triple = '''Python'''
```

---

# String Indexing

```python
name = "Python"

print(name[0])
```

Output:

```python
P
```

---

# Negative Indexing

```python
print(name[-1])
```

Output:

```python
n
```

---

# String Slicing

```python
print(name[0:4])
```

Output:

```python
Pyth
```

---

# Important String Methods

```python
name.lower()
name.upper()
name.replace("P", "J")
name.split()
```

---

# Strings are Immutable (VERY IMPORTANT)

```python
name = "Python"
name[0] = "J"
```

ERROR.

Because strings cannot be modified.

---

# 9. Boolean Type

Represents:

* True
* False

---

# Example

```python
is_active = True
```

---

# Used in Conditions

```python
if is_active:
    print("Active")
```

---

# Boolean Operations

```python
print(True and False)
print(True or False)
print(not True)
```

---

# 10. Type Checking

Use `type()`.

```python
x = 10
print(type(x))
```

Output:

```python
<class 'int'>
```

---

# isinstance()

Better than type checking.

```python
print(isinstance(x, int))
```

---

# Why isinstance() Better?

Because it supports inheritance.

Important interview point.

---

# 11. Type Conversion

Convert one datatype into another.

---

# String to Integer

```python
age = int("25")
```

---

# Integer to String

```python
num = str(100)
```

---

# Float to Integer

```python
x = int(10.9)
```

Output:

```python
10
```

Decimal removed.

---

# Common Conversion Functions

| Function | Purpose            |
| -------- | ------------------ |
| int()    | Convert to integer |
| float()  | Convert to float   |
| str()    | Convert to string  |
| bool()   | Convert to boolean |
| list()   | Convert to list    |

---

# 12. Mutable vs Immutable (VERY IMPORTANT)

One of the MOST ASKED interview topics.

---

# Mutable

Can change after creation.

Examples:

* list
* dict
* set

---

# Immutable

Cannot change after creation.

Examples:

* int
* float
* str
* tuple

---

# Example of Mutable

```python
nums = [1,2,3]
nums.append(4)
```

Original object modified.

---

# Example of Immutable

```python
name = "Python"
name = name + "3"
```

New object created.

---

# Why Important?

Impacts:

* memory
* performance
* bugs
* multithreading

---

# 13. Memory Behavior in Python

VERY IMPORTANT for deeper interviews.

---

# Variables are References

```python
x = 10
y = x
```

Both point to same object.

---

# id() Function

Shows memory identity.

```python
x = 10
print(id(x))
```

---

# Example

```python
x = [1,2]
y = x

y.append(3)

print(x)
```

Output:

```python
[1,2,3]
```

Why?

Both refer same list object.

---

# Important Concept

Assignment copies references, NOT actual object.

---

# 14. Multiple Assignment

```python
x, y, z = 1, 2, 3
```

---

# Same Value Assignment

```python
a = b = c = 100
```

---

# Swapping Variables

```python
x = 10
y = 20

x, y = y, x
```

Pythonic way.

---

# 15. Important Built-in Functions

# len()

```python
len("Python")
```

---

# max()

```python
max([1,2,3])
```

---

# min()

```python
min([1,2,3])
```

---

# sum()

```python
sum([1,2,3])
```

---

# round()

```python
round(10.567, 2)
```

---

# 16. Common Mistakes

# Mistake 1

```python
age = input("Enter age")
print(age + 10)
```

ERROR.

Because input() returns string.

Correct:

```python
age = int(input("Enter age"))
```

---

# Mistake 2

```python
name = "Python"
name[0] = "J"
```

Strings immutable.

---

# Mistake 3

```python
x = y = []
```

Both reference same list.

Dangerous.

---

# 17. Best Practices

# Use Meaningful Names

Good:

```python
employee_salary
```

Bad:

```python
x
```

---

# Follow snake_case

```python
employee_name
```

---

# Avoid Overwriting Built-ins

BAD:

```python
list = [1,2,3]
```

Now built-in `list()` broken.

---

# 18. Real-World Examples

# Example 1 — User Profile

```python
name = "Harsha"
age = 25
salary = 50000.5
is_employee = True
```

---

# Example 2 — Ecommerce

```python
product_name = "iPhone"
price = 1000
stock_available = True
```

---

# Example 3 — Banking

```python
account_balance = 50000
is_kyc_done = False
```

---

# 19. Most Important Interview Questions

# Q1. What is a variable in Python?

A variable is a reference name pointing to an object stored in memory.

---

# Q2. Is Python statically typed or dynamically typed?

Python is dynamically typed.

Datatype decided during runtime.

---

# Q3. Difference between mutable and immutable?

Mutable objects can change after creation.
Immutable objects cannot.

---

# Q4. Are strings mutable?

No.
Strings are immutable.

---

# Q5. Difference between `==` and `is`?

`==` compares values.

`is` compares memory identity.

Example:

```python
x = [1,2]
y = [1,2]

print(x == y)
print(x is y)
```

Output:

```python
True
False
```

---

# Q6. Why use isinstance() instead of type()?

Because isinstance supports inheritance.

---

# Q7. What does input() return?

Always string.

---

# Q8. What is Python memory management?

Python automatically manages memory using reference counting and garbage collection.

---

# 20. Tricky Interview Questions

# Q1

```python
x = [1,2,3]
y = x

y.append(4)

print(x)
```

Output?

```python
[1,2,3,4]
```

Reason:
Both refer same object.

---

# Q2

```python
x = "Python"
x += "3"
```

Did original string change?

NO.
New string object created.

---

# Q3

```python
a = 256
b = 256

print(a is b)
```

Usually True.

Reason:
Python integer caching.

---

# Q4

```python
a = 1000
b = 1000

print(a is b)
```

May be False.

Why?

Larger integers may not be cached.

---

# Q5

```python
x = [[]] * 3
x[0].append(1)
print(x)
```

Output:

```python
[[1], [1], [1]]
```

Reason:
All inner lists reference same object.

VERY IMPORTANT interview question.

---

# 21. Practice Questions

# Beginner

1. Create variables for student details.
2. Convert string age to integer.
3. Swap two variables.
4. Find datatype of variables.
5. Perform arithmetic operations.

---

# Intermediate

1. Check mutable vs immutable behavior.
2. Experiment with `is` vs `==`.
3. Create examples using type conversion.
4. Explore memory IDs using id().

---

# Advanced

1. Explain Python variable memory model.
2. Explain reference behavior.
3. Explain string immutability internally.
4. Explain integer caching.

---

# Revision Summary

```text
Variable → Reference to object
Python → Dynamically typed
Mutable → Can change
Immutable → Cannot change
== → Value comparison
is → Memory comparison
input() → Returns string
Strings → Immutable
Lists → Mutable
```

---

# What to Learn Next

Recommended next topic:

👉 Operators + Conditional Statements

because:

Variables + Datatypes
↓
Operators
↓
Conditions
↓
Loops
↓
Functions

This builds strong fundamentals.

---

Happy Learning 🚀
