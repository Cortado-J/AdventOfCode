#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
parta, partb = 0,0

grid = {}
ylen = len(lines)
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        grid[(x,y)] = char
    xlen = len(line)
positions = grid.keys()
freqs = set(grid.values())
freqs.remove('.')

visita = set()
visitb = set()
for freq in freqs:
    points = [k for k, v in grid.items() if v == freq]
    n = len(points)
    for a in range(n):
        for b in range(a):
            pa = points[a]
            pb = points[b]
            offsetx = pb[0] - pa[0]
            offsety = pb[1] - pa[1]
            for k in range(max(xlen,ylen)):
                pc = (pb[0] + offsetx * k, pb[1] + offsety * k)
                pd = (pa[0] - offsetx * k, pa[1] - offsety * k)
                if pc in positions:
                    if k == 1:
                        visita.add(pc)
                    visitb.add(pc)
                if pd in positions:
                    if k == 1:
                        visita.add(pd)
                    visitb.add(pd)
print("Part A:", len(visita))
print("Part B:", len(visitb))
