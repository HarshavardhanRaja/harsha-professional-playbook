# Python Notes — 01 Variables Basics 🚀

> 📘 Beginner → Interview Level Python Notes
> Topic: Variables Fundamentals

---

# 🎯 Learning Outcomes

After completing this file, you should be able to:

✅ Understand what variables are internally
✅ Explain variable assignment clearly
✅ Understand Python references
✅ Explain dynamic typing
✅ Avoid common beginner mistakes
✅ Answer interview questions confidently

---

# 📚 Table of Contents

* [1. What is a Variable?](#1-what-is-a-variable)
* [2. Why Variables are Needed](#2-why-variables-are-needed)
* [3. Variable Naming Rules](#3-variable-naming-rules)
* [4. Variable Assignment](#4-variable-assignment)
* [5. Dynamic Typing](#5-dynamic-typing)
* [6. Variable References Internally](#6-variable-references-internally)
* [7. Multiple Assignment](#7-multiple-assignment)
* [8. Common Beginner Mistakes](#8-common-beginner-mistakes)
* [9. Best Practices](#9-best-practices)
* [10. Real-World Examples](#10-real-world-examples)
* [11. Important Interview Questions](#11-important-interview-questions)
* [12. Tricky Interview Questions](#12-tricky-interview-questions)
* [13. Practice Questions](#13-practice-questions)
* [14. Revision Summary](#14-revision-summary)

---

# 🧠 How to Use This File

For every section:

1. Read explanation carefully
2. Run all code examples
3. Predict output before running
4. Modify examples yourself
5. Revise interview questions

---

# 1. What is a Variable?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A variable is a name used to store data.

Example:

```python id="wlf28u"
name = "Harsha"
```

Here:

| Part       | Meaning       |
| ---------- | ------------- |
| `name`     | Variable name |
| `"Harsha"` | Stored value  |

---

# Real-Life Analogy

Think of a variable like a labeled box.

```text id="upg0ep"
Box Label  → name
Inside Box → Harsha
```

Whenever Python sees `name`, it retrieves the stored value.

---

# Why Variables Matter

Without variables:

```python id="50b2e3"
print("Harsha")
print("Harsha")
print("Harsha")
```

With variables:

```python id="9faj6t"
name = "Harsha"

print(name)
print(name)
print(name)
```

Benefits:

✅ Reusability
✅ Better readability
✅ Easier debugging
✅ Easier updates

---

# 2. Why Variables are Needed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Variables help programs become dynamic.

Example:

```python id="k6lsk9"
price = 100
quantity = 5

total = price * quantity

print(total)
```

Output:

```python id="r44q0w"
500
```

Instead of hardcoding values everywhere, variables make programs flexible.

---

# Real-World Example

Ecommerce Application:

```python id="ln4z8h"
product_name = "iPhone"
price = 1000
stock_available = True
```

Banking Application:

```python id="0glp7d"
account_balance = 50000
is_kyc_completed = False
```

---

# 3. Variable Naming Rules

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ✅ Valid Variable Names

```python id="lxt0f0"
name = "Harsha"
age = 25
employee_salary = 50000
_private = "Python"
```

---

# ❌ Invalid Variable Names

```python id="i6yzl9"
2name = "Wrong"
```

Reason:
Variable cannot start with a number.

---

```python id="nn67tb"
first-name = "Wrong"
```

Reason:
`-` is treated as subtraction operator.

---

# Rules Summary

| Rule                       | Allowed? |
| -------------------------- | -------- |
| Start with letter          | ✅        |
| Start with underscore      | ✅        |
| Start with number          | ❌        |
| Spaces allowed             | ❌        |
| Special characters allowed | ❌        |

---

# Python is Case Sensitive

```python id="u0djlwm"
name = "Harsha"
Name = "Python"
```

These are DIFFERENT variables.

---

# Recommended Naming Style

Use `snake_case`.

✅ Good:

```python id="x4u09f"
employee_salary = 50000
```

❌ Bad:

```python id="d7jotq"
EmployeeSalary = 50000
empsal = 50000
```

---

# 4. Variable Assignment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Basic assignment:

```python id="4y2a5g"
x = 10
```

What Python does internally:

```text id="o0emg6"
1. Creates object 10 in memory
2. Creates variable x
3. Makes x point to object 10
```

---

# Reassignment

```python id="bvx0ml"
x = 10
x = 20
```

Now `x` points to a new object.

---

# Important Concept

Python variables DO NOT directly store values.

They store REFERENCES to objects.

This is VERY IMPORTANT for interviews.

---

# Visual Explanation

```text id="l3u4wp"
x ───► 10
```

After reassignment:

```text id="7td0r6"
x ───► 20
```

---

# 5. Dynamic Typing

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Python is dynamically typed.

Meaning:
You DO NOT declare datatype manually.

---

# Example

```python id="fhsm3v"
x = 10
x = "Harsha"
x = True
```

Same variable stores different types.

---

# Why?

Because Python decides datatype during runtime.

---

# Comparison with Java

Java:

```java id="s57blf"
int x = 10;
```

Python:

```python id="zjlwmn"
x = 10
```

Python is simpler and faster to write.

---

# Benefits of Dynamic Typing

✅ Faster development
✅ Less code
✅ Flexible programming

---

# Disadvantages

❌ Runtime errors possible
❌ Harder debugging in large systems

---

# 6. Variable References Internally

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERY IMPORTANT concept.

Variables store REFERENCES, not actual values.

---

# Example

```python id="1m1bcz"
x = [1, 2]
y = x
```

Visual:

```text id="okp2az"
x ──► [1,2]
y ──► [1,2]
```

Both variables point to SAME object.

---

# Proof

```python id="m2r70y"
x = [1,2]
y = x

print(id(x))
print(id(y))
```

IDs will usually be same.

---

# What is id()?

`id()` returns memory identity of object.

---

# Important Example

```python id="mtm1yx"
x = [1,2]
y = x

y.append(3)

print(x)
```

Output:

```python id="3evr4z"
[1,2,3]
```

Why?

Because both refer same object.

---

# Important Interview Point

Assignment copies references, NOT objects.

---

# 7. Multiple Assignment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Assign Multiple Variables

```python id="p7i6tr"
x, y, z = 1, 2, 3
```

---

# Same Value Assignment

```python id="f13fzh"
a = b = c = 100
```

---

# Variable Swapping

Pythonic way:

```python id="88t63f"
x = 10
y = 20

x, y = y, x
```

No temporary variable needed.

---

# Output

```python id="o65m0j"
x = 20
y = 10
```

---

# 8. Common Beginner Mistakes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Mistake 1 — Confusing `=` and `==`

Wrong:

```python id="fh0c5c"
if x = 10:
```

Correct:

```python id="8qhm5q"
if x == 10:
```

---

# Mistake 2 — Using Reserved Keywords

Wrong:

```python id="3nnlc7"
class = 10
```

`class` is reserved keyword.

---

# Mistake 3 — Overwriting Built-ins

Bad:

```python id="ubdbhu"
list = [1,2,3]
```

Now built-in `list()` breaks.

---

# Mistake 4 — Shared References

```python id="yb5dmb"
x = y = []
```

Both point to SAME list.

Dangerous in real projects.

---

# 9. Best Practices

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Use Meaningful Names

✅ Good:

```python id="k2i6ec"
employee_salary = 50000
```

❌ Bad:

```python id="4lnkzv"
x = 50000
```

---

# Use snake_case

```python id="lfjvvb"
customer_name
product_price
```

---

# Keep Names Short but Clear

✅ Good:

```python id="hll18u"
user_age
```

❌ Bad:

```python id="4e7n2g"
ua
```

---

# 10. Real-World Examples

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Example 1 — Student System

```python id="kv9z38"
student_name = "Harsha"
student_age = 25
student_marks = 90
```

---

# Example 2 — Ecommerce

```python id="b6kc54"
product_name = "Laptop"
price = 50000
in_stock = True
```

---

# Example 3 — Banking

```python id="bghgg3"
account_balance = 100000
is_loan_approved = False
```

---

# 11. Important Interview Questions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Q1. What is a variable in Python?

A variable is a reference name pointing to an object stored in memory.

---

# Q2. Does variable store actual value?

No.

Variables store references to objects.

---

# Q3. Is Python statically typed or dynamically typed?

Python is dynamically typed.

Datatype determined during runtime.

---

# Q4. What is dynamic typing?

Same variable can store different datatypes during execution.

---

# Q5. What does id() do?

Returns memory identity of object.

---

# Q6. What is difference between `=` and `==`?

| Operator | Meaning    |
| -------- | ---------- |
| `=`      | Assignment |
| `==`     | Comparison |

---

# Q7. Why is Python case sensitive?

Because lowercase and uppercase identifiers are treated differently internally.

---

# 12. Tricky Interview Questions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Q1

```python id="1bx9nq"
x = [1,2]
y = x

y.append(3)

print(x)
```

Output?

```python id="z88yeh"
[1,2,3]
```

Reason:
Both reference same object.

---

# Q2

```python id="rzrhtm"
x = 10
y = 10

print(x is y)
```

Usually:

```python id="88g96o"
True
```

Reason:
Python caches small integers.

---

# Q3

```python id="8fzf3k"
x = 1000
y = 1000

print(x is y)
```

May be False.

Reason:
Large integers may not be cached.

---

# Q4

```python id="7q4g2h"
x = y = []

x.append(1)

print(y)
```

Output:

```python id="25h9kc"
[1]
```

Reason:
Both reference same list.

VERY IMPORTANT interview question.

---

# 13. Practice Questions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Beginner

1. Create variables for employee details.
2. Create variables for ecommerce application.
3. Swap two variables.
4. Print memory IDs using `id()`.

---

# Intermediate

1. Experiment with shared references.
2. Explore integer caching.
3. Create examples using dynamic typing.

---

# Advanced

1. Explain Python memory model.
2. Explain variable references internally.
3. Explain why assignment copies references.

---

# 14. Revision Summary

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```text id="0tw1s0"
Variable → Reference to object
Python → Dynamically typed
Variables → Store references
id() → Memory identity
= → Assignment
== → Comparison
snake_case → Recommended naming style
```

---

# ✅ Next Recommended Topic

👉 `02_data_types.md`

Because understanding datatypes deeply is the foundation for:

* operators
* loops
* functions
* OOP
* PySpark
* interview coding

---

Happy Learning 🚀
