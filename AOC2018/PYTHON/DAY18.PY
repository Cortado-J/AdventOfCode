import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
from collections import defaultdict

lines = text.splitlines()
W = len(lines[0])
H = len(lines)
land = text

def offset(pos):
    return pos[0]+(W+1)*pos[1]

def get(pos):
    (x, y) = pos
    if 0 <= x < W and 0 <= y < H:
        return land[offset(pos)]
    return '.'

def gettreelumberall():
    stats = defaultdict(int)
    for x in range(W):
        for y in range(H):
            pos = (x,y)
            stats[get(pos)] += 1
    return stats['|'], stats['#']

def gettreelumberneigh(pos):
    stats = defaultdict(int)
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if dx != 0 or dy != 0:
                stats[get((pos[0]+dx,pos[1]+dy))] += 1
    return stats['|'], stats['#']

def gen(pos):
    this = get(pos)
    tree, lumber = gettreelumberneigh(pos)
    if this == '.' and tree >= 3:
        this = '|'
    elif this == '|' and lumber >= 3:
        this = '#'
    elif this == '#' and (lumber < 1 or tree < 1):
        this = '.'
    # Otherwise leave as it is!
    return this

def generate():
    global land
    next = ''
    for y in range(0, H):
        for x in range(0, W):
            pos = (x,y)
            next += gen(pos)
        next += '\n'
    land = next

def show(msg):
    print("----------------")
    print(msg)
    print(land)

# show("Initial state:")
for g in range(10):
    generate()
    show(f"After {g+1} minute(s):")
tree, lumber = gettreelumberall()
print("Result A = ", tree*lumber)

memo = {}
loopstart = None
g = 0
land = text
print("Takes a few seconds...")
end = 1000000000
for g in range(end):
    endgen = None
    generate()
    # show(f"After {g} minute(s):")
    # if g % 100 == 0: print(g)
        # show(f"After {g} minute(s):")
    if land in memo:
        loopstart = memo[land]        
        loopend = g
        endgen = loopend + (end-loopstart) % (loopend-loopstart)
    if g == endgen:
        break
    memo[land] = g

tree, lumber = gettreelumberall()
print("Result B = ", tree*lumber)
