#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')

def get(s,ch):
    ss = s.split(",")
    return (int(ss[0].split(ch)[1]), int(ss[1].split(ch)[1]))

for part, offset in [("A",0), ("B",10000000000000)]:
    tokens = 0
    for line in lines:
        if len(line) > 10:
            if line[7] == "A":
                ax, ay = get(line[10:],"+")
            elif line[7] == "B":
                bx, by = get(line[10:],"+")
            elif line[0] == "P":
                px, py = get(line[7:],"=")
                px += offset
                py += offset
                det = ay*bx - ax*by
                if det != 0: # Check determinant is non zero
                    anum = py * bx - px * by
                    bnum = px * ay - py * ax
                    if anum % det == 0 and bnum % det == 0: # Check integer solution
                        a = anum // det
                        b = bnum // det
                        tokens += a*3 + b
    print(f"Part {part}:", tokens)
