#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.splitlines()

cave = set()  # The set of all filled points in cave (whether rock or sand)

def rockline(a, b):
    if a[0] == b[0]:
        x = a[0]
        y1 = min(a[1], b[1])
        y2 = max(a[1], b[1])
        for y in range(y1, y2 + 1):
            cave.add((x, y))
    else:
        y = a[1]
        x1 = min(a[0], b[0])
        x2 = max(a[0], b[0])
        for x in range(x1, x2 + 1):
            cave.add((x, y))

def caverocks():
    for line in lines:
        points = line.split(' -> ')
        lastpos = None
        for point in points:
            bits = point.split(',')
            pos = (int(bits[0]), int(bits[1]))
            if lastpos != None:
                rockline(lastpos, pos)
            lastpos = pos

def floorrocks(y):
    height = maxy - miny + 1
    minxfloor = min(minx, spout[0] - height - 2)  # 2 is to be safe
    maxxfloor = max(maxx, spout[0] + height + 2)  # 2 is to be safe
    for x in range(minxfloor, maxxfloor + 1):
        cave.add((x, y))

caverocks()
spout = (500, 0)
miny = 0  # Fixed at zero for spout
maxy = 0
minx = 10000
maxx = 0
# Find range of x and y
for pos in cave:
    minx = min(minx, pos[0])
    maxx = max(maxx, pos[0])
    maxy = max(maxy, pos[1])
    # miny not needed because miny is spout = 0
floory = maxy+2
floorrocks(floory)

def below(pos, adj):
    return (pos[0] + adj, pos[1] + 1)


# Return resting place of grain
def drop():
    grain = spout
    while True:
        next = below(grain, 0)
        if next in cave:
            next = below(grain, -1)
            if next in cave:
                next = below(grain, 1)
                if next in cave:
                    break  # All three blocked so we've found our grain resting spot
        grain = next
    cave.add(grain)
    return grain


parta = None
partb = None
graincount = 0
while partb == None:
    latest = drop()
    graincount += 1
    if latest[1] == floory-1 and parta == None:
        parta = graincount-1  # Note "-1" because we don't include the grain which falls to the floor
    if latest == spout:
        partb = graincount
print(f"Day {daytext}: Part A = {parta}")
print(f"Day {daytext}: Part B = {partb}")
