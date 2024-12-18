#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
import time
start_time = time.time()

lines = text.split('\n')
grid = {}
ylen = len(lines)
start, end = None, None
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        pos = (x,y)
        grid[pos] = char
        if char == "S":
            start = pos
        elif char == "E":
            end = pos
    xlen = len(line)

def show():
    for y in range(ylen):
        for x in range(xlen):
            char = grid[x,y]
            print(char,end="")
        print()
    print()

show()
print(start,end)

dirs = {0:(1,0),1:(0,1),2:(-1,0),3:(0,-1)}
dirhor = {(1,0),(-1,0)}
dirver = {(0,1),(0,-1)}
big = 10 ** 10

# Calculate the location if you moved from pos in dir
def posdir(pos,dir):
    return (pos[0]+dir[0],pos[1]+dir[1])

def get(pos):
    return grid[pos] if pos in grid else "#"

def compare(a, b):
    return (a > b) - (a < b)

# Get the direction of b from a as one of the four directions as (x,y)
# Assumes that the two are either horizontal or vertical (diagonals cause an error!)
def getdir(a, b):
    xd, yd = bx-ax, by-ay
    if xd == 0:
        assert yd != 0
        return (0, compare(by, ay))
    if yd == 0:
        assert xd != 0
        return (compare(bx, ax),0)

def ispath(pos):
    return get(pos) in {".","S","E"}

# Whether a position is at a junction
def isjunction(pos):
    if not ispath(pos):
        # Walls are not junctions
        return False
    if get(pos) in {"S", "E"}:
        # Always include start and end as junctions
        return True
    hor = sum(1 for dir in dirhor if ispath(posdir(pos, dir))) # Number of horizontal paths from pos
    ver = sum(1 for dir in dirver if ispath(posdir(pos, dir))) # Number of vertical paths from pos
    if hor == 0 or ver == 0:
        # 0,0 isolated cell (walls all round)
        # 0,1 deadend
        # 0,2 straightline
        return False
    # In which case it's one of:
    # 1,1 corner
    # 1,2 tjunction
    # 2,2 crossroads
    # Which are all counted as junctions:
    return True

junctions = set(pos for pos in grid.keys() if isjunction(pos))
print("junctions")
print(junctions)

links = {}

def connect(a,b,dist):
    if a not in links:
        links[a] = {(b,dist)}
    else:
        links[a].add((b,dist))

# def doubleconnect(a,b,dist):
#     connect(a,b,dist)
    # connect(b,a,dist)

for a in junctions:
    for b in junctions:
        ax, bx = a[0], b[0]
        ay, by = a[1], b[1]
        xd, yd = abs(ax-bx), abs(ay-by)
        if xd == 0 and all(ispath((ax,y)) for y in range(min(ay,by), max(ay,by)+1)):
            connect(a,b,yd)
        elif yd == 0 and all(ispath((x,ay)) for x in range(min(ax,bx), max(ax,bx)+1)):
            connect(a,b,xd)
print("links")
for link in links.items():
    print(link)
    print("- - - - - - -")

import time
parta_time = time.time()  # Record the current time

# From pos pointing in dir, find the minimum score to get to end using the remaining junctions
def score(pos, dir, junctions):
    global parta_time
    # Print only if 1 second has passed
    if time.time() - parta_time >= 1:
        print(len(junctions))
        parta_time = time.time()  # Reset the timer
        
    # print(">>>", pos, dir)
    minscore = big
    if pos == end:
        # We've got to the end so return zero score
        return 0
    nextlinks = links[pos]
    if len(nextlinks) == 0:
        # We've got to a dead end so return a big number
        return big
    # Otherwise we can explore the possible directions:
    for (linkpos, linkdist) in nextlinks:
        # If we are pointing in a vertical direction
        if dir in dirver:
            # We need to now move horizontally so we need a horizontal link:
            if ax == bx:
                if linkpos in junctions:
                    newpos = linkpos
                    newdir = (0, compare(linkpos, pos))
                    newjunctions = junctions.copy()
                    newjunctions.remove(pos)
                    newscore = score(newpos, newdir, newjunctions) + linkdist + 1000
                    minscore = min(minscore, newscore)
        elif dir in dirhor:
            # We need to now move vertically so we need a vertical link:
            if ay == by:
                if linkpos in junctions:
                    newpos = linkpos
                    newdir = (compare(linkpos, pos), 0)
                    newjunctions = junctions.copy()
                    newjunctions.remove(pos)
                    newscore = score(newpos, newdir, newjunctions) + linkdist + 1000
                    minscore = min(minscore, newscore)
    return minscore

parta = score(start, (1,0), junctions)
print("Part A:", parta)
parta, partb = 0, 0
print("Part B:", partb)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")