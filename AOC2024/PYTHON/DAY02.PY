#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
parta, partb = 0, 0

def safe(s):
    print(levels)
    firstmove = s[1] - s[0]
    if firstmove == 0:
       return 0
    for i in range(len(s)-1):
        move = s[i+1] - s[i]
        print("compare",s[i+1],s[i],move)
        if firstmove > 0:
            if move < 1 or move > 3:
               return 0
        else:
            if move < -3 or move > -1:
               return 0
    return 1

def skipsafe(s):
    if safe(s) == 1:
        return 1
    for skip in range(len(s)):
        skipped = s[:skip] + s[skip+1:]
        if safe(skipped) == 1:
            return 1
    return 0

for report in lines:
    levels = [int(x) for x in report.split()]
    parta += safe(levels)
    partb += skipsafe(levels)

print("Part a = ", parta)
print("Part b = ", partb)
