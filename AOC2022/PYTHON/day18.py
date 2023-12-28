import copy
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.splitlines()

cubes = [[int(p) for p in xyz.split(',')] for xyz in lines]

def connect(a, b):
    if (a[0] == b[0] and a[1] == b[1] and abs(a[2] - b[2]) == 1) or (
            a[0] == b[0] and abs(a[1] - b[1]) == 1 and a[2] == b[2]) or (
            abs(a[0] - b[0]) == 1 and a[1] == b[1] and a[2] == b[2]):
        return True
    return False

covered = 0
num = len(cubes)
for i, a in enumerate(cubes):
    for j in range(i, num):
        b = cubes[j]
        if connect(a, b):
            covered += 2

parta = 6 * num - covered
print(f"Day {daytext}: Part A = {parta}")


# Array of sets each of which is a joined area
areas = []


def hash(p):
    return p[0] * 10000 + p[1] * 100 + p[2]


def unhash(h):
    result = (h // 10000, (h // 100) % 100, h % 100)
    return result


def touchings(area):
    alist = list(area)
    num = len(alist)
    result = 0
    for i, a in enumerate(alist):
        ua = unhash(a)
        for j in range(i, num):
            b = alist[j]
            ub = unhash(b)
            if connect(ua, ub):
                result += 1
    return result


# Find area with point or None
def getarea(hp):
    for index, ar in enumerate(areas):
        if hp in ar:
            return index
    return None


def neigh(p):
    return [(p[0] - 1, p[1], p[2]), (p[0] + 1, p[1], p[2]), (p[0], p[1] - 1, p[2]), (p[0], p[1] + 1, p[2]),
            (p[0], p[1], p[2] - 1), (p[0], p[1], p[2] + 1)]


edges = set([hash(p) for p in cubes])

for x in range(0, 21):
    for y in range(0, 21):
        for z in range(0, 21):
            p = (x, y, z)
            hp = hash(p)
            if not hp in edges:  # If an edge then ignore
                areasofneighbours = set()  # So that we ignore duplicates (if connected to two other cells of same area then that's no extra info
                for n in neigh(p):
                    na = getarea(hash(n))
                    if na is not None:
                        areasofneighbours.add(na)
                # Now areasofneighbours is an array of neighbours of the current cube
                if len(areasofneighbours) == 0:
                    # We need to create a new area:
                    newarea = set()
                    newarea.add(hp)
                    areas.append(newarea)
                else:
                    # We have one or more joined areas:
                    alist = list(areasofneighbours)
                    # Add the point to the first area:
                    ato = alist[0]
                    areas[ato].add(hp)
                    if len(alist) > 1:  # and if there's any more areas connected to the cube
                        # We want to join them into one bigger area so transfer them all into the first area
                        for afrom in alist[1:]:  # Loop over additional areas
                            for newpoint in areas[afrom]:
                                # Transferring points to new area
                                areas[ato].add(newpoint)
                            areas[afrom] = set()  # Make old area empty (We could be tidy and remove them but hey!)

outside = areas[getarea(hash((20, 20, 20)))]
volumeofinsides = 0
touchingsofinsides = 0
for index, area in enumerate(areas):
    if not area == outside and len(area):
        volumeofinsides += len(area)
        touch = touchings(area)
        touchingsofinsides += touch
        # print(f"Area {index} has volume {len(area)} and touchings {touch}.  Area is: {area}")

partb = parta - volumeofinsides * 6 + touchingsofinsides * 2
print(f"Day {daytext}: Part B = {partb}")
