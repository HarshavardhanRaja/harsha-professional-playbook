# Day 001 — Repository Setup

Status:

[✓] PySpark learning repository initialized
[✓] Standard folder structure created
[✓] ChatGPT learning notes structure created

Folder Philosophy:

This repository is intended to become:

1. PySpark learning hub
2. Interview preparation guide
3. Portfolio project collection
4. Freelancing showcase
5. Public knowledge base

Important Lesson:

macOS does not include `tree` by default.

Alternative:

find pyspark -type d | sort

Next Step:

Verify local environment:

- Python
- Java
- pip


## Environment Check

Python:

3.9.6

Java:

OpenJDK 17

pip:

21.2.4

Observation:

Java is compatible with Spark.

Python version may require upgrade later for newer PySpark versions.

Next:

Check Homebrew-managed Python installations.

## Python Upgrade

Installed:

python@3.11 via Homebrew

Reason:

Avoid dependency issues with modern PySpark versions and isolate from macOS system Python.


## Virtual Environment

Why use virtual environments?

Without venv:

Project A installs PySpark 3.5

Project B installs PySpark 4.0

Both conflict.

With venv:

Each project has isolated dependencies.

Think:

venv ≈ Docker container for Python packages


## Python Session Memory

Observation:

Closing Python removes variables.

Example:

```python
spark
df
explicit_df
```

will disappear after exiting REPL.

Error:

```txt
NameError:
name 'spark' is not defined
```

Reason:

Variable exists only within current Python session.

Analogy:

Python REPL ≈ temporary whiteboard

Close room → whiteboard erased