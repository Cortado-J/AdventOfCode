#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
sections = text.split('\n\n')
pats = [p.strip() for p in sections[0].split(',')]
dess = sections[1].split('\n')
maxpat = max(len(pat) for pat in pats)
memo = {}
def make(des):
    if des in memo:
        return memo[des]
    lendes = len(des)
    if lendes == 0:
        return 1
    count = 0
    for lenpat in range(1, min(maxpat,lendes)+1):
        if lenpat <= lendes:
            if des[:lenpat] in pats:
                count += make(des[lenpat:])
    memo[des] = count
    return count

parta, partb = 0, 0
for des in dess:
    count = make(des)
    partb += count
    if count > 0:
        parta += 1 

print("Part A:", parta)
print("Part B:", partb)
