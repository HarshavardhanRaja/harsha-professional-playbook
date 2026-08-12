"""
# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
"""

"""
Q: The Battle for Priority Plains
You’re a strategist preparing your army to take over Priority Plains, a vast battlefield divided into regions, each represented by a number. Spies have reported the frequency of enemy patrols in these regions, but you only have the resources to secure the k most critical regions where enemy activity is highest.
Your commander hands you a list of these regions (nums) and orders you to determine which k regions are the most frequently patrolled by the enemy.
For example:
If the intel says nums = [4,5,5,6,6,6] and k = 2, you conclude that regions 6 and 5 are the hotspots and report back [6,5] or [5,6].
If the patrol data is nums = [9,10,11,9,9] and k = 1, it’s obvious region 9 is the highest priority, so the output is [9].
Strategist, the fate of the Priority Plains depends on your calculations. Can you identify the regions to focus on?


test_case 1: 
nums = [4,5,5,6,6,6]
k = 2
result = [6,5] or [5,6].


nums = [9,10,11,9,9]
k = 1
result = [9]
"""



"""

# def calculate_priority_plain(nums, k):
#     priority_map = {}
#     for num in nums:
#         if num in priority_map:
#             priority_map[num] = priority_map[num] + 1
#         else:
#             priority_map[num] = 1

#     return_list = []
#     for i in range(k):
#         max_element = None
#         max_element_priority = 0
#         for each_element in priority_map:
#             if priority_map.get(each_element) > max_element_priority:
#                 max_element_priority = priority_map.get(each_element)
#                 max_element = each_element
#         return_list.append(max_element)
#         del priority_map[max_element]

#     return return_list
        


"""
nums = [9,10,11,9,9]
k = 1
result = [9]
map_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1]
frequncy_list = [[10, 11], [], [9]]
"""


def calculate_priority_plain(nums, k):
    priority_map = {}
    for num in nums:
        if num in priority_map:
            priority_map[num] = priority_map[num] + 1
        else:
            priority_map[num] = 1
    print(priority_map)
    
    frequency_list = [[] for each in nums]
    for each in priority_map:
        prior_update_list = frequency_list[priority_map.get(each)]
        prior_update_list.append(each)
        frequency_list[priority_map.get(each)] = prior_update_list
    print(frequency_list)

    return_list = []
    sorted_list = []
    for each_list in frequency_list:
        if each_list:
            for each_element in each_list:
                sorted_list.append(each_element)
    print(sorted_list)
    return sorted_list[:-k]
    
    # return_list = []
    # for i in range(k):
    #     max_element = None
    #     max_element_priority = 0
    #     for each_element in priority_map:
    #         if priority_map.get(each_element) > max_element_priority:
    #             max_element_priority = priority_map.get(each_element)
    #             max_element = each_element
    #     return_list.append(max_element)
    #     del priority_map[max_element]

    # return return_list

nums = [4,5,5,6,6,6]
k = 2

# nums = [9,10,11,9,9]
# k = 1

# nums = [4, 4, 5,5,6,6,6]
# k = 2

# nums = [1, 2, 3, 4, 5]
# k = 3

print(calculate_priority_plain(nums, k))




"""



