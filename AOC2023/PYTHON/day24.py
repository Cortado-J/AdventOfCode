=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
P = []
V = []
for line in lines:
    bits = line.split("@")
    pos = [int(v.strip()) for v in bits[0].split(",")]
    P.append(pos)
    vel = [int(v.strip()) for v in bits[1].split(",")]
    V.append(vel)

def intersects(p1, v1, p2, v2):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p1[0]+v1[0], p1[1]+v1[1]
    x3, y3 = p2[0], p2[1]
    x4, y4 = p2[0]+v2[0], p2[1]+v2[1]
    denominator = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if denominator == 0:
        # The two lines are parallel or coincident
        return None
    xnumerator = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))
    x = xnumerator/denominator
    
    ynumerator = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))
    y = ynumerator/denominator

    ok  = (x>x1 and x2>x1) or (x<=x1 and x2<=x1)
    ok2 = (x>x3 and x4>x3) or (x<=x3 and x4<=x3)
    if (not ok) or (not ok2):
        return None
    return (x,y)

N = len(P)
dmin, dmax = 200000000000000, 400000000000000
if N < 10:
    # We're testing!
    dmin, dmax = 7, 27
count = 0
print("----")
for i in range(N):
    for j in range(i+1,N):
        PA = (P[i][0], P[i][1])
        VA = (V[i][0], V[i][1])
        PB = (P[j][0], P[j][1])
        VB = (V[j][0], V[j][1])
        inter = intersects(PA, VA, PB, VB)
        # print(P[i],V[i],P[j],V[j],end=" ")
        if inter != None:
            ix, iy = inter
            inside = False
            if dmin <= ix <= dmax and dmin <= iy <= dmax:
                inside = True
                count += 1
        #     print(ix, iy, inside, end=" ")
        # print()

resulta = count
print("Result A=", resulta )

from z3 import *
# Position and velocity of the rock:
px = Int('px')
py = Int('py')
pz = Int('pz')
vx = Int('vx')
vy = Int('vy')
vz = Int('vz')
# Times at which each of the hail stones will be hit by the rock:
times = []
for index in range(N):
    # Create a variable for each impact time:
    times.append(Int(f'time{index}'))
    # We don't need to know those impact times but we need holders for thm as part of the set of equations

solver = Solver()
# Create all the simultaneous equations:
for stone in range(N):
  # Rock_posn + Rock_velocity * time_i == Stone_posn + Stone_velocity * time_i
  solver.add(px + vx * times[stone] == P[stone][0] + V[stone][0] * times[stone])
  solver.add(py + vy * times[stone] == P[stone][1] + V[stone][1] * times[stone])
  solver.add(pz + vz * times[stone] == P[stone][2] + V[stone][2] * times[stone])

if solver.check() == sat:
    model = solver.model()
    resultb = model.eval(px + py + pz)
    print("Result B=", resultb )
else:
    print("Result B: Solver couldn't find a solution")
