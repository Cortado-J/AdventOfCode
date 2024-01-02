#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
# from collections import defaultdict
lines = text.splitlines()
# print(lines)
# position=< 9,  1> velocity=< 0,  2>
posx, posy, velx, vely = [], [], [], []
size = len(lines)
for line in lines:
    pos = line.split('<')[1].split('>')[0].split(',')
    posx.append(int(pos[0]))
    posy.append(int(pos[1]))

    vel = line.split('<')[2].split('>')[0].split(',')
    velx.append(int(vel[0]))
    vely.append(int(vel[1]))

def limits(t):
    miny = 10000000
    maxy = -10000000
    minx = 10000000
    maxx = -10000000
    for i in range(size):
        y = posy[i] + vely[i] * t 
        miny = min(miny, y)
        maxy = max(maxy, y)
        x = posx[i] + velx[i] * t 
        minx = min(minx, x)
        maxx = max(maxx, x)
    return miny, maxy, minx, maxx

miny, maxy, minx, maxx = limits(0)
height = maxy-miny+1
t = 1
lims = None
while True:
    miny, maxy, minx, maxx = limits(t)
    newheight = maxy-miny+1
    # print(t, "==>", newheight)
    if newheight > height:
        break
    height = newheight
    t += 1

# print(miny, maxy, minx, maxx ,height)
chosentime = t-1

print("Result A = ")
view = set()
for i in range(size):
    view.add((posx[i] + velx[i] * chosentime, posy[i] + vely[i] * chosentime))

for y in range(miny, maxy+1):
    for x in range(minx, maxx+1):
        print('#' if (x,y) in view else '.', end='')
    print()

print()
print("Result B = ", chosentime)





