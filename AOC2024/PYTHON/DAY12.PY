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
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        grid[(x,y)] = char
    xlen = len(line)

todo = grid.copy()

# Return neighbours in same plot
def neighs(pos):
    plant = grid[pos]
    for off in [(0,1),(1,0),(0,-1),(-1,0)]:
        next = (pos[0]+off[0], pos[1]+off[1])
        if next in grid:
            if grid[next] == plant:
                yield next

# Get plots
plots = []
while todo:
    (pos, plant) = todo.popitem() # Choose any item to work with
    plot = [pos] # Start a plot with a seed
    tocheck = [pos] # This to hunt using flood fill starting at the seed
    while tocheck:
        check = tocheck.pop()
        for neigh in neighs(check):
            if neigh not in plot:
                plot.append(neigh) # Add to our plot
                todo.pop(neigh) # And remove from the todo list
                tocheck.append(neigh) # And finally add to the tocheck list
    # We have a plot!
    plots.append( (plant, plot) )

def perimiter(plot):
    total = 0
    for pos in plot:
        total += 4
        for neigh in neighs(pos):
            total -= 1
    return total

# For a boundary between two cells get . or x for the first cell and . or x for the second
# where x means the cell is in the plot and . means not
def get(poss, x, y):
    pos = (x,y)
    return "x" if pos in poss else "."

# Now we look for runs of .x or x. in both horizontal directions to count the fences
def sides(poss):
    xs = [x for (x, _) in poss]
    xrange = range(min(xs)-1, max(xs)+1)
    ys = [y for (_, y) in poss]
    yrange = range(min(ys)-1, max(ys)+1)
    fences = 0
    # Count horizontal fences
    for y in yrange:
        last = "none"
        for x in xrange:
            sig = get(poss, x, y) + get(poss, x, y+1)
            if sig in [".x", "x."]:
                if sig != last:
                    fences += 1
            last = sig
    # Count vertical fences
    for x in xrange:
        last = "none"
        for y in yrange:
            sig = get(poss, x, y) + get(poss, x+1, y)
            if sig in [".x", "x."]:
                if sig != last:
                    fences += 1
            last = sig
    return fences

parta, partb = 0, 0
for (plant, poss) in plots:
    area = len(poss)
    parta += area * perimiter(poss)
    partb += area * sides(poss)

print("Part A:", parta)
print("Part B:", partb)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
