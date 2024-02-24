#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
rows = text.splitlines()
components = []

for row in rows:
    bits = row.split("/")
    component = (int(bits[0]), int(bits[1]))
    components.append(component)

longestlength = 0
strongestlongest = 0

def strongest(lastport, remain, sofar):
    global longestlength
    global strongestlongest
    maxstrength = 0
    maxsofar = sofar
    for index, rem in enumerate(remain):
        for pairindex in [0,1]:
            if lastport == rem[pairindex]:
                otherendofport = rem[1-pairindex]
                remcopy = remain.copy()
                next = remcopy.pop(index)
                nexttrail = sofar.copy()
                nexttrail.append(next)
                strength = rem[0] + rem[1]
                strong, trail = strongest(otherendofport, remcopy, nexttrail)
                strong += strength
                if strong > maxstrength:
                    maxstrength = strong
                    maxsofar = trail
                traillength = len(trail)
                if traillength > longestlength:
                    longestlength = traillength
                    strongestlongest = 0
                if traillength == longestlength:
                    strengthofit = 0
                    for pair in trail:
                        strengthofit += (pair[0] + pair[1])
                    strongestlongest = max(strongestlongest, strengthofit)
                
    return maxstrength, maxsofar

resulta, msf = strongest(0, components, [])
resultb = strongestlongest

print("Result Part A = ", resulta)
print("Result Part B = ", resultb)
