#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
import time
start_time = time.time()
blocks = text.split('\n\n')
a = blocks[0]

# #..O@..O.#
# ##########

# <vv>^<v^>v>^vv^v>v<>v^v<v<^

lines = blocks[0].split('\n')
ylen = len(lines)
robot = (0,0)
grid = {}
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        pos = (x,y)
        if char == "@":
            robot = (x,y)
            grid[(x,y)] = "."
        else:
            grid[(x,y)] = char
    xlen = len(line)
print(grid)
print(robot)

moves = blocks[1]
print(moves)

dirs = {"<":(-1,0),">":(1,0),"^":(0,-1),"v":(0,1)}
print(dirs)
a = 0

def posadd(pos,dir):
    return (pos[0]+dir[0],pos[1]+dir[1])

# def possub(pos,dir):
#     return (pos[0]-dir[0],pos[1]-dir[1])

def moveit(dir):
    global robot
    next = posadd(robot,dir)
    if grid[next] == ".":
        robot = next
        return True
    if grid[next] == "#":
        return False
    if grid[next] == "O":
        linestart = next
        while True:
            nextline = posadd(next,dir)
            if grid[nextline] == ".":
                # We've hit end of line and we can move:
                lineoffend = nextline
                grid[lineoffend] = "O"
                grid[linestart] = "."
                robot = linestart
                return True
            elif grid[nextline] == "#":
                # We've hit a wall so can;t go!
                return False
            else:
                # We're seeing more of the line of blocks:
                next = nextline

def show():
    for y in range(ylen):
        for x in range(xlen):
            char = "@" if x == robot[0] and y == robot[1] else grid[x,y]
            print(char,end="")
        print()
    print()

show()

for move in moves:
    if move in dirs:
        dir = dirs[move]
        # print(move, dir)
        if moveit(dir):
            # show()
            pass

parta = 0
for y in range(ylen):
    for x in range(xlen):
        pos = (x,y)
        if grid[pos] == "O":
            parta += y*100+x
print("Part A:", parta)

partb = 0
print("Part B:", partb)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
