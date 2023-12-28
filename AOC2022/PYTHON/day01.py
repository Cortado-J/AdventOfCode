#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n\n')
elves = []
for section in lines:
    count = 0
    for calories in section.splitlines():
        count += int(calories)
    elves.append(count)
elves.sort(reverse=1)

parta = elves[0]
print(f"Day {daytext}: Part A = {parta}")
partb = sum(elves[0:3])
print(f"Day {daytext}: Part B = {partb}")
