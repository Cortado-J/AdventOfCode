#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')

dirs = {'N': (0,-1), 'S': (0,1), 'E': (1,0), 'W': (-1,0)}
links = {'|': 'NS', '-': 'EW', 'L': 'NE', 'J': 'NW', '7': 'SW', 'F': 'SE', '.': ''}
crosses = {'|': 1, '-': 0, 'L': -0.5, 'J': 0.5, '7': -0.5, 'F': 0.5, '.': 0, 'S': None}

land = {}
start = None
height = len(lines)
width = len(lines[0])
for y, row in enumerate(lines):
    for x, char in enumerate(row):
        land[(x,y)] = char
        if char == 'S':
            start = (x,y)

def move_dir(pos, compass):
    dir = dirs[compass]
    return (pos[0]+dir[0], pos[1]+dir[1])

def split(pos):
    if pos not in land:
        return []
    return [move_dir(pos, link) for link in links[land[pos]]]

seconds = []
for compass in 'NESW':
    candidate_second = move_dir(start, compass)
    if start in split(candidate_second):
        seconds.append(candidate_second)

second = seconds[0]
step = 1
current = second
last = start
path = {start: land[start], second: land[second]} # Save the path
while land[current] != 'S':
    two = split(current)
    next = two[0] if two[1] == last else two[1]
    path[next] = land[next]
    last = current
    current = next
    step += 1

print("part a:", step/2)

def crossings_range(xfrom, xto, y):
    if xfrom == xto:
        return 0
    cross_count = 0
    for x in range(xfrom, xto):
        if (x,y) in path:
            spot = path[(x,y)]
            if spot == 'S':
                return None
            cross_count += crosses[spot]
    return cross_count    

def crossings(pos):
    if pos in path:
        return None # shouldn't choose!
    y = pos[1]
    cross_count = crossings_range(0, pos[0], y)
    if cross_count == None: # Because there's an S to the left of the position!
        cross_count = crossings_range(pos[0]+1, width, y)
    return cross_count

inside = 0
for y in range(height):
    for x in range(width):
        if (x,y) in path:
            print(path[(x,y)], end="")
        else:
            if crossings((x,y)) % 2 == 0:
                print("O", end="")
            else:
                print("I", end="")
                inside += 1
    print()
print(inside)
