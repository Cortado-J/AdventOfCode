#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.splitlines()
from collections import defaultdict
points = set()
near = defaultdict(lambda: '.')
minx = 1000000
miny = 1000000
maxx = 0
maxy = 0

for line in lines:
    bits = line.split(',')
    x = int(bits[0])
    y = int(bits[1])
    pos = (x,y)
    points.add(pos)
    near[pos] = pos
    minx = min(minx, x)
    miny = min(miny, y)
    maxx = max(maxx, x)
    maxy = max(maxy, y)

print(f"{minx} <= x <= {maxx} and {miny} <= y <= {maxy}")
size = max(maxx-minx+1, maxy-miny+1)

def huntaround(pos, dist):
    for dx in range(-dist,dist+1):
        absdy = dist-abs(dx)
        for dy in ([0] if absdy == 0 else [-absdy,absdy]): # To make it manhattan
            yield (pos[0]+dx,pos[1]+dy)

def pointsaround(pos, dist):
    for hunt in huntaround(pos, dist):
        if hunt in points:
            yield hunt

def nearestpoints(pos, maxdist):
    for dist in range(0,maxdist+1):
        atthisdist = list(pointsaround(pos, dist))
        if atthisdist:
            return atthisdist
    return []

# print(nearestpoints((5,0),50))

sums = defaultdict(int)
infinites=set()
for y in range(miny-1,maxy +2):
    print(f"{y} in range({miny-1})")
    for x in range(minx-1,maxx +2):
        pos = (x,y)
        nearest = nearestpoints(pos, size*2)
        if len(nearest) == 1:
            nearestpoint = nearest[0]
            sums[nearestpoint] += 1
            if x == minx-1 or x == maxx+1 or y == miny-1 or y == maxy+1:
                infinites.add(nearestpoint)
        # print((f"{pos}->{nearestpoint}" +"              ")[:16], end="")
    # print()

print("==== infinites:")
print(infinites)

print("==== sums:")
print(sums)

area = max([ area for point, area in sums.items() if point not in infinites])
print("Result A: (max area) = ", area)
