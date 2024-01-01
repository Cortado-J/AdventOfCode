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

def manhattan(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

sums = defaultdict(int)
infinites=set()
resultb = 0
for y in range(miny-1, maxy+2):
    for x in range(minx-1, maxx+2):
        pos = (x,y)
        dists = [(point, manhattan(pos, point)) for point in points]
        dists.sort(key=lambda a: a[1])
        nearest_dist = dists[0][1]
        secondnearest_dist = dists[1][1]
        nearest = dists[0][0]
        if nearest_dist != secondnearest_dist:
            sums[nearest] += 1
            if x == minx-1 or x == maxx+1 or y == miny-1 or y == maxy+1:
                infinites.add(nearest)
        sum_dist = sum([dist for point, dist in dists])
        if sum_dist < 10000:
            resultb += 1
    #     print((f"{pos}->{nearest}" +"              ")[:16], end="")
    # print()

area = max([ area for point, area in sums.items() if point not in infinites])
print("Result A: (max area) = ", area)
print("Result B: = ", resultb)