import time
import json
import random
import unicodedata
import math
from collections import deque, defaultdict

from composites import RsetSL, Rsum, RrevIN

start_time = time.time()


operations = {
    0: RsetSL,
    1: Rsum,
    2: RrevIN,
    # 3: (str, len), # not used
    # 4: (range, enumerate, set, str, len),
}

operation_lengths = {}

for operation in operations:
    operation_lengths[operation] = operations[operation].get_string_length()

possible_values = set()
operation_paths = {}
operation_path_lengths = defaultdict(int)

max_value = 1_114_111
max_depth = 24  # 24 is good

visited = {}

queue = deque()


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
    queue.append((i, max_depth, [i], len(candidates[i])))

while queue:
    value, depth, path, path_length = queue.popleft()

    if depth == 0 or value > max_value:
        continue
    # if depth == 0 or value > max_value * max_value:
    #     continue

    if value in visited and visited[value] >= depth:
        continue
    visited[value] = depth

    possible_values.add(value)

    if (
        value not in operation_paths
        or path_length < operation_path_lengths[value]
    ):
        operation_path_lengths[value] = path_length
        operation_paths[value] = path[:]

    for ops in range(len(operations)):
        new_value = value
        new_path = path[:]

        if not operations[ops].guard(new_value):
            continue

        new_value = operations[ops].simulate(new_value)

        new_path.append(ops)
        new_path_length = path_length + operation_lengths[ops]
        queue.append((new_value, depth - 1, new_path, new_path_length))


keys = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"

if len(keys) < len(candidates.keys()):
    print("Not enough keys!")

ikTranslator = {}
i = 0
for k in sorted(candidates.keys()):
    ikTranslator[k] = keys[i]
    i += 1


result_dict = {
    "initialKeys": {
        ikTranslator[key]: value for key, value in candidates.items()
    },
    "operations": {
        key: [v.__name__ for v in value.functions] for key, value in operations.items()
    },
    "paths": {},
}

# for v in sorted(possible_values):
#     char = chr(int(v))
#     if unicodedata.name(char, False):
#         final_path = ikTranslator[operation_paths[v][0]]
#         final_path += "".join([str(x) for x in operation_paths[v][1:]])
#         result_dict["paths"][v] = final_path


# with open("output.json", mode="w", encoding="utf-8") as f:
#     json.dump(result_dict, f)

counter = {0: 0, 1: 0, 2: 0, 3: 0}

with open("testoutput.txt", mode="w", encoding="utf-8") as f:
    for v in sorted(possible_values):
        if v > max_value:
            continue

        char = chr(int(v))
        if unicodedata.name(char, False):
            for x in operation_paths[v][1:]:
                counter[x] += 1

print(counter)


print("Time taken: ", time.time() - start_time)
