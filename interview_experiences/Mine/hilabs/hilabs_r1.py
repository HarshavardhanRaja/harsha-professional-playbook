"""

You’re given a list of (timestamp, user_id, ip_address) tuples sorted by timestamp.
Implement a function to compute, for each subnet, the maximum number of unique users seen in last 1-hour sliding window.

#sample input
logs = [
    ("2023-05-20T14:00:00", "user1", "192.168.1.2"),
    ("2023-05-20T14:10:00", "user2", "192.168.1.5"),
    ("2023-05-20T14:30:00", "user3", "192.168.1.9"),
    ("2023-05-20T14:59:00", "user1", "192.168.1.2"),
    ("2023-05-20T15:05:00", "user4", "192.168.1.20"),
    ("2023-05-20T14:05:00", "user1", "10.0.0.1"),
    ("2023-05-20T14:20:00", "user2", "10.0.0.2"),
    ("2023-05-20T14:50:00", "user3", "10.0.0.3"),
]

#output
{
    '192.168.1': 3,
    '10.0.0': 3
}

def compute_max_users_subnet(logs):
    initial_start_index = 0
    initial_end_index = len(logs) - 1
    max_users_subnet = {}

    for index, entry in enumerate(logs):
        initial_start_index = index
        temp_subnet_users = {}

        for j, end_value in enumerate(range(index, len(entry))):
            time_diff = entry[starting_index][0] - entry[j][0]
            if time_diff == 60:
                initial_end_index = j
                break
        window = entry[initial_start_index:initial_end_index]

        for record in window:
            if record[2] in temp_subnet_users and record[1] not in temp_subnet_users[record[2]]:
               temp_subnet_users[record[2]] = temp_subnet_users[record[2]].append(record[1])
            else:
               temp_subnet_users[record[2]] = set(record[1])

        for key, value in temp_subnet_users:
            if key in max_users_subnet:
                if max_users_subnet[key] < len(value):
                   max_users_subnet[key] = len(value)



"""