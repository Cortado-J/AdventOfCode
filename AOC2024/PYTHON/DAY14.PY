#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
import time
start_time = time.time()
# p=0,4 v=3,-3
# p=6,3 v=-1,-3
lines = text.split('\n')
robots = []
maxx, maxy = -1000000000, -1000000000
for line in lines:
    bs = line.split(" ")
    ps=bs[0].split(",")
    px,py = int(ps[0][2:]),int(ps[1])
    vs=bs[1].split(",")
    vx,vy = int(vs[0][2:]),int(vs[1])
    robots.append(((px,py), (vx,vy)))
    maxx, maxy = max(maxx,px), max(maxy,py)
gen = 100
sx,sy=(maxx+0) // 2, (maxy+0)//2
q00,q01,q10,q11=0,0,0,0
for ((px,py),(vx,vy)) in robots:
    x = (px + vx*gen) % (maxx+1)
    y = (py + vy*gen) % (maxy+1)
    if x < sx:
        if y < sy:
            q00 += 1
        if y > sy:
            q01 += 1
    elif x > sx:
        if y < sy:
            q10 += 1
        if y > sy:
            q11 += 1
parta = q00*q01*q10*q11
print("Part A:", parta)

gen = 0
lasta = 0
adjacents = 0
while adjacents < 100:
    for r,((px,py),(vx,vy)) in enumerate(robots):
        x = (px + vx) % (maxx+1)
        y = (py + vy) % (maxy+1)
        robots[r] = ((x,y),(vx,vy))
    posns = [p for(p,v) in robots]
    robsorted = sorted(posns, key=lambda pair: (pair[0], pair[1]))
    adjacents = 0
    lasty = 0
    for (x,y) in robsorted:
        if y-lasty == 1:
            adjacents += 1
        lasty = y
    gen += 1

partb = gen
print("Part B:", partb)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
