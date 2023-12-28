#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.splitlines()

def priority(ch):
    if ord(ch) > 96:
        return ord(ch)-96
    else:
        return ord(ch)-64+26

def common(x,y):
    gather = ''
    for ch1 in x:
        for ch2 in y:
            if ch1 == ch2:
                gather += ch1
    return gather

def value(sack):
    return priority(common(sack[0:len(sack)//2], sack[len(sack)//2:len(sack)])[0])

parta = sum([value(line) for line in lines])
print(f"Day {daytext}: Part A = {parta}")

partb = 0
for base in range(0, len(lines), 3):
    firsttwo = common(lines[base], lines[base+1])
    all = common(firsttwo, lines[base + 2])
    partb += priority(all[0])

print(f"Day {daytext}: Part B = {partb}")
