#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
rows = text.splitlines()
H = len(rows)
W = len(rows[0])
offset = H // 2
turnleft  = {(1,0):(0,-1),(0,-1):(-1,0),(-1,0):(0,1),(0,1):(1,0)}
turnright = {(1,0):(0,1),(0,1):(-1,0),(-1,0):(0,-1),(0,-1):(1,0)}
reverse   = {(1,0):(-1,0),(0,1):(0,-1),(-1,0):(1,0),(0,-1):(0,1)}

def show(grid, current, direction):
    xmin, xmax = 1000000, -1000000
    ymin, ymax = 1000000, -1000000
    for (x,y) in grid:
        xmin, xmax = min(xmin, x), max(xmax, x)
        ymin, ymax = min(ymin, y), max(ymax, y)
    print()
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            pos = (x, y)
            print(grid[pos] if pos in grid else ".", end="")
            if x == current[0]-1 and y == current[1]:
                print("[", end="")
            elif x == current[0] and y == current[1]:
                print("]", end="")
            else:
                print(" ", end="")
        print()
    print("Pointing:", direction)

def run(part, generations):
    grid = {}
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char == "#":
                pos = (x-offset, y-offset)
                grid[pos] = char
    current = (0, 0)
    direction = (0, -1) # North (x,y)
    # show(grid, current, direction)
    infections = 0

    def burst():
        nonlocal current
        nonlocal direction
        nonlocal infections
        nonlocal part
        if current in grid:
            state = grid[current]
            # The following works for parts a and b
            # Part A instructions:
            # If the current node is infected, it turns to its right. Otherwise, it turns to its left. (Turning is done in-place; the current node does not change.)
            # Part B instructions embedded

            if   state == "W":
                # If it is weakened, it does not turn, and will continue moving in the same direction.
                pass
            elif state == "#":
                # If it is infected, it turns right.
                direction = turnright[direction]
            else: #state == "F":
                # If it is flagged, it reverses direction, and will go back the way it came.
                direction = reverse[direction]
        else:
            # If it is clean, it turns left.
            direction = turnleft[direction]

        if part == "A":
            # If the current node is clean, it becomes infected. Otherwise, it becomes cleaned. (This is done after the node is considered for the purposes of changing direction.)
            if current in grid:
                del grid[current]
            else:
                grid[current] = "#"
                infections += 1
        else: # part == "B":
            if current in grid:
                state = grid[current]
                if state == "W":
                    # Weakened nodes become infected.
                    grid[current] = "#"
                    infections += 1
                elif state == "#":
                    # Infected nodes become flagged.
                    grid[current] = "F"
                else: #state == "F":
                    # Flagged nodes become clean.
                    del grid[current]
            else:
                # Clean nodes become weakened.
                grid[current] = "W"
 
        # The virus carrier moves forward one node in the direction it is facing.
        current = (current[0] + direction[0], current[1] + direction[1])

    for gen in range(generations):
        burst()
        # show(grid, current, direction)
    return infections

resulta = run("A", 10000)
print("Result A = ", resulta)
resultb = run("B", 10000000)
print("Result B = ", resultb)
