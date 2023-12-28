import math
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
sections = text.split('\n\n')
path = sections[0].strip()
net = {}
for line in sections[1].split("\n"):
    bits = line.split("=")
    node  = bits[0].strip()
    left  = bits[1].strip()[1:4]
    right = bits[1].strip()[6:9]
    # print(node, left, right)
    net[node] = (left, right)

# Part A
step = 0
index = 0
start = "AAA"
current = start
while current != "ZZZ":
    direction = 0 if path[index] == "L" else 1
    index += 1
    if index >= len(path):
        index = 0
    step += 1
    current = net[current][direction]

resulta = step
print("Part a = ", resulta)

#  Part B
loops = []
for node in net.keys():
    if node[-1] == "A":
        # We've found a start so lets look for Zs in it's path:
        zeds = {}
        done = False
        current = node
        step = 0
        path_index = 0
        while not done:
            direction = 0 if path[path_index] == "L" else 1
            path_index += 1
            if path_index >= len(path):
                path_index = 0
            step += 1

            current = net[current][direction]

            if current[-1] == "Z":
                record = (current, path_index)
                if record in zeds:
                    last_step = zeds[record]
                    this_step = step
                    loop_length = this_step - last_step
                    # print(node, last_step, this_step, loop_length, zeds)
                    loops.append(loop_length)
                    done = True
                else:
                    zeds[record] = step

lcd = math.lcm(*loops)
resultb = lcd
print("Part b = ", resultb)
