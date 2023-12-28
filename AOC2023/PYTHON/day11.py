#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
xs = []
ys = []
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "#":
            xs.append(x)
            ys.append(y)
xs.sort()
ys.sort()
number = len(xs)
dist = 0
expansion = 1000000
for i in range(1, number):
    dx = xs[i] - xs[i-1]
    if dx > 1:
        for inc_i in range(i, number):
            xs[inc_i] += (dx - 1)*(expansion-1)
    dist += i * (number-i) * (xs[i] - xs[i-1])

    dy = ys[i] - ys[i-1]
    if dy > 1:
        for inc_i in range(i, number):
            ys[inc_i] += (dy - 1)*(expansion-1)
    dist += i * (number-i) * (ys[i] - ys[i-1])
print("part a", dist)
