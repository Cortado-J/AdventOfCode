#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
from collections import Counter

lines = text.split('\n')
grid = {}
ylen = len(lines)

def ischarpath(char): return char in {".","S","E"}

start, end = None, None
pathcount = 0
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        pos = (x,y)
        grid[pos] = char
        if char == "S":
            start = pos
        elif char == "E":
            end = pos
        if ischarpath(char):
            pathcount += 1
    xlen = len(line)

def show():
    for y in range(ylen):
        for x in range(xlen):
            char = grid[x,y]
            print(char,end="")
        print()
    print()

# show()
# print(start,end)

dirs = {0:(1,0),1:(0,1),2:(-1,0),3:(0,-1)}
dirhor = {(1,0),(-1,0)}
dirver = {(0,1),(0,-1)}
big = 10 ** 10

# Calculate the location if you moved from pos in dir
def posdir(pos,dir):
    return (pos[0]+dir[0],pos[1]+dir[1])

def ispath(pos):
    return ischarpath(get(pos))

def pathnexts(pos):
    result = []
    for dir in dirs.values():
        next = posdir(pos,dir)
        if ispath(next):
            result.append(next)
    return result

def get(pos):
    return grid[pos] if pos in grid else "#"

def compare(a, b):
    return (a > b) - (a < b)

pos = start
disttostart = {}
disttoend = {}
distsofar = 0
lastpos = None
disttostart[start] = 0
disttoend[start] = pathcount - 1
while pos != end:
    allpaths = pathnexts(pos)
    numberofpaths = len(allpaths)
    assert numberofpaths in [1,2]
    nextpos = allpaths[0]
    if numberofpaths == 2:
        if allpaths[0] == lastpos:
            nextpos = allpaths[1]
    # Now next is the next position along the path
    distsofar += 1
    disttostart[nextpos] = distsofar
    disttoend[nextpos] = pathcount - distsofar - 1
    lastpos = pos
    pos = nextpos
# print(f"pathcount={pathcount}")

def taxicab(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

parta, partb = 0,0

print("-------------------------------------")
print("Run time approx 20 seconds...")
for startpos, tostart in disttostart.items():
    for endpos, toend in disttoend.items():
        taxi = taxicab(startpos, endpos)
        if taxi <= 20:
            time = tostart + taxi + toend
            saving = pathcount-1-time
            if saving >= 100:
                partb += 1
                if taxi <= 2:
                    parta += 1

print("Part A:", parta)
print("Part B:", partb)
print("-------------------------------------")
