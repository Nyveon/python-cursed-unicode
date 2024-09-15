import time
import json
import unicodedata
from collections import deque

start_time = time.time()

operations = [
    (range, set, str, len),
    (range, sum),
    (range, reversed, iter, next),
    # (range, enumerate, set, str, len),
]

possible_values = set()
operation_paths = {}

max_value = 129782
max_depth = 8 # 24 is good

visited = {}

queue = deque()

def calculate_list_string_length(N):
    N = N - 1
    commas_and_spaces = max(0, (N) * 2)
    parentheses = 2

    digits = 0
    start = 1
    num_digits = 1

    while start <= N:
        end = min(N, 10**num_digits - 1)
        count = end - start + 1
        digits += count * num_digits
        start *= 10
        num_digits += 1

    digits += 1  # (0)

    total_length = commas_and_spaces + parentheses + digits
    return total_length


def calculate_range_sum(N):
    N -= 1
    return (N * (N + 1)) // 2

candidates = {
    78: ["ord(min(str(print())))"],
    111: ["ord(max(str(print())))"],
    4: [
        "len(str(IndentationError()))",
        "len(str(SyntaxError()))",
        "len(str(TabError()))",
        "len(str(print()))",
    ],
    32: ["ord(min(str(type(zip()))))"],
    116: ["ord(max(str(type(vars()))))"],
    26: ["len(str(type(IndentationError())))"],
    121: ["ord(max(str(type(property()))))"],
    21: ["len(str(type(SyntaxError())))"],
    115: ["ord(max(str(type(bool()))))"],
    18: [
        "len(str(type(TabError())))",
        "len(str(type(print())))",
        "len(str(type(property())))",
    ],
    70: ["ord(min(str(bool())))"],
    5: ["len(str(bool()))", "len(str(set()))"],
    14: [
        "len(str(type(bool())))",
        "len(str(bytearray()))",
        "len(str(type(dict())))",
        "len(str(type(dir())))",
        "len(str(type(globals())))",
        "len(str(type(list())))",
        "len(str(type(locals())))",
        "len(str(type(vars())))",
    ],
    39: ["ord(min(str(bytes())))", "len(str(property()))"],
    19: ["len(str(type(bytearray())))", "len(str(type(frozenset())))"],
    98: ["ord(max(str(bytes())))"],
    3: ["len(str(bytes()))", "len(str(float()))"],
    15: [
        "len(str(type(bytes())))",
        "len(str(type(float())))",
        "len(str(type(tuple())))",
    ],
    48: ["ord(max(str(int())))"],
    106: ["ord(max(str(complex())))"],
    2: [
        "len(str(complex()))",
        "len(str(dict()))",
        "len(str(list()))",
        "len(str(tuple()))",
    ],
    120: ["ord(max(str(object())))"],
    17: ["len(str(type(complex())))"],
    123: ["ord(min(str(dict())))"],
    46: ["ord(min(str(float())))"],
    40: ["ord(min(str(tuple())))"],
    122: ["ord(max(str(type(zip()))))"],
    11: ["len(str(frozenset()))"],
    1: ["len(str(int()))"],
    13: [
        "len(str(type(int())))",
        "len(str(type(set())))",
        "len(str(type(zip())))",
    ],
    91: ["ord(min(str(list())))"],
    93: ["ord(max(str(list())))"],
    37: ["len(str(object()))"],
    16: ["len(str(type(object())))"],
    41: ["ord(max(str(tuple())))"],
    117: ["ord(max(str(type(tuple()))))"],
    34: ["len(str(zip()))"],
}

for k, v in candidates.items():
    candidates[k] = v[0]

for i in candidates.keys():
    if i == 44:
        continue
    queue.append((i, max_depth, [i]))

while queue:
    value, depth, path = queue.popleft()

    if depth == 0 or value > max_value:
        continue

    if value in visited and visited[value] >= depth:
        continue
    visited[value] = depth

    possible_values.add(value)

    if value not in operation_paths or len(path) < len(operation_paths[value]):
        operation_paths[value] = path[:]

    for ops in range(len(operations)):
        new_value = value
        new_path = path[:]

        if ops == 0:
            new_value = calculate_list_string_length(new_value)
            for op in operations[ops]:
                new_path.append(op.__name__)
        elif ops == 1:
            new_value = calculate_range_sum(new_value)
            for op in operations[ops]:
                new_path.append(op.__name__)
        elif ops == 2:
            if new_value == 0:
                continue

            new_value = new_value - 1
            for op in operations[ops]:
                new_path.append(op.__name__)
        else:
            print("here")
            for op in operations[ops]:
                try:
                    new_value = op(new_value)
                    new_path.append(op.__name__)
                except Exception as e:
                    print(e)
                    break

        queue.append((new_value, depth - 1, new_path))

result_dict = {
    "paths": {}
}

for v in sorted(possible_values):
    char = chr(int(v))
    if unicodedata.name(char, False):
        result_dict["paths"][v] = operation_paths[v]


with open("output.json", mode="w", encoding="utf-8") as f:
    json.dump(result_dict, f)
