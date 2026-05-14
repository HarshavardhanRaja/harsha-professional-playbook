"""


input:
records = [
    {"id": 1, "value": "A"},
    {"id": 2, "value": "B"},
    {"id": 1, "value": "A"},
    {"id": 3, "value": "C"},
    {"id": 2, "value": "B"},
    
]
output:
[
    {"id": 1, "value": "A"},
    {"id": 2, "value": "B"},
    {"id": 3, "value": "C"},
]


"""