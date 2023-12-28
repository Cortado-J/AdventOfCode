import copy
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
jets = text
jetlength = len(jets)
shapes = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (0, 1), (1, 1)]
    ]

cavewidth = 7
air = [0, 0, 0, 0, 0, 0, 0]
floor = [1, 1, 1, 1, 1, 1, 1]
cave = [floor]

def towerheight():
    return len(cave)-1

def cango(shapeindex, atx, aty):
    shape = shapes[shapeindex]
    for shapex, shapey in shape:
        placex = atx + shapex
        placey = aty + shapey
        maxy = towerheight()
        if placex >= cavewidth or placex < 0:  # Bumped into side
            return False
        if placey <= maxy:  # Not in above cave drawn so far so check bump:
            if cave[placey][placex] == 1:  # Bumped into rocks or floor
                return False
    return True

def place(shapeindex, atx, aty):
    shape = shapes[shapeindex]
    for (shapex, shapey) in shape:
        placex = atx + shapex
        placey = aty + shapey
        while placey > len(cave) - 1:
            cave.append(copy.deepcopy(air))
        cave[placey][placex] = 1

jetindex = 0

def jet():
    global jetindex
    jetindex = (jetindex + 1) % jetlength
    return -1 if jets[jetindex-1] == '<' else 1

def showcave():
    for y in range(towerheight(),-1,-1):
        print(''.join(['#' if point == 1 else '.' for point in cave[y]]))

# Record recent history:
# We want to spot when we get same:
# a) Point in jet cycle
# b) Point in shape cycle
# c) Last n rows compacted
lastn = 3 # We actually only need one row!
history = {} # Key is the recent tuple as described above.  Value is the rock index where it happened

def hash(caveslice):
    val = 0
    mult = 1
    for row in caveslice:
        for point in row:
            val += point * mult
            mult *= 2
    return val

def drop():
    currentx = 2
    currenty = len(cave) + 3
    while True:
        # Gas blow
        proposex = currentx + jet()
        if cango(nextrock, proposex, currenty):
            currentx = proposex

        # Drop
        proposey = currenty - 1
        if cango(nextrock, currentx, proposey):
            currenty = proposey
        else:
            place(nextrock, currentx, currenty)
            # showcave()
            # print("=====================")
            break

nextrock = 0
parta = None
partb = None
rock = 0
heights = []
while parta is None or partb is None:
    drop()
    heights.append(towerheight)
    if parta is None:
        if rock == 2022-1: # -1 because first rock is rock zero
            parta = towerheight()
    if partb is None:
        if rock > lastn:
            # a) Point in jet cycle
            # b) Point in shape cycle
            # c) Last n rows (lets start with n = 3)
            recent = (jetindex, nextrock, hash(cave[-1-lastn:-1]))
            if recent in history:
                startofcycle = history[recent]
                cyclelen = rock - startofcycle
                heightatstartofcylce = heights[startofcycle]
                heightgainedinacycle = towerheight()-heights[startofcycle]
                totalrocks = 1000000000000
                rocksdone = rock+1
                rockstogo = totalrocks - rocksdone
                cycleswecanskip = rockstogo // cyclelen
                heightwewouldgainfromthosecycles = cycleswecanskip * heightgainedinacycle
                rocksremainingtodo = rockstogo % cyclelen
                # We can find the increase from those last ones.
                # The increase will be equivalent to the increase of height between
                #    startofcycle                                [which we know as heightatstartofcylce]
                #    point = startofcylce + rocksremainingtodo   [which we don't know but have recorded]
                heightatpoint = heights[startofcycle+rocksremainingtodo]
                increasefromstartofcycletopoint = heightatpoint - heightatstartofcylce

                finalheight = towerheight() + heightwewouldgainfromthosecycles + increasefromstartofcycletopoint
                partb = finalheight
            history[recent] = rock
    heights[rock] = towerheight()
    rock += 1
    if rock % 10000 == 0:
        print(rock)
    nextrock = ((nextrock + 1) % 5)

print(f"Day {daytext}: Part A = {parta}")
print(f"Day {daytext}: Part B = {partb}")
