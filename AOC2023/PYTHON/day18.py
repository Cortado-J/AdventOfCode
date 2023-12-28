#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
dirs = {'U': (0,-1), 'D': (0,1), 'R': (1,0), 'L': (-1,0)}

for part in [1,2]: 
    loop = [] # Array of points
    x = 0
    y = 0
    border = 0
    area = 0
    for line in lines:
        loop.append((x,y))
        # R 6 (#70c710)
        bits = line.split(" ")
        dir = 'X'
        dist = 0
        if part == 1:
            dir = bits[0]
            dist = int(bits[1])
        else:
            col = bits[2][1:-1]
            dir = {0:'R', 1:'D', 2:'L', 3:'U'}[int(col[-1])]
            dist = int(col[1:-1] ,16)
        border += dist
        if dir == 'R': area -= y*dist
        if dir == 'L': area += y*dist
        x += dirs[dir][0] * dist
        y += dirs[dir][1] * dist
    assert x == 0 and y == 0

    result = area + border/2 + 1 # By Pick's therem the answer is area + border/2 + 1
    result = int(result)
    if part == 1:
        print("Result A = ", result)
    else:
        print("Result B = ", result)
