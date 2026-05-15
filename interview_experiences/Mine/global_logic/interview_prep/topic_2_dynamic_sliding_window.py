"""

Fixed Window:
Size always fixed.
Example: window size = k


Dynamic Window:
Window size changes dynamically.
We,
expand window
shrink window
maintain some condition
This is where interviews become interesting.
"""

"""
Most Famous Dynamic Window Problem:
Longest Substring Without Repeating Characters

Problem
Given string: s = "abcabcbb"
Find length of longest substring without repeating characters.

Answer: "abc"
Length: 3


Brute force:
generate all substrings
check duplicates

Complexity becomes: O(n²)
or worse.
Not scalable.

"""

def brute_force_longest_substring(s):
    max_length = 0
    for i in range(len(s)):
        seen = set()
        current_length = 0
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
            current_length += 1
        max_length = max(max_length, current_length)
    return max_length


"""
Key Insight
We need:
contiguous substring
duplicates constraint

This screams: Sliding Window

Core Dynamic Window Idea
We maintain, 
[left .... right]
Window expands using right.
If condition breaks: shrink using left


Visual Understanding

String: "abcabcbb"
Step 1 Window: "a" Unique.Expand.
Step 2 Window: "ab" Unique. Expand.
Step 3 Window: "abc" Unique. Expand.
Step 4 Window: "abca" Problem: duplicate "a".
Now we SHRINK from left.
Shrinking Process
Remove leftmost "a".
Window becomes: "bca" Now valid again. Continue expanding.


THIS IS THE CORE PATTERN: 
Expand while valid
Shrink when invalid
That’s dynamic sliding window.

"""

def dynamic_sliding_window_longest_substring(s):

    char_set = set()

    left = 0
    max_length = 0

    for right in range(len(s)):

        while s[right] in char_set:

            char_set.remove(s[left])
            left += 1

        char_set.add(s[right])

        max_length = max(
            max_length,
            right - left + 1
        )

    return max_length


"""
Dynamic Sliding Window Template
MEMORIZE THIS MENTALLY.

left = 0
for right in range(len(data)):
    # expand window
    while invalid_condition:

        # shrink window
        left += 1

    # update answer

This template solves MANY problems.
"""