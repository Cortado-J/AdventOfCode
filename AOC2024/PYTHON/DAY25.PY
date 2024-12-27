#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
items = text.split('\n\n')
# #####
# .####
# .####
# .####
# .#.#.
# .#...
# .....
keys = []
locks = []
for item in items:
    lines = item.split('\n')
    bits = [-1] * 5
    for line in lines:
        for col, char in enumerate(line):
            if char == "#":
                bits[col] += 1
    # print(bits)
    if lines[0] == "#####":
        keys.append(bits.copy())
    else:
        locks.append(bits.copy())
parta = 0
for lock in locks:
    for key in keys:
        fit = True
        for bit in range(5):
            if lock[bit] + key[bit] > 5:
                fit = False
        if fit:
            parta += 1

print("Part A:", parta)
