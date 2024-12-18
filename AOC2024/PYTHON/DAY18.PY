#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
grid = {}
xlen, ylen = 6,6
xlen, ylen = 70,70

def get(pos):
    if pos not in grid:
        return "#"
    return grid[pos] if pos in grid else "."

def show():
    for y in range(ylen+1):
        for x in range(xlen+1):
            char = get((x,y))
            print(char,end="")
        print()
    print()

show()

dirs = {0:(1,0),1:(0,1),2:(-1,0),3:(0,-1)}

# Calculate the location if you moved from pos in dir
def posdir(pos,dir):
    return (pos[0]+dir[0],pos[1]+dir[1])

def neighs(pos):
    for dir in dirs.values():
        yield posdir(pos, dir)

start = (0,0)
end = (6,6)
end = (70,70)
parta = None
partb = None

for x in range(xlen+1):
    for y in range(ylen+1):
        pos = (x,y)
        grid[pos] = "."
for index, line in enumerate(lines):
    bits = line.split(",")    
    x, y = int(bits[0]), int(bits[1])
    pos = (x,y)
    grid[pos] = "#"

    if index >= 1023:
        # We have the grid with index-1 blocks loaded
        fill = set()
        edge = set()
        edge.add(start)

        def showit():
            for y in range(ylen+1):
                for x in range(xlen+1):
                    pos = (x,y)
                    if pos in edge:
                        print("E",end="")
                    elif pos in fill:
                        print("O",end="")
                    else:
                        char = get(pos)
                        print(char,end="")
                print()
            print("----------------------------------------")

        for steps in range(10000000):
            if end in edge:
                # We've found a solution
                print(f"SUCCEEDED AT STEP {index}")
                # showit()
                if index == 1023:
                    parta = steps
                # Because we've found a solution break from this loop
                break
            fill |= edge
            nextedge = set()
            for p in edge:
                for neigh in neighs(p):
                    if get(neigh) == ".": # Check it's free space in grid
                        if neigh not in fill:  # Check it's not used by previous fill
                            if neigh not in edge:  # Check it's not part of the edge
                                # So it's a new place to fill!
                                nextedge.add(neigh)
            # We have nextedge as the new edge
            if len(edge) == 0:
                # We have failed to find a route:
                print("FAILED AT STEP {index}")
                showit()
                partb = pos
                break

            edge = nextedge.copy()
        if parta != None and partb != None:
            print(f"Part A: {parta}")
            print(f"Part B: {partb}")
            break
    if parta != None and partb != None:
        break
