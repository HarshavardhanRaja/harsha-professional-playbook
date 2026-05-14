# Python Notes — 02 Data Types 🚀

> 📘 Beginner → Interview Level Python Notes
> Topic: Python Data Types

---

# 🎯 Learning Outcomes

After completing this file, you should be able to:

✅ Understand all major Python data types
✅ Differentiate mutable vs immutable types
✅ Explain datatype behavior internally
✅ Use correct datatypes in real-world problems
✅ Avoid datatype-related bugs
✅ Answer interview questions confidently

---

# 📚 Table of Contents

* [1. What are Data Types?](#1-what-are-data-types)
* [2. Why Data Types Matter](#2-why-data-types-matter)
* [3. Categories of Python Data Types](#3-categories-of-python-data-types)
* [4. Numeric Data Types](#4-numeric-data-types)
* [5. String Data Type](#5-string-data-type)
* [6. Boolean Data Type](#6-boolean-data-type)
* [7. List Data Type](#7-list-data-type)
* [8. Tuple Data Type](#8-tuple-data-type)
* [9. Set Data Type](#9-set-data-type)
* [10. Dictionary Data Type](#10-dictionary-data-type)
* [11. None Type](#11-none-type)
* [12. Mutable vs Immutable Types](#12-mutable-vs-immutable-types)
* [13. Type Checking](#13-type-checking)
* [14. Type Conversion](#14-type-conversion)
* [15. Memory Behavior of Data Types](#15-memory-behavior-of-data-types)
* [16. Common Beginner Mistakes](#16-common-beginner-mistakes)
* [17. Best Practices](#17-best-practices)
* [18. Real-World Examples](#18-real-world-examples)
* [19. Important Interview Questions](#19-important-interview-questions)
* [20. Tricky Interview Questions](#20-tricky-interview-questions)
* [21. Practice Questions](#21-practice-questions)
* [22. Revision Summary](#22-revision-summary)

---

# 🧠 How to Use This File

For every datatype:

1. Understand purpose
2. Run examples yourself
3. Modify examples
4. Predict outputs before running
5. Compare mutable vs immutable behavior
6. Revise interview questions

---

# 1. What are Data Types?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A datatype defines:

* What kind of data is stored
* What operations are allowed
* How memory is allocated internally

---

# Example

```python id="g0n1bc"
age = 25
```

Here:

* `25` → integer datatype
* Python knows arithmetic operations are allowed

---

# Another Example

```python id="vj1j98"
name = "Harsha"
```

Here:

* `"Harsha"` → string datatype
* Python allows string operations

---

# Why Important?

Datatype determines:

✅ Memory usage
✅ Performance
✅ Allowed operations
✅ Internal behavior

---

# 2. Why Data Types Matter

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Choosing correct datatype is important.

Example:

```python id="quv4ik"
marks = [90, 85, 95]
```

List chosen because:

* multiple values needed
* ordered collection needed

---

# Wrong Choice Example

```python id="25o0w4"
marks = {90, 85, 95}
```

Set may change order unexpectedly.

---

# Real-World Impact

Bad datatype choices can cause:

❌ Bugs
❌ Performance issues
❌ Memory wastage
❌ Difficult debugging

---

# 3. Categories of Python Data Types

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Category | Data Types          |
| -------- | ------------------- |
| Numeric  | int, float, complex |
| Sequence | str, list, tuple    |
| Set      | set                 |
| Mapping  | dict                |
| Boolean  | bool                |
| Special  | NoneType            |

---

# Most Commonly Used

| Datatype | Usage          |
| -------- | -------------- |
| int      | Numbers        |
| str      | Text           |
| bool     | Conditions     |
| list     | Collections    |
| dict     | Key-value data |

---

# 4. Numeric Data Types

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Integer (int)

Whole numbers.

```python id="7xnscc"
age = 25
```

---

# Float

Decimal numbers.

```python id="6y4m4p"
salary = 50000.75
```

---

# Complex Numbers

Rarely used.

```python id="5u7x7u"
x = 3 + 4j
```

---

# Arithmetic Operations

```python id="prl9v0"
print(10 + 5)
print(10 - 5)
print(10 * 5)
print(10 / 5)
print(10 % 3)
print(10 ** 2)
```

---

# Division vs Floor Division

## Normal Division

```python id="m91w1m"
print(5 / 2)
```

Output:

```python id="fd6r6v"
2.5
```

---

## Floor Division

```python id="gj6r7u"
print(5 // 2)
```

Output:

```python id="nn6wla"
2
```

Decimal removed.

---

# Numeric Type Conversion

```python id="1fd54w"
x = int("10")
y = float(5)
```

---

# Important Interview Point

Python integers are immutable.

---

# 5. String Data Type

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Strings store text.

```python id="dhgy6v"
name = "Python"
```

---

# String Types

```python id="s7x2u9"
single = 'Python'
double = "Python"
triple = '''Python'''
```

---

# String Indexing

```python id="d2ttd2"
name = "Python"

print(name[0])
```

Output:

```python id="ul8o4l"
P
```

---

# Negative Indexing

```python id="s7ifsk"
print(name[-1])
```

Output:

```python id="9zy3vq"
n
```

---

# String Slicing

```python id="8k5r0d"
print(name[0:4])
```

Output:

```python id="m1zhj5"
Pyth
```

---

# Important String Methods

```python id="z2tqq2"
name.lower()
name.upper()
name.replace("P", "J")
name.split()
```

---

# Strings are Immutable

VERY IMPORTANT.

```python id="1uxy2w"
name = "Python"

name[0] = "J"
```

ERROR.

Reason:
Strings cannot be modified after creation.

---

# String Concatenation

```python id="1d6c5l"
first = "Hello"
second = "World"

print(first + second)
```

---

# f-Strings (BEST PRACTICE)

```python id="vb3e8v"
name = "Harsha"
age = 25

print(f"My name is {name} and age is {age}")
```

---

# 6. Boolean Data Type

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Boolean represents:

* True
* False

---

# Example

```python id="mjlwm8"
is_active = True
```

---

# Used in Conditions

```python id="nqcd7w"
if is_active:
    print("User Active")
```

---

# Boolean Operations

```python id="7xjqmu"
print(True and False)
print(True or False)
print(not True)
```

---

# Truthy & Falsy Values

Falsy values:

```python id="70m8e8"
False
0
None
""
[]
{}
set()
```

Everything else usually becomes True.

---

# Example

```python id="3y6qfr"
print(bool(""))
print(bool("Python"))
```

---

# 7. List Data Type

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Lists store multiple values.

Ordered and mutable.

```python id="m6cx3g"
nums = [1, 2, 3]
```

---

# Access Elements

```python id="95nvt7"
print(nums[0])
```

---

# Modify Elements

```python id="n05j9y"
nums[0] = 100
```

Allowed because lists are mutable.

---

# Important List Methods

```python id="eexv6u"
nums.append(4)
nums.insert(1, 200)
nums.remove(2)
nums.pop()
nums.sort()
nums.reverse()
```

---

# List Slicing

```python id="z0gvfe"
print(nums[0:2])
```

---

# Nested Lists

```python id="pj9t3v"
matrix = [
    [1,2],
    [3,4]
]
```

---

# Important Interview Point

Lists are mutable.

---

# 8. Tuple Data Type

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tuples are ordered and immutable.

```python id="n6q2lk"
point = (10, 20)
```

---

# Access Tuple Elements

```python id="g1lfxh"
print(point[0])
```

---

# Tuple Unpacking

```python id="r0jll1"
x, y = point
```

---

# Why Tuples Exist?

Tuples:

* safer
* faster
* immutable

---

# Tuple Immutability

```python id="ru5e7m"
point[0] = 100
```

ERROR.

---

# Tuple vs List

| List        | Tuple       |
| ----------- | ----------- |
| Mutable     | Immutable   |
| Slower      | Faster      |
| More memory | Less memory |

---

# 9. Set Data Type

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sets store UNIQUE values.

Unordered collection.

```python id="q1dzif"
nums = {1,2,3,3}
```

Output:

```python id="mk7owu"
{1,2,3}
```

Duplicate removed automatically.

---

# Set Operations

```python id="lk4m9z"
a = {1,2,3}
b = {3,4,5}

print(a.union(b))
print(a.intersection(b))
```

---

# Important Properties

| Property           | Value |
| ------------------ | ----- |
| Ordered            | ❌     |
| Mutable            | ✅     |
| Duplicates Allowed | ❌     |

---

# Common Use Cases

✅ Removing duplicates
✅ Fast membership checking

---

# 10. Dictionary Data Type

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stores key-value pairs.

```python id="3b0yqj"
student = {
    "name": "Harsha",
    "age": 25
}
```

---

# Access Values

```python id="crv93j"
print(student["name"])
```

---

# Safer Access

```python id="tjlwm2"
print(student.get("age"))
```

---

# Add New Key

```python id="vvv10e"
student["city"] = "Bangalore"
```

---

# Loop Dictionary

```python id="sl9x4y"
for key, value in student.items():
    print(key, value)
```

---

# Important Properties

| Property               | Value           |
| ---------------------- | --------------- |
| Ordered                | ✅ (Python 3.7+) |
| Mutable                | ✅               |
| Duplicate Keys Allowed | ❌               |

---

# Real-World Use Cases

✅ JSON data
✅ APIs
✅ Configurations
✅ User profiles

---

# 11. None Type

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Represents absence of value.

```python id="mgjlwm"
x = None
```

---

# Why Important?

Used when:

* value not assigned yet
* no result available

---

# Example

```python id="64mfx4"
def test():
    pass

print(test())
```

Output:

```python id="34ys7d"
None
```

---

# 12. Mutable vs Immutable Types

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MOST IMPORTANT interview topic.

---

# Mutable Types

Can change after creation.

Examples:

* list
* dict
* set

---

# Immutable Types

Cannot change after creation.

Examples:

* int
* float
* str
* tuple

---

# Mutable Example

```python id="3ryovk"
nums = [1,2]
nums.append(3)
```

Same object modified.

---

# Immutable Example

```python id="vjlwm6"
name = "Python"
name = name + "3"
```

New object created.

---

# Why Important?

Impacts:

✅ Memory
✅ Performance
✅ Thread safety
✅ Bugs

---

# 13. Type Checking

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# type()

```python id="hjlwm2"
x = 10

print(type(x))
```

---

# isinstance()

Preferred in interviews.

```python id="2vjlwm"
print(isinstance(x, int))
```

---

# Why isinstance() Better?

Supports inheritance.

---

# 14. Type Conversion

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Convert datatype into another datatype.

---

# Examples

```python id="mjlwm7"
int("10")
float(5)
str(100)
bool(1)
list((1,2,3))
```

---

# Important Conversion Behavior

```python id="pjjlwm"
bool("")
```

Output:

```python id="8jlwmx"
False
```

---

```python id="tjlwm8"
bool("Python")
```

Output:

```python id="fjlwm0"
True
```

---

# 15. Memory Behavior of Data Types

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Python variables store references.

---

# Example

```python id="yjlwm8"
x = [1,2]
y = x
```

Both point to same object.

---

# Visual

```text id="jlwmr3"
x ──► [1,2]
y ──► [1,2]
```

---

# Example

```python id="jlwm6p"
y.append(3)

print(x)
```

Output:

```python id="jlwmn9"
[1,2,3]
```

---

# Important Point

Assignment copies references, NOT objects.

---

# 16. Common Beginner Mistakes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Mistake 1 — Using Mutable Default Values

Dangerous:

```python id="jlwm5k"
def test(nums=[]):
    nums.append(1)
```

---

# Mistake 2 — Confusing Tuple & List

```python id="jlwm0z"
point = (1,2)
point[0] = 10
```

ERROR.

---

# Mistake 3 — Assuming Sets Maintain Order

Sets unordered.

---

# Mistake 4 — Using `is` Instead of `==`

Wrong:

```python id="jlwm8x"
x = [1]
y = [1]

print(x is y)
```

---

# 17. Best Practices

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Choose Correct Datatype

| Need                   | Use   |
| ---------------------- | ----- |
| Ordered mutable data   | list  |
| Ordered immutable data | tuple |
| Unique values          | set   |
| Key-value data         | dict  |

---

# Prefer Tuples for Fixed Data

```python id="jlwmm4"
coordinates = (10,20)
```

---

# Use Meaningful Dictionary Keys

```python id="jlwm5n"
user = {
    "name": "Harsha"
}
```

---

# 18. Real-World Examples

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Ecommerce Product

```python id="jlwm3a"
product = {
    "name": "Laptop",
    "price": 50000,
    "in_stock": True
}
```

---

# Student Marks

```python id="jlwmz9"
marks = [90, 85, 95]
```

---

# Unique Visitors

```python id="jlwm1f"
users = {"Harsha", "Rahul", "Harsha"}
```

---

# 19. Important Interview Questions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Q1. Difference between list and tuple?

| List    | Tuple     |
| ------- | --------- |
| Mutable | Immutable |
| Slower  | Faster    |

---

# Q2. Are strings mutable?

No.

Strings are immutable.

---

# Q3. Why are tuples faster than lists?

Because immutability allows internal optimizations.

---

# Q4. Difference between set and list?

| List               | Set           |
| ------------------ | ------------- |
| Ordered            | Unordered     |
| Duplicates allowed | No duplicates |

---

# Q5. Difference between `==` and `is`?

`==` compares values.

`is` compares memory identity.

---

# Q6. Why use dictionaries?

Fast key-value lookup.

---

# Q7. Why are sets faster for membership checking?

Because sets internally use hashing.

---

# 20. Tricky Interview Questions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Q1

```python id="jlwmn2"
x = [1,2]
y = x

y.append(3)

print(x)
```

Output:

```python id="jlwmn7"
[1,2,3]
```

---

# Q2

```python id="jlwmq5"
x = "Python"
x += "3"
```

Did string change?

NO.

New object created.

---

# Q3

```python id="jlwm4m"
x = [[]] * 3

x[0].append(1)

print(x)
```

Output:

```python id="jlwmu1"
[[1], [1], [1]]
```

VERY IMPORTANT interview question.

Reason:
All inner lists reference same object.

---

# Q4

```python id="jlwmk8"
print(bool([]))
```

Output:

```python id="jlwmw2"
False
```

---

# 21. Practice Questions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Beginner

1. Create examples for every datatype.
2. Perform string slicing.
3. Create nested lists.
4. Convert string to integer.

---

# Intermediate

1. Compare mutable vs immutable behavior.
2. Experiment with shared references.
3. Create dictionary examples.

---

# Advanced

1. Explain why strings are immutable.
2. Explain set hashing internally.
3. Explain Python memory behavior.

---

# 22. Revision Summary

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text id="jlwm8c"
int → Whole numbers
float → Decimal numbers
str → Text
bool → True/False
list → Ordered mutable collection
tuple → Ordered immutable collection
set → Unique unordered collection
dict → Key-value collection
None → Absence of value
```

---

# ✅ Next Recommended Topic

👉 `03_mutable_vs_immutable.md`

This is one of the MOST IMPORTANT topics for:

* interviews
* debugging
* memory understanding
* real-world Python development

---

Happy Learning 🚀
