#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
resulta = 0
resultb = 0
cave = {}
rocks = set()
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        pos = (x,y)
        if char == "O":
            cave[pos] = '.'
            rocks.add(pos) 
        else:
            cave[pos] = char
print(cave, rocks)
H = len(lines)
W = len(lines[0])

def get(pos):
    if 0<=pos[0]<W and 0<=pos[1]<H:
        return 'O' if pos in rocks else cave[pos]
    else:
        return '#' # Pretend there's immovable rocks around the edge!
    
def tilt(dir):
    change = True
    while change:
        change = False
        for rock in rocks:
            look = (rock[0]+dir[0],rock[1]+dir[1])
            if get(look) == '.':
                change = True
                rocks.remove(rock)
                rocks.add(look)

def load():
    result = 0
    for rock in rocks:
        result += H-rock[1]
    return result

tilt((0,-1))
resulta = load()
print(resulta)

def rockhash(r):
    result = ""
    for x in range(W):
        for y in range((H)):
            result = result + ("O" if (x,y) in r else ".")
    return result

history = {}
loads = {}
cycle = 0
found = None
while True:
    tilt((0,-1))
    tilt((-1,0))
    tilt((0,1))
    tilt((1,0))
    cycle += 1
    print(cycle)
    dhash = rockhash(rocks)
    if dhash in history:
        found = history[dhash]
        break
    history[dhash] = cycle
    loads[cycle] = load()
base = found
repeat = cycle
same_as_last = base + (1000000000-base)%(repeat-base)
resultb = loads[same_as_last]
print(resultb)
