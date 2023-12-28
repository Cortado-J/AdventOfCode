from collections import deque
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.splitlines()

elves = set()
for row, line in enumerate(lines):
    for col, ch in enumerate(line):
        if ch == '#':
            elves.add((row, col))

def limits():
    up    = min([row for row, col in elves])
    down  = max([row for row, col in elves])
    left  = min([col for row, col in elves])
    right = max([col for row, col in elves])
    return up, down, left, right

def show():
    up, down, left, right = limits()
    print(f"Rows: {up} to {down} and Cols: {left} to {right}")
    for row in range(up, down+1):
        for col in range(left, right+1):
            print('#' if (row, col) in elves else '.', end='')
        print()

allpos = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
look = [[(-1, -1), (-1, 0), (-1, 1)], [(1, -1), (1, 0), (1, 1)], [(-1, -1), (0, -1), (1, -1)], [(-1, 1), (0, 1), (1, 1)]]
looking = 0
show()
round = 1
parta = None
partb = None
while parta is None or partb is None:
    propose = {}
    moves = 0

    # First half
    for elf in elves:
        if not all([(elf[0] + offset[0], elf[1] + offset[1]) not in elves for offset in allpos]):
            lookingindex = looking
            while True:
                offsets = look[lookingindex]
                if all([(elf[0]+offset[0], elf[1]+offset[1]) not in elves for offset in offsets]):
                    proposedelta = offsets[1] # The middle one (N,S,E,W)
                    proposepos = (elf[0] + proposedelta[0], elf[1] + proposedelta[1])
                    if proposepos in propose:
                        propose[proposepos].append(elf)
                    else:
                        propose[proposepos] = [elf]
                    break # Once we've found a proposed direction don;t make any more proposals
                lookingindex = (lookingindex+1) % 4
                if lookingindex == looking:
                    break # Only try each direction once

    # Second half
    for newpos, proposers in propose.items():
        if len(proposers) == 1:
            elves.remove(proposers[0])
            elves.add(newpos)
            moves += 1

    if moves == 0:
        partb = round

    # Adjust directions
    looking = (looking + 1) % 4

    round += 1
    if round == 10:
        up, down, left, right = limits()
        parta = (right - left + 1) * (down - up + 1) - len(elves)


print(f"Day {daytext}: Part A = {parta}")
print(f"Day {daytext}: Part B = {partb}")
