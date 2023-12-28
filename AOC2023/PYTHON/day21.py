from collections import Counter
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
height = len(lines)
width = len(lines[0])
dirs = {'N': (0,-1), 'S': (0,1), 'E': (1,0), 'W': (-1,0)}

rocks = set()
visit = {}
edges = {}
for y, row in enumerate(lines):
    for x, char in enumerate(row):
        pos = (x,y)
        if char == 'S':
            edges[pos] = char
        elif char == '#':
            rocks.add(pos)
            
def get(pos):
    modpos = (pos[0] % width, pos[1] % height)
    if modpos in rocks:
        return '#'
    if pos in edges:
        return edges[pos]
    if pos in visit:
        return visit[pos]
    return '.'

def getforshow(pos):
    modpos = (pos[0] % width, pos[1] % height)
    if modpos in rocks:
        return '#'
    if pos in edges:
        return 'E'
    if pos in visit:
        return visit[pos]
    return '.'

# global minx, miny, maxx, maxy
# def reset():
#     global minx, miny, maxx, maxy
#     minx = 0
#     miny = 0
#     maxx = 0
#     maxy = 0

# def update(pos):
#     global minx, miny, maxx, maxy
#     x = pos[0]
#     y = pos[1]
#     if x < minx:
#         minx = x
#     if x > maxx:
#         maxx = x
#     if y < miny:
#         miny = y
#     if y > maxy:
#         maxy = y

# def show():
#     reset()
#     for rock in rocks:
#         update(rock)
#     for vis in visit.keys():
#         update(vis)
#     print("------------------")
#     for y in range(miny,maxy+2):
#         for x in range(minx,maxx+2):
#             print(getforshow((x,y)),end="")
#         print()

def countste(forstep):
    counts = 0
    countt = 0
    for key, vis in visit.items():
        if vis == 'S':
            counts += 1
        if vis == 'T':
            countt += 1
    counte = len(edges)
    if forstep % 2 == 0:
        return counts + counte
    else:
        return countt + counte

tog = 1
P = [] # Polynomial
for step in range(1,26501365):
    # show()
    tog = 1 - tog
    ref = "S" if tog == 0 else "T"
    reft = "T" if tog == 0 else "S"
    
    # Keep copy of edges
    keepedges = edges.copy().items()

    # Move edges to visits
    for pos, val in edges.items():
        visit[pos] = val
    edges = {}

    # Work through all edges (the kept ones) and make any cells adjacent to edges
    # which are not in the existing visits into the new edges
    for pos, cur in keepedges:
        cur = get(pos)
        if cur == ref:
            for dir in dirs.values():
                new_pos = (pos[0]+dir[0], pos[1]+dir[1])
                new_modpos = ((pos[0]+dir[0]) % width, (pos[1]+dir[1]) % height)
                if new_modpos not in rocks:
                    if new_pos not in visit:
                        edges[new_pos] = reft
    # Keep result for part a
    if step == 64:
        resulta = countste(step)

    # Keep the three we need to calculate
    halfwithoutmiddle = int((width - 1)/2) # 65
    if step == halfwithoutmiddle or step == halfwithoutmiddle + width*4 or step == halfwithoutmiddle + width*8:
        P.append(countste(step))
        if step == halfwithoutmiddle + width*8:
            Q0 = P[1]-P[0]
            Q1 = P[2]-P[1]
            jump = Q1-Q0
            remaining_steps = int((26501365 - step) / (width*4))
            P = P[2]
            Q = Q1
            R = jump
            for _ in range(remaining_steps):
                Q += R
                P += Q
            resultb = P
            break
    
print("Result A = ", resulta)
print("Result B = ", resultb)
