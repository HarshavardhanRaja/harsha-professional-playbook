"""
Problem Statement
You are given a list of event names. Write a function that counts how many times each event occurred and returns the result.

 

Example 1
Input ["login", "logout", "login", "purchase", "login", "logout"]

Output
login -> 3
logout -> 2
purchase -> 1

 
Example 2

Input ["A", "B", "A", "C", "B", "A"]

Output

 

A -> 3

 

B -> 2

 

C -> 1

 

 

 

Clarifications (If Candidate Asks)

 

● Event names are strings.

 

● The input list can be empty.

 

● Return the result as a Map<String, Integer> (or equivalent in the candidate's

 

language).

 

 

 

● Event names are case-sensitive unless specified otherwise.


"""

test_case_1 = ["login", "logout", "login", "purchase", "login", "logout"]
test_case_2 = ["A", "B", "A", "C", "B", "A"] 


def count_events(input_list):
    final_dict = {}
    for each_event in input_list:
        if each_event in final_dict:
            final_dict[each_event] = final_dict[each_event] + 1
        else:
            final_dict[each_event] = 1

    return final_dict

print(count_events(test_case_2))

