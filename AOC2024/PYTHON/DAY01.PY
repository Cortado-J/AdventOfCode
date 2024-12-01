#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
left = sorted([int(line.split()[0]) for line in lines])
right = sorted([int(line.split()[1]) for line in lines])
parta, partb = 0, 0
for index, lef in enumerate(left):
    rig = right[index]
    diff = max(lef,rig) - min(lef,rig)
    parta += diff
    partb += lef * right.count(lef)

print("Part a = ", parta)
print("Part b = ", partb)
