from collections import deque
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.splitlines()

cave = {}
moves = lines[-1] + 'X'  # Add X to ensure last character of "moves" gets processed
cavesize = 10000
maxwidth = 0
for row, line in enumerate(lines[:-2]):
    mincol = 10000
    maxcol = 0
    for col, ch in enumerate(line):
        if not ch == ' ':
            cave[(row, col)] = ch
            mincol = min(mincol, col)
            maxcol = max(maxcol, col)
    rowwidth = maxcol - mincol + 1
    cavesize = min(cavesize, rowwidth)
    maxwidth = max(maxwidth, len(line))
print("cavesize=", cavesize)


def showcave(pos):
    print("==============================")
    for row in range(len(lines[:-2])):
        for col in range(maxwidth):
            if not (row, col) in cave:
                print('~', end='')
            elif row == pos[0] and col == pos[1]:
                print('X', end='')
            else:
                print(cave[(row, col)], end='')
        print()


# Position is a tuple: (row,col)
# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def open(pos):
    return pos in cave and cave[pos] == '.'


def forward(row, col, n, face, cube):
    newface = None
    currentrow = row
    currentcol = col
    currentface = face
    for _ in range(n):
        dr, dc = directions[currentface]
        propose = (currentrow + dr, currentcol + dc)
        if propose not in cave:
            if not cube:
                # Part A
                propose = (propose[0] - 300 * dr, propose[1] - 300 * dc)
                while propose not in cave:
                    propose = (propose[0] + dr, propose[1] + dc)
            else:
                # Part B
                r = propose[0]
                c = propose[1]
                rr = r
                cc = c

                cuber = r // cavesize
                cubec = c // cavesize
                if cavesize == 50:
                    if   cuber == -1 and cubec ==  1 and currentface == 3: rr, cc, newface = c + 100, 0, 0
                    elif cuber ==  3 and cubec == -1 and currentface == 2: rr, cc, newface = 0, r - 100, 1
                    elif cuber == -1 and cubec ==  2 and currentface == 3: rr, cc, newface = 199, c - 100, 3
                    elif cuber ==  4 and cubec ==  0 and currentface == 1: rr, cc, newface = 0, c + 100, 1
                    elif cuber ==  0 and cubec ==  0 and currentface == 2: rr, cc, newface = 149 - r, 0, 0
                    elif cuber ==  2 and cubec == -1 and currentface == 2: rr, cc, newface = 149 - r, 50, 0
                    elif cuber ==  0 and cubec ==  3 and currentface == 0: rr, cc, newface = 149 - r, 99, 2
                    elif cuber ==  2 and cubec ==  2 and currentface == 0: rr, cc, newface = 149 - r, 149, 2
                    elif cuber ==  1 and cubec ==  0 and currentface == 2: rr, cc, newface = 100, r - 50, 1
                    elif cuber ==  1 and cubec ==  0 and currentface == 3: rr, cc, newface = c + 50, 50, 0
                    elif cuber ==  1 and cubec ==  2 and currentface == 0: rr, cc, newface = 49, r + 50, 3
                    elif cuber ==  1 and cubec ==  2 and currentface == 1: rr, cc, newface = c - 50, 99, 2
                    elif cuber ==  3 and cubec ==  1 and currentface == 0: rr, cc, newface = 149, r - 100, 3
                    elif cuber ==  3 and cubec ==  1 and currentface == 1: rr, cc, newface = c + 100, 49, 2
                    else:
                        assert False, f"Unrecognised combo: r={r} c={c} (cuber={cuber} cubec={cubec}) currentface={currentface} (propose={propose})"
                else:
                    if  cuber == -1 and cubec ==  2 and currentface == 3: rr, cc, newface = 4, 11 - c, 1
                    elif cuber == 0 and cubec ==  0 and currentface == 3: rr, cc, newface = 0, 11 - c, 1
                    elif cuber == 0 and cubec ==  1 and currentface == 2: rr, cc, newface = 4, r + 4, 1
                    elif cuber == 0 and cubec ==  1 and currentface == 3: rr, cc, newface = c - 4, 8, 0
                    elif cuber == 0 and cubec ==  3 and currentface == 0: rr, cc, newface = 11 - r, 15, 2
                    elif cuber == 2 and cubec ==  4 and currentface == 0: rr, cc, newface = 11 - r, 11, 2
                    elif cuber == 1 and cubec == -1 and currentface == 2: rr, cc, newface = 11, 19 - r, 3
                    elif cuber == 3 and cubec ==  3 and currentface == 1: rr, cc, newface = 19 - c, 0, 0
                    elif cuber == 1 and cubec ==  3 and currentface == 0: rr, cc, newface = 8, 19 - r, 1
                    elif cuber == 1 and cubec ==  3 and currentface == 3: rr, cc, newface = 19 - c, 11, 2
                    elif cuber == 2 and cubec ==  0 and currentface == 1: rr, cc, newface = 11, 11 - c, 3
                    elif cuber == 3 and cubec ==  2 and currentface == 1: rr, cc, newface = 7, 11 - c, 3
                    elif cuber == 2 and cubec ==  1 and currentface == 1: rr, cc, newface = 15 - c, 8, 0
                    elif cuber == 2 and cubec ==  1 and currentface == 2: rr, cc, newface = 7, 15 - r, 3
                    else:
                        assert False, f"Unrecognised combo: r={r} c={c} (cuber={cuber} cubec={cubec}) currentface={currentface} (propose={propose})"
                print(
                    f"Elf at ({currentrow},{currentcol}) moving {'>v<^'[currentface]} to ({r},{c}) (propose={(r, c)}) but over edge so instead propose ({rr},{cc}) moving {'>v<^'[newface]}")
                propose = (rr, cc)
        if not open(propose):
            break
        currentrow, currentcol = propose
        if newface is not None:
            currentface = newface
    return currentrow, currentcol, currentface


def solve(cube):
    # Initially, you are facing to the right (from the perspective of how the map is drawn).
    facing = 0
    # Rotate right means increase direction by 1 (mod 4)
    # Rotate left means decrease direction by 1 (mod 4)

    # Rows start from 1 at the top and count downward
    # Columns start from 1 at the left and count rightward.
    # (In the above example, row 1, column 1 refers to the empty space with no tile on it in the top-left corner.)
    # We'll use zero based until output
    # You begin the path in the leftmost open tile of the top row of tiles.
    row = 0
    col = 0
    while not open((row, col)):
        col += 1
    # print(f"Starting at row:{row}, col:{col}")

    number = 0
    # showcave((row, col))
    for i in range(len(moves)):  # Rounds
        m = moves[i]
        if m.isnumeric():
            number = number * 10 + int(moves[i])
        else:
            # Not a number so we need to process any number gathered:
            # print(f"Forward {number}")
            (row, col, newface) = forward(row, col, number, facing, cube)
            facing = newface
            # showcave((row, col))
            number = 0
            if m == 'R':
                # print(f"Turn Right")
                facing = (facing + 1) % 4
            elif m == 'L':
                # print(f"Turn Left")
                facing = (facing + 3) % 4
    # The final password is the sum of 1000 times the row, 4 times the column, and the facing.
    password = (row + 1) * 1000 + (col + 1) * 4 + facing
    return password


parta = solve(False)
print(f"Day {daytext}: Part A = {parta}")

partb = solve(True)
print(f"Day {daytext}: Part B = {partb}")
