#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
bricks = []
for line in lines:
    ends = line.split('~')
    a = [int(x) for x in ends[0].split(',')]
    b = [int(x) for x in ends[1].split(',')]
    bricks.append( (a,b) )
print("Bricks:\n", bricks)

# Sort by z:
bricks.sort(key=lambda x: x[0][2]) 

def iter(brick):
    a,b = brick
    for x in range(min(a[0],b[0]), max(a[0],b[0])+1):
        for y in range(min(a[1],b[1]), max(a[1],b[1])+1):
            for z in range(min(a[2],b[2]), max(a[2],b[2])+1):
                yield (x,y,z)

used = {}
for brickind, brick in enumerate(bricks):
    for block in iter(brick):
        used[block] = brickind

def used_remove_brick(brickind):
    for pos in iter(bricks[brickind]):
        del used[pos]

def used_add_brick(brickind):
    for pos in iter(bricks[brickind]):
        used[pos] = brickind

def down(brick, n):
    a,b = brick
    return ([a[0],a[1],a[2]-n],[b[0],b[1],b[2]-n])

def isequal(p,q):
    return p[0] == q[0] and p[1] == q[1] and p[2] == q[2]

def isin(point,brick):
    for pos in iter(brick):
        if isequal(pos, point):
            return True
    return False

def overlap(brick1,brick2):
    for pos in iter(brick1):
        if isin(pos, brick2):
            return True
    return False

def overlapsany(brick, excluding_index):
    for pos in iter(brick):
        if pos in used and used[pos] != excluding_index:
            return True
    return False

def underground(brick):
    return brick[0][2] <= 0 or brick[1][2] <= 0

def drop(brickind): # Drop brick with the given index and return the number of cells it drops by
    tryfall = bricks[brickind]
    drop = 0
    while True:
        dow = down(tryfall, drop+1)
        if underground(dow) or overlapsany(dow, brickind):
            if drop > 0:
                used_remove_brick(brickind)
                bricks[brickind] = down(tryfall, drop)
                used_add_brick(brickind)
                # if drop > 1:
                #     print("Drop", brickind, "by", drop)
            return drop
        drop += 1

def gravity(): # Apply gravity to all bricks and return number of bricks which drop
    drops = set()
    falling = True
    while falling:
        falling = False
        for indfall in range(len(bricks)):
            brickdrops = drop(indfall)
            if brickdrops > 0:
                drops.add(indfall)
                falling = True
                break
    return len(drops)

def show():
    for brick in bricks:
        print(brick)
    print("- - - - - - - - -")
    
dummy = gravity()

safe = 0
totaldrops = 0
keep_bricks = bricks.copy()
keep_used = used.copy()
for ind in range(len(bricks)):
    bricks = keep_bricks.copy()
    used = keep_used.copy()

    used_remove_brick(ind)
    bricks[ind][0][2] = -10000 # Put brick underground
    bricks[ind][1][2] = -10000 # Put brick underground
    used_add_brick(ind)

    drops = gravity()
    totaldrops += drops
    if drops == 0:
        safe += 1
    print(ind, "of", len(bricks), "Bricks dropped = ", drops)
    
print("Result A = ", safe)
print("Result B = ", totaldrops)