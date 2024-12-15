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

def posadd(pos,dir):
    return (pos[0]+dir[0],pos[1]+dir[1])

lines = blocks[0].split('\n')
ylen = len(lines)
robot = (0,0)
grid = {}
dub = {"#":"##", "O":"[]", ".":"..", "@":".."} # Robot as .. cos it's posn is stored elsewhere!
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        pos = (x*2,y)
        if char == "@":
            robot = pos
        grid[pos] = dub[char][0]
        grid[posadd(pos,(1,0))] = dub[char][1]
    xlen = len(line)*2
print(grid)
print(robot)

moves = blocks[1]
print(moves)

dirs = {"<":(-1,0),">":(1,0),"^":(0,-1),"v":(0,1)}
print(dirs)
a = 0

# The left hand bit of the block at pos
def left(pos):
    if grid[pos] == "[":
        return pos
    if grid[pos] == "]":
        return (pos[0]-1,pos[1])
    return None

# The right hand bit of the block at pos
def right(pos):
    if grid[pos] == "[":
        return (pos[0]+1,pos[1])
    if grid[pos] == "]":
        return pos
    return None

def oneright(pos):
    return posadd(pos, (1,0))

# An array of all the left hand cells of the blocks in poss
def getlefts(poss):
    gather = set()
    for pos in poss:
        if pos != robot:
            gather.add(left(pos))
    return list(gather)

# The positions of the block at position pos moved in direction dir
def moved(pos, dir):
    base = left(pos)
    if base == None:
        return None
    rig = right(pos)
    return [posadd(base,dir), posadd(rig, dir)]

def movetype(dir):
    return "|" if dir[0] == 0 else "-"

# The positions needed to move the block or robot at pos in direction dir
# Or "None" if there is no block or robot at pos
def needed(pos, dir):
    if pos == robot:
        return [posadd(pos, dir)]
    if dir == (1,0): # Right
        return [posadd(right(pos),dir)]
    if dir == (-1,0): # Left
        return [posadd(left(pos),dir)]
    lef = left(pos)
    if lef == None:
        return None
    rig = right(pos)
    return [posadd(lef,dir), posadd(rig, dir)]

# Whether all the positions in the list are free to move to
def free(poss):
    for pos in poss:
        if grid[pos] != ".":
            return False
    return True

# Whether any position in the list is a wall
def blocked(poss):
    for pos in poss:
        if grid[pos] == "#":
            return True
    return False

# List of all positions recursively dependent on position pos being move in direction dir
# Result includes the pos itself (Which may be a robot or a block!)
# Or "None" if either there is no block at pos or a wall blocks the whole scenario
def depend(pos, dir):
    need = needed(pos,dir)
    if need == None:
        # We're looking at space!
        return "SPACE"
    if blocked(need):
        # Blocked by a wall!
        return "WALL"
    if free(need):
        # No further dependents so just return the position
        return [pos]
    deps = [pos]
    for needpos in need:
        dep = depend(needpos, dir)
        if dep == "SPACE":
            # That's fine for a dependency so just don't add any dependencies
            pass
        elif dep == "WALL":
            # We're blocked so this is a no go!
            return "WALL"
        else:
            # We've actually got a list of blocks we depend on:
            deps += dep
    return deps

def moveit(dir):
    global robot
    dep = depend(robot, dir)
    assert dep != "SPACE"  # The robot should never be in space!!
    if dep == "WALL":
        # We're blocked so do nothing (Don't even move the robot!)
        pass
    else:
        # We've actually got a list of blocks we depend on and no blockage!
        blocks = getlefts(dep)
        # Clear all the blocks
        for block in blocks:
            grid[block] = "."
            grid[oneright(block)] = "."
        # Create all the blocks in the grid but now moved
        for block in blocks:
            moved = posadd(block,dir)
            grid[moved] = "["
            grid[oneright(moved)] = "]"
        robot = posadd(robot,dir)

def show():
    for y in range(ylen):
        for x in range(xlen):
            char = "@" if x == robot[0] and y == robot[1] else grid[x,y]
            print(char,end="")
        print()
    print()

show()

for move in moves[:]:
    if move in dirs:
        dir = dirs[move]
        print(move, dir)
        if moveit(dir):
            pass
        # show()

partb = 0
for y in range(ylen):
    for x in range(xlen):
        pos = (x,y)
        if grid[pos] == "[":
            partb += y*100+x
print("Part B:", partb)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
