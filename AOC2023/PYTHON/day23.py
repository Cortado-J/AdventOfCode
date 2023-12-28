#######################################################
# Choose Part:
partb = False  # N.B. part b takes about 3 minutes!
#######################################################

#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
dirs = {'^': (0, -1), 'v': (0, 1), '>': (1, 0), '<': (-1, 0)}
forest = "#"

maze = {} # { (x,y) : char } where char is "#" for forest, '.' for flat path and one of ><v^ for a slope.
height = len(lines)
width = len(lines[0])
for y, row in enumerate(lines):
    for x, char in enumerate(row):
        if partb:
            if char in dirs:  # For partb only!!
                char = '.'    # For partb only!!
        maze[(x,y)] = char

startmaze = (1, 0)
endmaze = (width-2, height-1)

# Iterator which returns ((newx, newy), dslope) where (newx, newy) is a neighbour of pos and dslope is the direction a slope would need to go in that direction
def neighbours(pos):
    for dslope, dir in dirs.items():
        newx = pos[0] + dir[0]
        newy = pos[1] + dir[1]
        if 0 <= newx <= width-1 and 0 <= newy <= height-1:
            yield ((newx, newy), dslope)

# Iterator which returns ((newx, newy), dslope) where (newx, newy) is a neighbour of pos and dslope is the direction a slope would need to go in that direction
def neighbours_graph(pos):
    for dest in graph[pos].items():
        yield dest

# Iterator which returns topos where topos is a neighbour of pos and is a valid direction
#   'Valid direction' means that source and destinatin are either '.' or the correct '^v<>' for that direction
def destins(frompos):
    for topos, validslope in neighbours(frompos):
        if (maze[frompos] == '.' or maze[frompos] == validslope ) and (maze[topos] == '.' or maze[topos] == validslope):
            yield topos

# # Create a weighted graph: {frompos, {topos, weight}}
graph = {}
for frompos, char in maze.items():
    if char in '.<>^v':
        toposs = list(destins(frompos))
        if toposs:
            graph[frompos] = dict([(topos, 1) for topos in toposs])

# print(graph)
print("Before simplification:", len(graph), "nodes")

# Simplify maze (just one simplification)
# Step 1) For any nodea for which:
#   a) nodea has an edge TO a nodeb
#   b) nodeb is a path (not a slope)
#   c) nodeb is connected TO exactly two nodes: nodea and nodec
# Step 2) Remove nodeb:
#   a) add edge from nodea to nodec
#   b) weight from nodea to nodec should be sum of the weights from nodea to nodeb and nodeb to nodec
#   c) remove edge from nodea to nodeb
#   d) remove edge from nodeb to nodec
#   Note that we don't then remove nodeb because it might have other edges.
#   Once we have simplified the whole graph we can remove any orphan nodes :-) 
def simplify(graph):
    for nodea, adests in graph.items():
        # a) nodea has an edge TO a nodeb
        for nodeb, weightab in adests.items():
            # b) nodeb is a path (not a slope)
            if maze[nodeb] == '.':
                # c) nodeb is connected TO exactly two nodes: nodea and nodec
                if nodeb in graph:
                    bdests = graph[nodeb]
                    if len(bdests) == 2:
                        bdestslist = list(bdests.items())
                        # Load the first:
                        nodec = bdestslist[0][0]
                        weightbc = bdestslist[0][1]
                        # But if the first was nodea then switch to the second:
                        if nodec == nodea:
                            # The one we chose (the first) was nodea so instead we choose the second:
                            nodec = bdestslist[1][0]
                            weightbc = bdestslist[1][1]
                        if maze[nodec] == '.':
                            # Check that A->B->C AND C->B->A:
                            cdests = graph[nodec]
                            if nodeb in adests and nodec in bdests and nodeb in cdests and nodea in bdests:
                                # Step 2) Remove nodeb:
                                # a) add edge from nodea to nodec
                                # b) weight from nodea to nodec should be sum of the weights from nodea to nodeb and nodeb to nodec
                                graph[nodea][nodec] = weightab + weightbc
                                # And the same in reverse:
                                graph[nodec][nodea] = weightab + weightbc

                                # c) remove edge from nodea to nodeb
                                del graph[nodea][nodeb]
                                # And in reverse
                                del graph[nodeb][nodea]
                                # d) remove edge from nodeb to nodec
                                del graph[nodeb][nodec]
                                # And in reverse
                                del graph[nodec][nodeb]
                                return True
    # No simplifications
    return False

# Simplify until no more simplifications found!
while simplify(graph):
    pass

# Remove all orphan nodes:
snap = graph.copy().items()
for node, dests in snap:
    if len(dests) == 0:
        del graph[node]

# print(graph)
print("After simplification:", len(graph), "nodes")

stack = [ ([startmaze], 0) ] # [ ([pos], weight) ] Stack of (pathsofar, weightsofar) still to be explored:
# We start with just the start of the maze and zero weight
maxweight = 0 # The maximum weight of path found so far

step = 0
while stack:
    pathsofar, weightsofar = stack.pop()

    def get(pos):
        if pos in pathsofar:
            return "O"
        if pos in maze:
            return maze[pos]
        return '.'
    
    endpath = pathsofar[-1]
    while True:
        # ====================================================
        # Gather all the new ends:
        newends = [] # [(pos, weight)]
        for next, weight in neighbours_graph(endpath):
            if next == endmaze:
                maxweight = max(maxweight, weightsofar + weight)
            else:
                char = get(next)
                if char == '.' or char in dirs: # char == slope: # Either it's a path or it's the acceptable slope for the latest move:
                    newends.append((next, weight)) # We've found a new end to gather
                # else it's a forest '#' or part of the path so far 'O' so no go so don't do anything
        # ====================================================
        # Deal with the newends (if there are any!)
        if len(newends) == 0:
            # This is a deadend so we just forget this path
            break # The while True loop
        # Deal with any newends more than 1 (this won't do anything when we are running along a single track road!)
        while len(newends) > 1:
            # If there's more than one option then we push it to the stack:
            newend, weight = newends.pop()
            newpath = pathsofar.copy()
            newpath.append(newend)
            stack.append((newpath, weightsofar+weight))
        # Now we've only got one newend left so rather than push it to the stack we just carry on in this routine:
        # We get the last newend:
        newend, weight = newends.pop()
        # We add it to the path:
        pathsofar.append(newend)
        weightsofar += weight
        # And can update the endpath directly
        endpath = newend
        # And then just go round the "while True" loop again
        step += 1
        if step % 100000 == 0:
            print("stack=", len(stack), "path=", len(pathsofar), "maxweight=", maxweight)

result = maxweight
print(f"Result {'B' if partb else 'A'} = ", result)
