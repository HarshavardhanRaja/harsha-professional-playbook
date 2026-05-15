"""
Topic: Heap / Priority Queue OR LRU Cache

First Understand The Problem Heap Solves
Suppose you have numbers: [10, 4, 15, 20, 0]
And interviewer asks:

“Find the smallest element efficiently.”
Easy: 0

But what if:
numbers keep coming continuously
you repeatedly need smallest/largest element
data is huge
Sorting every time becomes expensive.
That’s where Heap helps.


What Is a Heap?
Heap is a special tree-based data structure.

Main property:
Min Heap
Smallest element always at top/root.

        0
      /   \
     4     15
    / \
   20 10

Top element: 0
always accessible quickly.


Max Heap
Largest element always at top.

       20
      /  \
    15    10
   / \
  4   0

Top: 20



Why Is Heap Powerful?

Heap gives:

Operation	Complexity
Insert	O(log n)
Remove top	O(log n)
Peek top	O(1)
Very efficient.


Real-World Backend Uses
1. Task Scheduling Highest priority task first.

2. Top K Problems
Find:

top 10 users
top trending hashtags
largest transactions

3. Streaming Data
Continuously incoming values.

4. Load Balancers
Choose least loaded server.

"""

"""
Python uses: heapq

IMPORTANT:
Python heap is: Min Heap by default


"""

import heapq
nums = [10,4,15,20,0]
heapq.heapify(nums)
print(nums)
print(heapq.heappop(nums))


"""
Why Not Sorting?

Interview IMPORTANT.

Suppose:

n = 1 million

Sorting:

O(n log n)

Heap top retrieval:

O(log n)

Much better for repeated operations.
"""


"""
MOST IMPORTANT INTERVIEW PATTERN
Top K Elements
This is HEAP’S most common interview use case.

Most Important Interview Insight

Heap is useful when:
repeatedly need min/max
need top-k
streaming input
dynamic ranking



1. Kth Largest Element

Classic heap problem.

2. Top K Frequent Elements

Use:

hashmap frequency
heap
3. Merge K Sorted Lists

Very famous.

4. Median From Data Stream

Hard but common.

Uses:

min heap
max heap together
5. Task Scheduler

Backend-oriented.




IMPORTANT INTERVIEW QUESTION
Q: Why use heap instead of sorting?

Strong answer:

“Heap is more efficient when we only need top-k elements or repeated min/max operations because it avoids sorting the entire dataset.”

Excellent backend answer.

Complexity Table (IMPORTANT)
Operation	Heap
Insert	O(log n)
Remove Top	O(log n)
Peek Top	O(1)
Heapify	O(n)
"""
