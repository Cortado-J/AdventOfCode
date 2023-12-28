#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.splitlines()

ta = 0
tb = 0
for line in lines:
    elves = line.split(',')
    a = elves[0].split('-')
    b = elves[1].split('-')
    ab = int(a[0])
    ae = int(a[1])
    bb = int(b[0])
    be = int(b[1])
    if ((ab >= bb and ae <= be) or (bb >= ab and be <= ae)):
        ta += 1
    if max(ab, bb) <= min(ae, be):
        tb += 1

print(f"Day {daytext}: Part A = {ta}")
print(f"Day {daytext}: Part B = {tb}")
