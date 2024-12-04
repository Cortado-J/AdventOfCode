#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
grid = {}
ylen = len(lines)
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        grid[(x,y)] = char
    xlen = len(line)
dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
offsets = [(0,0),(1,1),(-1,1),(-1,-1),(1,-1)]
crosses = ["AMMSS", "ASMMS", "ASSMM", "AMSSM"]

def get(pos):
    return grid[pos] if pos in grid else "#"

def finda(x, y, dir, word):
    xx, yy = x, y
    for char in word:
        pos = (xx, yy)
        if char == get(pos):
            xx += dir[0]
            yy += dir[1]
        else:
            return False
    return True

def findb(x, y, word):
    for index, char in enumerate(word):
        pos = (x+offsets[index][0], y+offsets[index][1])
        if char != get(pos):
            return False
    return True

parta, partb = 0, 0

for y in range(ylen):
    for x in range(xlen):
        for dir in dirs:
            if finda(x, y, dir, "XMAS"):
                parta += 1
        for cross in crosses:
            if findb(x, y, cross):
                partb += 1

print("Part A:", parta)
print("Part B:", partb)
