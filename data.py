import time
import json
import unicodedata
from collections import deque, defaultdict

from composites import RsetSL, Rsum, RrevIN, REsetSL, REEsetSL, REEEsetSL, BSL

start_time = time.time()


operations = {
    0: RsetSL,
    1: Rsum,
    2: RrevIN,
    3: REsetSL,
    4: REEsetSL,
    5: REEEsetSL,
    6: BSL,
}

#

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

keys = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

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
        key: [v.__name__ for v in value.functions]
        for key, value in operations.items()
    },
    "paths": [],
}


charmap = {
    "000000": "A",
    "000001": "B",
    "000010": "C",
    "000011": "D",
    "000100": "E",
    "000101": "F",
    "000110": "G",
    "000111": "H",
    "001000": "I",
    "001001": "J",
    "001010": "K",
    "001011": "L",
    "001100": "M",
    "001101": "N",
    "001110": "O",
    "001111": "P",
    "010000": "Q",
    "010001": "R",
    "010010": "S",
    "010011": "T",
    "010100": "U",
    "010101": "V",
    "010110": "W",
    "010111": "X",
    "011000": "Y",
    "011001": "Z",
    "011010": "a",
    "011011": "b",
    "011100": "c",
    "011101": "d",
    "011110": "e",
    "011111": "f",
    "100000": "g",
    "100001": "h",
    "100010": "i",
    "100011": "j",
    "100100": "k",
    "100101": "l",
    "100110": "m",
    "100111": "n",
    "101000": "o",
    "101001": "p",
    "101010": "q",
    "101011": "r",
    "101100": "s",
    "101101": "t",
    "101110": "u",
    "101111": "v",
    "110000": "w",
    "110001": "x",
    "110010": "y",
    "110011": "z",
    "110100": "0",
    "110101": "1",
    "110110": "2",
    "110111": "3",
    "111000": "4",
    "111001": "5",
    "111010": "6",
    "111011": "7",
    "111100": "8",
    "111101": "9",
    "111110": "+",
    "111111": "/",
}

semicharmap = {
    0: "000",
    1: "001",
    2: "010",
    3: "011",
    4: "100",
    5: "101",
    6: "110",
}

def output_json():
    running = False
    run_flag = False

    for i in range(max_value):

        if i in operation_paths and unicodedata.name(chr(int(i)), False):
            final_path = ikTranslator[operation_paths[i][0]]
            final_path += "".join([str(x) for x in operation_paths[i][1:]])
            result_dict["paths"].append(final_path)

            run_flag = False
            running = False
        else:
            run_flag = True

        if run_flag:
            if not running:
                result_dict["paths"].append(1)
                running = True
            else:
                result_dict["paths"][-1] += 1

    # Compression run
    paths = ""

    for path in result_dict["paths"]:
        if type(path) is int:
            paths += f",{path}"
        else:
            binarypath = path[0]

            if len(path) <= 1:
                paths += f",{binarypath}"
                continue

            # for each pair of characters
            for i in range(1, len(path) - 1, 2):
                left = semicharmap[int(path[i])]
                right = semicharmap[int(path[i + 1])]
                bc = left + right
                binarypath += charmap[bc]
            
            if len(binarypath) % 2 != 0:
                left = semicharmap[int(path[-1])]
                bc = left + "111"
                binarypath += charmap[bc]

            paths += f",{binarypath}"


    result_dict["paths"] = paths[1:]

    with open("output.json", mode="w", encoding="utf-8") as f:
        json.dump(result_dict, f, separators=(",", ":"))


output_json()


def output_counter():
    counter = {key: 0 for key in operations}

    for v in sorted(possible_values):
        if v > max_value:
            continue

        char = chr(int(v))
        if unicodedata.name(char, False):
            for x in operation_paths[v][1:]:
                counter[x] += 1

    print(counter)


output_counter()

print("Time taken: ", time.time() - start_time)
