#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
parta, partb = 0,0

def get_ops(num, base, length):
    ops = ""
    for _ in range(length):
        ops += "*+|"[num % base]
        num //= base
    return ops

def canmake(test, vals, part):
    numvals = len(vals)
    base = 2 if part == "A" else 3
    for bin in range(base ** (numvals-1) ):
        result = vals[0]
        ops = get_ops(bin, base, numvals-1)
        for index in range(numvals-1):
            nextval = vals[index+1]
            op = ops[index]
            if op == "*":
                result *= nextval
            if op == "+":
                result += nextval
            if op == "|":
                result = int(f"{result}{nextval}")
        if result == test:
            return True
    return False

for part in ["A","B"]:
    total = 0
    for line in lines:
        bits = line.split(': ')
        test = int(bits[0])
        vals = [int(x) for x in bits[1].split(' ')]
        if canmake(test, vals, part):
            total += test
    print(f"Part {part}: ", total)
