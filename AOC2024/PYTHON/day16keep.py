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

# From a direction, return (left, right)
def leftright(dir):
    left  = (dir+3) % 4
    right = (dir+1) % 4
    return [left, right]

# Calculate the location if you moved from pos in dir
def posdir(pos,dir):
    dirpair = dirs[dir]
    return (pos[0]+dirpair[0],pos[1]+dirpair[1])

# Looking from a position in a direction return:
# ((aheadpos, aheaddir), (leftpos, leftdir), (rightpos, rightdir))
#      A
#    L ^ R
def look(pos,dir):
    aheadpos = posdir(pos,dir)
    (leftdir, rightdir) = leftright(dir)
    leftpos  = posdir(pos, leftdir)
    rightpos = posdir(pos, rightdir)
    return ((aheadpos, dir), (leftpos, leftdir), (rightpos, rightdir))

# From currentpos, provide a list of possible next locations as: (pos, dir, distance)
# Needs to include all locations in a straight line from pos which either:
#   a) are as far as is possible in newdir; OR
#   b) is before that but stops next to a "junction" of 3 or more paths
def nextindir(currentpos, newdir):
    workpos = currentpos
    workdir = newdir
    distance = 0
    while True:
        ((aheadpos, aheaddir), (leftpos, leftdir), (rightpos, rightdir)) = look(workpos, workdir)
        distance += 1
        aheadchar = grid[aheadpos]
        if aheadchar == "#":
            # This is type a)
            yield (aheadpos, newdir, distance)
        else:
            # Let's see if we are at a type b)
            leftchar = grid[]
        

# From currentpos, provide a list of the possible next locations with costs to get there
# The cost will be:
#   <The number of cells to the new position> + 1000
#   Notable that the turning cost is always 1000 because you would never turn twice because that is going back 
#     and you would never not turn because then you would have done things in the previous step.
# Because of never going straight or about turning, the turns alternate between horizontal and vertical moves.
#   and that means on each turn you only look left and right from the previous dir (see function leftright)
# Needs to include all locations in a straight line from pos which either:
#   a) are as far as is possible in a direction; OR
#   b) stops next to a "junction" of 3 or more paths
# Also note:
# * Don't go back the way you cam (can determine that from looking at currentdir)
def next(currentpos, currentdir):
    work = currentpos
    dirs = bothways(currentdir)




rpos = start # Start at S
rdir = 0 # Start facing east


parta, partb = 0, 0
print("Part A:", parta)
print("Part B:", partb)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")