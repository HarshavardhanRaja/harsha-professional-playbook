"""
"""
Connect to API to get logs 



"""

# # Task 1: Connect to the server API and dump the logs in a file 
# df = spark.real_connect_to_api(connection_details=connection_details_dict)
# df.load_to_s3("folder_path", "file_prefix")

# # Task 2: Read the files from the path do aggregations and shouw the results
# df = spark.read_parquet("file_path").(group_by('colum_name'))
# final_df = df.show() 


"""

You are given a list of logs:

 

logs = [
    "2024-01-01 ERROR Database failure",
    "2024-01-01 INFO Service started",
    "2024-01-02 ERROR Timeout occurred",
    "2024-01-02 ERROR Database failure"
]

 

Task:

Count occurrences of each ERROR message
"""


# def count_error_occurances(logs):
#   error_type = {}
#   for log in logs:
#     if "ERROR" in log:
#       current_error_type = log[16:]
#       if current_error_type in error_type.keys():
#         error_type[current_error_type] = error_type.get(current_error_type) + 1
#       else:
#         error_type[current_error_type] = 1
#   return error_type

# print(count_error_occurances(logs))





  





"""



"""
# You are reviewing the following code:
def get_even_numbers(nums):
    result = []
    for i in range(len(nums)):
        if nums[i] % 2 == 0:
            result.append(nums[i])
    return result
How to make this more pytonic and optimise it further



If dataset is HUGE and we want lazy evaluation:

def get_even_numbers(nums):
    for num in nums:
        if num % 2 == 0:
            yield num

OR

def get_even_numbers(nums):
    return (num for num in nums if num % 2 == 0)

"""

"""
nums = [1, 2, 3]
def sample_func(nums):
  print(nums)

there is a list called nums right after passsing it to a function and accessing it inside the function the value changed how is the possible?

# Question:
# nums = [1, 2, 3]
#
# def sample_func(nums):
#     print(nums)
#
# After passing the list to a function, why can changes inside the function
# affect the original list?


# Answer:

# In Python, variables do not store actual objects directly.
# They store REFERENCES to objects in memory.

# Example:
nums = [1, 2, 3]

# Here:
# nums ---> [1, 2, 3]

# When we pass nums to a function:

def sample_func(nums):
    nums.append(4)

sample_func(nums)

print(nums)

# Output:
# [1, 2, 3, 4]


# Explanation:
# Python passes the REFERENCE of the list to the function,
# not a separate copy of the list.

# Both the original variable and the function parameter
# point to the SAME list object in memory.

# So operations like:
# - append()
# - sort()
# - remove()
# - item assignment
#
# modify the SAME object,
# which changes the original list as well.


# --------------------------------------------------
# Important Concept: Mutable vs Immutable
# --------------------------------------------------

# Lists are MUTABLE:
# They can be changed after creation.

# Mutable types:
# - list
# - dict
# - set

# Immutable types:
# - int
# - str
# - tuple


# --------------------------------------------------
# Difference Between Mutation and Reassignment
# --------------------------------------------------

# 1. Mutation (affects original object)

nums = [1, 2, 3]

def mutate_list(nums):
    nums.append(4)

mutate_list(nums)

print(nums)

# Output:
# [1, 2, 3, 4]

# Reason:
# append() modifies the same list object.


# --------------------------------------------------
# 2. Reassignment (does NOT affect original)
# --------------------------------------------------

nums = [1, 2, 3]

def reassign_list(nums):
    nums = [10, 20]

reassign_list(nums)

print(nums)

# Output:
# [1, 2, 3]

# Reason:
# nums = [10, 20]
# creates a NEW local object inside the function.
# The original variable still points to old list.


# --------------------------------------------------
# Important Interview Answer
# --------------------------------------------------

# "Python uses pass-by-object-reference (or pass-by-sharing).
# When a mutable object like a list is passed to a function,
# both variables reference the same object in memory.
# Mutating the object affects the original,
# while reassignment creates a new local reference."


# --------------------------------------------------
# How To Avoid Changing Original List
# --------------------------------------------------

nums = [1, 2, 3]

def safe_function(nums):
    nums = nums.copy()   # create copy
    nums.append(4)
    return nums

print(nums)

# Output:
# [1, 2, 3]

# Original list remains unchanged.

"""


"""
logs = [
    "2024-01-01 ERROR Database failure",
    "2024-01-01 INFO Service started",
    "2024-01-02 ERROR Timeout occurred",
    "2024-01-02 ERROR Database failure"
]

he want an output count of error types like, 
{
"Database failure": 2,
"Timeout occurred": 1
}

logs = [
    "2024-01-01 ERROR Database failure",
    "2024-01-01 INFO Service started",
    "2024-01-02 ERROR Timeout occurred",
    "2024-01-02 ERROR Database failure"
]

def count_error_types(logs):

    error_counts = {}

    for log in logs:

        # Split only first 2 spaces
        parts = log.split(" ", 2)

        # parts example:
        # ['2024-01-01', 'ERROR', 'Database failure']

        log_level = parts[1]

        # Process only ERROR logs
        if log_level == "ERROR":

            error_message = parts[2]

            # Increment count
            error_counts[error_message] = (
                error_counts.get(error_message, 0) + 1
            )

    return error_counts


print(count_error_types(logs))


# Output:
# {
#   'Database failure': 2,
#   'Timeout occurred': 1
# }



# Step 1:
# Split log into:
# - date
# - log level
# - message

parts = log.split(" ", 2)

# Why split(..., 2)?
# Because error message itself may contain spaces.

# Example:
# "2024-01-01 ERROR Database failure"

# becomes:
# ['2024-01-01', 'ERROR', 'Database failure']


# Step 2:
# Check if log level is ERROR

if log_level == "ERROR":


# Step 3:
# Count occurrences using dictionary

error_counts[error_message] = (
    error_counts.get(error_message, 0) + 1
)

# .get(key, 0)
# returns:
# existing count OR 0 if key not present

from collections import Counter

def count_error_types(logs):

    counter = Counter()

    for log in logs:

        date, level, message = log.split(" ", 2)

        if level == "ERROR":
            counter[message] += 1

    return dict(counter)
"""
