import math
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')

seqs = [ [int(num) for num in line.split(" ")] for line in lines]

def get(x):
    diff = [x[n]-x[n-1] for n in range(1,len(x))]
    if all(v == 0 for v in diff):
        return 0
    return x[-1] + get(diff)

parta = 0
partb = 0
for seq in seqs:
    parta += get(seq)
    seq.reverse()
    partb += get(seq)

print(parta, partb)


