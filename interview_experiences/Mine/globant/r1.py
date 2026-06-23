# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
"""

able_A 	Table_B
1		1
1		NULL
NULL		NULL





Inner Join: 3
Left Join: 2
Right Join: 1
Full Outer Join: 3
Cartesian Product: 9


"""


"""
Employees

Emp_ID Emp_Name Month Monthly_Salary
1	ABC	   1     10000
1	ABC	   2     10000
1	ABC	   3     10000
1	ABC	   4     10000
2	XYZ	   1     15000
2	XYZ	   2     15000
2	XYZ	   3     15000
2	XYZ	   4     15000

Given an Employees table which contains monthly salaries paid to employees during one calendar year,
calculate the cumulative salary paid to the employees till each month


Expected Output -

Emp_ID Emp_Name Month Monthly_Salary Cum_Salary
1	ABC	   1     10000		10000
1	ABC	   2     10000		20000
1	ABC	   3     10000		30000
1	ABC	   4     10000		40000
2	XYZ	   1     15000		15000
2	XYZ	   2     15000		30000
2	XYZ	   3     15000		45000
2	XYZ	   4     15000		60000



"""



# tuple_a = (1, 2, 3, -1, -2, -3)
# list_b = [ele*ele for ele in tuple_a]
# print(set(list_b))

"""
Given an array 'arr' and a target, check if there exists any pair of elements (arr[i], arr[j]) such that their sum is equal to the target. Return a list containing all such pairs.

Input: arr = [10, 60, 20, 35, 50, 10], target =70
Output: [(20,50), (10,60)]
"""
input_arr = [10, 60, 20, 35, 50, 10]
target = 70
def find_pair(arr, target):
    target_pairs = []
    processed_elemnts = []
    
    for element in arr:
        req_pair = target - element
        arr.remove(element)
        if element not in processed_elemnts and req_pair not in processed_elemnts:
            if req_pair in arr:
                target_pairs.append((element, req_pair))
                processed_elemnts.append(element)
    return target_pairs
            
print(find_pair(input_arr, target))

    


