"""

Topic 1: Sliding Window

“Find the maximum sum of any subarray of size k.”

arr = [2,1,5,1,3,2]
k = 3
[2,1,5] = 8
[1,5,1] = 7
[5,1,3] = 9
[1,3,2] = 6
Answer: 9

Brute Force Approach:
Step 1 Take first 3 elements
Step 2 Calculate sum
Step 3 Move to next subarray
Step 4 Recalculate entire sum again

Problem With This?
We are recalculating overlapping elements repeatedly.

[2,1,5]
[1,5,1]
Notice:
1,5 already calculated
but recalculated again
Wasteful.

Time Complexity
Outer loop: O(n)
Inner loop: O(k)
Total: O(n*k)
Can become slow for large input.


Sliding Window Optimization: 

Core idea:
Instead of recalculating entire window:
remove old element
add new element

Time Complexity
O(n)

"""


def brute_force_approach(arr, k):
    max_sum = 0
    for i in range(len(arr) - k + 1):
        current_sum = 0
        for j in range(i, i + k):
            current_sum += arr[j]
        max_sum = max(max_sum, current_sum)
    return max_sum


def sliding_window_approach(arr, k):

    window_sum = sum(arr[:k])
    max_sum = window_sum

    for right in range(k, len(arr)):

        window_sum += arr[right]
        window_sum -= arr[right-k]

        max_sum = max(max_sum, window_sum)

    return max_sum


"""
IMPORTANT INTERVIEW UNDERSTANDING

Sliding window works BEST when:
dealing with contiguous subarrays/substrings
window moves continuously
repeated recalculation can be avoided

"""



"""
Practice Problem1: 

Given an array of positive integers and integer k,
find the maximum sum of any contiguous subarray of size k.

arr = [4,2,1,7,8,1,2,8,1,0]
k = 3
16
"""

arr = [4,2,1,7,8,1,2,8,1,0]
k = 3
print(brute_force_approach(arr, k))
print(sliding_window_approach(arr, k))


# Practice Problem2:
"""

Problem 1 — Fixed Sliding Window
Maximum Sum Subarray of Size K
Given an integer array nums and an integer k,
return the maximum sum of any contiguous subarray of size k.

Example 1
nums = [2,1,5,1,3,2]
k = 3
Output: 9
Explanation: [5,1,3] = 9

Example 2
nums = [1,9,-1,-2,7,3,-1,2]
k = 4
Output: 13
"""

    