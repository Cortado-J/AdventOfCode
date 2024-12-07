#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
dirs = [(0,-1), (1,0), (0,1), (-1,0)]
grid = {}
start = (0,0) # Will be overwritten below
for x, line in enumerate(text.split('\n')):
    for y, char in enumerate(line):
        pos = (x,y)
        grid[pos] = char
        if char == "^":
            start = pos

visited = set()
pos = start
dir = 0
while pos in grid:
    visited.add(pos)
    dir_off = dirs[dir]
    look = (pos[0]+dir_off[1],pos[1]+dir_off[0])
    if look not in grid:
        pos = look
    else:
        next_val = grid[look]
        if next_val == "#":
            dir = (dir+1) % 4
        else:
            pos = look
parta = len(visited)
print("Part A: ", parta)

def loops():
    pos = start
    dir = 0
    visited = set() # of ((x,y),dir)
    while True:
        if not pos in grid:
            return False
        pair = (pos,dir)
        if pair in visited:
            return True
        visited.add(pair)
        dir_off = dirs[dir]
        look = (pos[0]+dir_off[1],pos[1]+dir_off[0])
        if look not in grid:
            pos = look
        else:
            next_val = grid[look]
            if next_val == "#":
                dir = (dir+1) % 4
            else:
                pos = look
    
tries = []
for pos in visited:
    if pos != start:
        tries.append(pos)
partb = 0
for count, newpos in enumerate(tries):
    if count % 100 == 0:
        print(".", end = "", flush=True)
    grid[newpos] = "#"
    if loops():
        partb += 1
    grid[newpos] = "."
print()
print("Part B: ", partb)
