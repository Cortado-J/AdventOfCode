#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')

dirs = {'N': (0,-1), 'S': (0,1), 'E': (1,0), 'W': (-1,0)}
map = {'.':  {'N': 'N',  'S': 'S',  'E': 'E',  'W': 'W'},
       '/':  {'N': 'E',  'S': 'W',  'E': 'N',  'W': 'S'},
       '\\': {'N': 'W',  'S': 'E',  'E': 'S',  'W': 'N'},
       '|':  {'N': 'N',  'S': 'S',  'E': 'NS', 'W': 'NS'},
       '-':  {'N': 'EW', 'S': 'EW', 'E': 'E',  'W': 'W'}}

space = {} # { (x,y) : mirror }
height = len(lines)
width = len(lines[0])
for y, row in enumerate(lines):
    for x, char in enumerate(row):
        space[(x,y)] = char

def beam(pos, dir):
    tried = set() # {(x,y),direction} to keep track of what position/direction combinations we have tried 
    needed = set() # As above but the ones that we need to try
    energized = set() # {(x,y)} to keep track of what positions we have visited
    needed.add((pos,dir))
    while len(needed) > 0:
        pos, dir = needed.pop()
        if (pos, dir) in tried:
            continue
        tried.add((pos, dir))
        energized.add(pos)

        mirror = space[pos]
        newdirs = map[mirror][dir]
        for newdir in newdirs:
            newdir_val = dirs[newdir]
            newpos = (pos[0]+newdir_val[0], pos[1]+newdir_val[1])
            if 0 <= newpos[0] < width and 0 <= newpos[1] < height:
                needed.add((newpos, newdir))
    return(len(energized))

resulta = beam((0,0),'E')
print("Result A = ", resulta)

resultb = 0
for x in range(width):
    top = beam((x, 0),"S")
    bot = beam((x, height-1), "N")
    resultb = max(resultb, top, bot)

for y in range(height):
    left = beam((0, y), "E")
    rig = beam((width-1, y), "W")
    resultb = max(resultb, left, rig)
print("Result B = ", resultb)
