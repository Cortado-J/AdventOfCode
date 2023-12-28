from collections import deque
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.splitlines()

valley = {}
goal = None
start = None
rowsize = len(lines)
colsize = len(lines[0])
for row, line in enumerate(lines):
    for col, ch in enumerate(line):
        if ch in '<>v^':
            valley[(row, col, 0)] = [ch]
        else:
            if row == 0 and ch == '.':
                start = (row, col)
            if row == len(lines) - 1 and ch == '.':
                goal = (row, col)
nexttogoal = (goal[0] - 1, goal[1])
valrows = rowsize - 2
valcols = colsize - 2
blowing = {'>': (0, 1), '<': (0, -1), 'v': (1, 0), '^': (-1, 0), 'W': (0, 0)}


def show(t):
    for r in range(rowsize):
        for c in range(colsize):
            if r == 0 or r == rowsize - 1 or c == 0 or c == colsize - 1:
                if (r, c) == start or (r, c) == goal:
                    print('*', end='')
                else:
                    print('#', end='')
            else:
                if (r, c, t) in valley:
                    blizzards = valley[(r, c, t)]
                    if len(blizzards) == 1:
                        print(blizzards[0], end='')
                    else:
                        print(len(blizzards), end='')
                else:
                    print('.', end='')
        print()
    print('- - - - - - - - - - - - - - - - -')


def showstep(t):
    steps = paths[t]
    for r in range(rowsize):
        for c in range(colsize):
            if r == 0 or r == rowsize - 1 or c == 0 or c == colsize - 1:
                if (r, c) == start or (r, c) == goal:
                    print('*', end='')
                else:
                    print('#', end='')
            else:
                if (r, c) in steps:
                    print('O', end='')
                else:
                    print('.', end='')
        print()
    print('- - - - - - - - - - - - - - - - -')


def blow(fromt):
    for r in range(1, rowsize - 1):
        for c in range(1, colsize - 1):
            if (r, c, fromt) in valley:
                blizzards = valley[(r, c, fromt)]
                for blizzard in blizzards:
                    if blizzard in blowing:
                        blow = blowing[blizzard]
                        newr = ((r + blow[0] + valrows - 1) % valrows) + 1
                        newc = ((c + blow[1] + valcols - 1) % valcols) + 1
                        if (newr, newc, fromt + 1) in valley:
                            valley[(newr, newc, fromt + 1)].append(blizzard)
                        else:
                            valley[(newr, newc, fromt + 1)] = [blizzard]


# An array (over t) of sets where set is possible positions
paths = [set()]


def setstagestart(time, frompos):
    assert time == len(paths) - 1  # Only allow setting last stage
    starting = set()
    starting.add(frompos)
    paths[time] = starting


setstagestart(0, start)


# Find paths from time t
def step(fromt):
    possible = set()
    for current in paths[fromt]:
        for move in blowing.values():
            newrow = current[0] + move[0]
            newcol = current[1] + move[1]
            if (1 <= newrow < rowsize - 1 and 1 <= newcol < colsize - 1) \
                    or ((newrow, newcol) == start) \
                    or ((newrow, newcol) == goal):
                newpos = (newrow, newcol, fromt + 1)
                if newpos not in valley:
                    possible.add((newrow, newcol))
    paths.append(possible)


t = 0


def timebetween(startpos, endpos):
    global t
    setstagestart(t, startpos)
    while True:
        # print(f"Minute {t}:")
        # show(t)
        if endpos in paths[t]:
            return t
        blow(t)
        step(t)
        # showstep(t+1)
        t += 1


parta = timebetween(start, goal)
print(f"Day {daytext}: Part A = {parta}")

partbstart = timebetween(goal, start)
partb = timebetween(start, goal)
print(f"Day {daytext}: Part B = {partb}")
