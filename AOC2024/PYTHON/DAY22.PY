#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')

def secret(n):
    a = ((n * 64) ^ n) % 16777216
    b = ((a // 32) ^ a) % 16777216
    return ((b * 2048) ^ b) % 16777216

firstbananas = {}
parta = 0
size = 2000
for line in lines:
    start = int(line)
    n = start
    secrets = [n]
    diffs = [None]
    for index in range(size):
        n = secret(n)
        secrets.append(n)
        diffs.append((secrets[index+1]%10)-(secrets[index]%10))
    parta += n
    first = set()
    for i in range(len(secrets)-3):
        sl = (diffs[i],diffs[i+1],diffs[i+2],diffs[i+3])
        if sl not in first:
            first.add(sl)
            if sl not in firstbananas:
                firstbananas[sl] = 0
            firstbananas[sl] += (secrets[i+3] % 10)
print(f"Part A: {parta}")

partb = max(firstbananas.values())
print(f"Part B: {partb}")
