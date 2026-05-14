# Complete Python Mastery Notes 🚀

> A complete beginner-to-intermediate Python guide inspired by the concepts commonly taught in professional Python learning paths.

---

# Table of Contents

1. Introduction to Python
2. Installing Python
3. Variables & Data Types
4. Strings
5. Numbers
6. Operators
7. User Input
8. Conditional Statements
9. Loops
10. Lists
11. Tuples
12. Sets
13. Dictionaries
14. Functions
15. Scope
16. Modules & Packages
17. File Handling
18. Exception Handling
19. Object-Oriented Programming
20. Iterators & Generators
21. List Comprehensions
22. Lambda Functions
23. Decorators
24. Virtual Environments
25. pip & Package Management
26. Regular Expressions
27. JSON Handling
28. CSV Handling
29. Working with Dates & Time
30. OS Module
31. Logging
32. Debugging
33. Best Practices
34. Python Interview Questions
35. Mini Projects
36. Next Steps for Data Engineering

---

# 1. Introduction to Python

Python is:

* Easy to read
* Beginner friendly
* Powerful
* Used in:

  * Web Development
  * Data Engineering
  * Machine Learning
  * Automation
  * Scripting
  * APIs

---

# 2. Installing Python

Download:
[https://www.python.org/downloads/](https://www.python.org/downloads/)

Verify installation:

```bash
python --version
```

---

# 3. Variables & Data Types

Variables store data.

```python
name = "Harsha"
age = 25
salary = 10000.5
is_active = True
```

---

# Important Data Types

| Type  | Example |
| ----- | ------- |
| int   | 10      |
| float | 10.5    |
| str   | "hello" |
| bool  | True    |
| list  | [1,2,3] |
| tuple | (1,2,3) |
| set   | {1,2,3} |
| dict  | {"a":1} |

---

# Type Checking

```python
print(type(name))
```

---

# 4. Strings

Strings are sequences of characters.

```python
message = "Hello Python"
```

---

# String Indexing

```python
print(message[0])
print(message[-1])
```

---

# String Slicing

```python
print(message[0:5])
```

---

# Common String Methods

```python
print(message.lower())
print(message.upper())
print(message.replace("Python", "World"))
print(message.split())
```

---

# f-Strings

Best way to format strings.

```python
name = "Harsha"
age = 25

print(f"My name is {name} and I am {age}")
```

---

# 5. Numbers

## Arithmetic Operators

```python
print(5 + 2)
print(5 - 2)
print(5 * 2)
print(5 / 2)
print(5 // 2)
print(5 % 2)
print(5 ** 2)
```

---

# 6. Operators

## Comparison Operators

```python
==
!=
>
<
>=
<=
```

---

# Logical Operators

```python
and
or
not
```

---

# Membership Operators

```python
in
not in
```

---

# 7. User Input

```python
name = input("Enter your name: ")
print(name)
```

---

# Type Conversion

```python
age = int(input("Enter age: "))
```

---

# 8. Conditional Statements

```python
age = 20

if age >= 18:
    print("Adult")
elif age == 17:
    print("Almost adult")
else:
    print("Minor")
```

---

# Nested Conditions

```python
if age > 18:
    if age < 60:
        print("Working age")
```

---

# Ternary Operator

```python
status = "Adult" if age >= 18 else "Minor"
```

---

# 9. Loops

# For Loop

```python
for i in range(5):
    print(i)
```

---

# While Loop

```python
count = 0

while count < 5:
    print(count)
    count += 1
```

---

# break & continue

```python
for i in range(10):
    if i == 5:
        break
```

```python
for i in range(5):
    if i == 2:
        continue
```

---

# 10. Lists

Lists are ordered and mutable.

```python
nums = [1,2,3]
```

---

# Important List Methods

```python
nums.append(4)
nums.insert(0, 100)
nums.remove(2)
nums.pop()
nums.sort()
nums.reverse()
```

---

# List Slicing

```python
print(nums[1:3])
```

---

# Loop Through Lists

```python
for num in nums:
    print(num)
```

---

# 11. Tuples

Tuples are immutable.

```python
point = (10,20)
```

---

# Tuple Unpacking

```python
x, y = point
```

---

# 12. Sets

Sets contain unique values.

```python
nums = {1,2,3,3}
print(nums)
```

---

# Set Operations

```python
a = {1,2,3}
b = {3,4,5}

print(a.union(b))
print(a.intersection(b))
```

---

# 13. Dictionaries

Key-value pairs.

```python
student = {
    "name": "Harsha",
    "age": 25
}
```

---

# Access Values

```python
print(student["name"])
print(student.get("age"))
```

---

# Add/Update

```python
student["city"] = "Bangalore"
```

---

# Loop Dictionary

```python
for key, value in student.items():
    print(key, value)
```

---

# 14. Functions

Functions help reuse code.

```python
def greet(name):
    return f"Hello {name}"
```

---

# Default Parameters

```python
def greet(name="Guest"):
    print(name)
```

---

# *args

Accept multiple positional arguments.

```python
def add(*nums):
    return sum(nums)
```

---

# **kwargs

Accept multiple keyword arguments.

```python
def info(**data):
    print(data)
```

---

# 15. Scope

## Local Scope

Variable inside function.

## Global Scope

Variable outside function.

```python
x = 10

def test():
    y = 20
```

---

# LEGB Rule

Python searches variables in:

* Local
* Enclosing
* Global
* Built-in

---

# 16. Modules & Packages

Modules are Python files.

```python
import math

print(math.sqrt(25))
```

---

# Create Custom Module

math_utils.py

```python

def add(a,b):
    return a+b
```

main.py

```python
import math_utils
```

---

# Packages

Folder containing Python modules.

---

# 17. File Handling

# Read File

```python
with open("data.txt", "r") as f:
    data = f.read()
```

---

# Write File

```python
with open("data.txt", "w") as f:
    f.write("Hello")
```

---

# Append File

```python
with open("data.txt", "a") as f:
    f.write("New line")
```

---

# 18. Exception Handling

Prevents program crashes.

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
finally:
    print("Done")
```

---

# Raise Exceptions

```python
raise ValueError("Invalid value")
```

---

# 19. Object-Oriented Programming

# What is OOP?

OOP organizes code using classes and objects.

---

# Class & Object

```python
class Employee:

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

emp1 = Employee("Harsha", 50000)
```

---

# self Keyword

Represents current object.

---

# Instance Variables

Different for every object.

---

# Class Variables

Shared across objects.

```python
class Employee:
    company = "ABC"
```

---

# Methods

```python
class Employee:

    def greet(self):
        print("Hello")
```

---

# Inheritance

```python
class Developer(Employee):
    pass
```

---

# Method Overriding

```python
class Animal:
    def sound(self):
        print("Animal sound")

class Dog(Animal):
    def sound(self):
        print("Bark")
```

---

# Encapsulation

Hide implementation details.

```python
class Bank:
    def __init__(self):
        self.__balance = 0
```

---

# Polymorphism

Same method behaves differently.

---

# Class Methods

```python
@classmethod
def company_name(cls):
    return cls.company
```

---

# Static Methods

```python
@staticmethod
def is_valid(age):
    return age > 18
```

---

# Magic Methods

```python
__init__
__str__
__repr__
```

---

# 20. Iterators & Generators

# Iterator

```python
nums = iter([1,2,3])
print(next(nums))
```

---

# Generator

```python
def gen():
    yield 1
    yield 2
```

---

# Why Generators?

* Memory efficient
* Useful for large datasets

---

# 21. List Comprehensions

Compact way to create lists.

```python
squares = [x*x for x in range(10)]
```

---

# Conditional List Comprehension

```python
evens = [x for x in range(10) if x % 2 == 0]
```

---

# 22. Lambda Functions

Anonymous functions.

```python
square = lambda x: x*x
```

---

# map()

```python
nums = [1,2,3]
result = list(map(lambda x: x*2, nums))
```

---

# filter()

```python
nums = [1,2,3,4]
result = list(filter(lambda x: x % 2 == 0, nums))
```

---

# 23. Decorators

Decorators modify functions.

```python
def decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper
```

---

# Using Decorator

```python
@decorator
def hello():
    print("Hello")
```

---

# 24. Virtual Environments

# Create

```bash
python -m venv env
```

---

# Activate

Windows:

```bash
env\Scripts\activate
```

Mac/Linux:

```bash
source env/bin/activate
```

---

# Why Use Virtual Environments?

* Avoid dependency conflicts
* Project isolation

---

# 25. pip & Package Management

# Install Package

```bash
pip install pandas
```

---

# requirements.txt

```bash
pip freeze > requirements.txt
```

---

# Install Requirements

```bash
pip install -r requirements.txt
```

---

# 26. Regular Expressions

```python
import re
```

---

# Search Pattern

```python
text = "My number is 9876543210"

result = re.search(r"\d+", text)
```

---

# Common Regex Symbols

| Symbol | Meaning       |
| ------ | ------------- |
| \d     | Digit         |
| \w     | Word          |
| .      | Any character |
| *      | Zero or more  |
| +      | One or more   |

---

# 27. JSON Handling

# Read JSON

```python
import json
```

```python
with open("data.json") as f:
    data = json.load(f)
```

---

# Write JSON

```python
with open("data.json", "w") as f:
    json.dump(data, f)
```

---

# 28. CSV Handling

```python
import csv
```

---

# Read CSV

```python
with open("data.csv") as f:
    reader = csv.reader(f)
```

---

# Write CSV

```python
with open("data.csv", "w") as f:
    writer = csv.writer(f)
```

---

# 29. Working with Dates & Time

```python
import datetime
```

---

# Current Date

```python
today = datetime.date.today()
```

---

# Current Time

```python
now = datetime.datetime.now()
```

---

# Formatting Dates

```python
print(now.strftime("%Y-%m-%d"))
```

---

# 30. OS Module

```python
import os
```

---

# Current Directory

```python
print(os.getcwd())
```

---

# List Files

```python
print(os.listdir())
```

---

# Create Directory

```python
os.mkdir("test")
```

---

# 31. Logging

Better than print statements.

```python
import logging
```

---

# Basic Logging

```python
logging.basicConfig(level=logging.INFO)
logging.info("Program started")
```

---

# 32. Debugging

# Common Techniques

* Read traceback carefully
* Use print statements
* Use debugger
* Check variable values

---

# pdb Debugger

```python
import pdb
pdb.set_trace()
```

---

# 33. Best Practices

# Naming

Good:

```python
employee_salary
```

Bad:

```python
x
```

---

# Follow PEP8

* Proper indentation
* Meaningful names
* Small functions

---

# DRY Principle

Don't Repeat Yourself.

---

# Write Modular Code

Split code into files/functions.

---

# 34. Python Interview Questions

# Basics

## Mutable vs Immutable

Mutable:

* list
* dict
* set

Immutable:

* tuple
* string
* int

---

# List vs Tuple

| List    | Tuple     |
| ------- | --------- |
| Mutable | Immutable |
| Slower  | Faster    |

---

# Deep Copy vs Shallow Copy

Shallow copy copies references.
Deep copy copies everything.

---

# OOP Questions

* What is inheritance?
* What is polymorphism?
* Difference between class and object?
* What is encapsulation?

---

# Advanced Questions

* What is GIL?
* Generator vs Iterator?
* Multithreading vs Multiprocessing?

---

# 35. Mini Projects

# Beginner Projects

* Calculator
* Todo App
* Number Guessing Game

---

# Intermediate Projects

* Expense Tracker
* CSV Processor
* File Organizer
* Weather App

---

# Advanced Projects

* REST API
* ETL Pipeline
* Web Scraper
* Automation Bot

---

# 36. Next Steps for Data Engineering

# Recommended Path

```text
Python
   ↓
SQL
   ↓
Pandas
   ↓
PySpark
   ↓
Airflow
   ↓
Kafka
   ↓
Cloud
```

---

# Important Advice

## DO NOT ONLY READ.

For every topic:

1. Write code yourself
2. Modify examples
3. Break the code intentionally
4. Fix errors
5. Build mini projects

---

# Best Way to Learn Fast

```text
Learn Concept
    ↓
Write Code
    ↓
Practice
    ↓
Build Project
    ↓
Teach Someone
```

---

# Final Goal

You should become capable of:

* Writing clean Python code
* Solving coding problems
* Building real projects
* Learning advanced technologies easily
* Cracking interviews confidently

---

# Recommended Next Topics

After mastering this:

* Pandas
* NumPy
* SQL
* PySpark
* APIs
* Airflow
* FastAPI
* Docker
* Cloud

---

Happy Learning 🚀
