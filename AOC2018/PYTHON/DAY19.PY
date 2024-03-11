#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
# #ip 0
# seti 5 0 1

lines = text.splitlines()
ipreg = int(lines.pop(0).split(' ')[1])
# print(ipreg)
# print(lines)

code = []
for line in lines:
    op = line.split(" ")
    opcode = (op[0], int(op[1]), int(op[2]), int(op[3]))
    code.append(opcode)

# print(code)

def exec(regs, instruction):
    R = regs.copy()
    (OP, A, B, C) = instruction
    if   OP == 'addr': R[C] = R[A] + R[B]
    elif OP == 'addi': R[C] = R[A] + B
    elif OP == 'mulr': R[C] = R[A] * R[B]
    elif OP == 'muli': R[C] = R[A] * B
    elif OP == 'banr': R[C] = R[A] & R[B]
    elif OP == 'bani': R[C] = R[A] & B
    elif OP == 'borr': R[C] = R[A] | R[B]
    elif OP == 'bori': R[C] = R[A] | B
    elif OP == 'setr': R[C] = R[A]
    elif OP == 'seti': R[C] = A
    elif OP == 'gtir': R[C] = 1 if A > R[B] else 0
    elif OP == 'gtri': R[C] = 1 if R[A] > B else 0
    elif OP == 'gtrr': R[C] = 1 if R[A] > R[B] else 0
    elif OP == 'eqir': R[C] = 1 if A == R[B] else 0
    elif OP == 'eqri': R[C] = 1 if R[A] == B else 0
    elif OP == 'eqrr': R[C] = 1 if R[A] == R[B] else 0
    return R

ip = 0
regs = [0,0,0,0,0,0]
count = 0
r1 = regs[1]
r3 = regs[3]
while 0 <= ip < len(code):
    regs[ipreg] = ip
    # print(regs,end="")
    instruction = code[ip]
    # print(instruction, end="")
    regs = exec(regs, instruction)
    ip = regs[ipreg]
    ip += 1
    if ip == 6:
        count += 1
        if r1 != regs[1]:
            print(f"count={count}, ip={ip}, regs={regs} R1 CHANGED")
            r1 = regs[1]
        if r3 != regs[3]:
            print(f"count={count}, ip={ip}, regs={regs} R3 CHANGED")
            r3 = regs[3]
            if r3 - r1 > 2:
                regs[3] += 1
        # if count % 1000000 == 0:
        #     print(f"count={count}, ip={ip}, regs={regs} COUNT MULT OF 1,000,000")
        if count > 1000 and regs[1] - regs[2] > 200000:
            # We're gonna fudge it!
            # print(f"Fudge: count += 1000000, R2 += 125000")
            count += 1000000
            regs[2] += 125000

resulta = regs[0]
print("Result A = ", resulta)

print("For Part B, it would be possible to change the starting register 0 to 1")
print("but the code would take a very long time indeed!!")

# We need to understand the code:
disassemble = {
"addr": "R{C} = R{A} + R{B}", 
"addi": "R{C} = R{A} + {B}", 
"mulr": "R{C} = R{A} * R{B}", 
"muli": "R{C} = R{A} * {B}", 
"banr": "R{C} = R{A} & R{B}", 
"bani": "R{C} = R{A} & {B}", 
"borr": "R{C} = R{A} | R{B}", 
"bori": "R{C} = R{A} | {B}", 
"setr": "R{C} = R{A}", 
"seti": "R{C} = {A}", 
"gtir": "R{C} = 1 if {A} > R{B} else 0", 
"gtri": "R{C} = 1 if R{A} > {B} else 0", 
"gtrr": "R{C} = 1 if R{A} > R{B} else 0", 
"eqir": "R{C} = 1 if {A} == R{B} else 0", 
"eqri": "R{C} = 1 if R{A} == {B} else 0", 
"eqrr": "R{C} = 1 if R{A} == R{B} else 0"
}

def subst(text, trans):
    work = text
    for txtfrom, txtto in trans:
        work = work.replace(txtfrom, txtto)
    return work

fix = [("R3", "f"), ("R2", "g"), ("R5 =", "JUMP")]
for row, (OP, A, B, C) in enumerate(code):
    dis = disassemble[OP].format(A=A,B=B,C=C)
    dis = subst(dis, fix)
    if dis[0:4] == "R5 =":
        dis = "JUMP" + dis[4:] + " + 1"
    if dis == "JUMP R5 * R5" and row*row > len(code):
        dis = "STOP!"
    if dis[0:9] == "JUMP R5 +":
        dis = "JUMP REL " + dis[10:] + " + 1"
    print(row, dis)

# BY LOOKING AT THIS CODE WE CAN DEDUCE THAT IT IS EQUIVALENT TO:
for part in ["A", "B"]:
    #  Setup
    R0,R1,R2,R3,R4,R5 = (0 if part == "A" else 1),0,0,0,0,0
    #  Code:
    R1 = 2*2*19*11 + 22+9 # Which is 867
    if R0 == 1:
        R1 = 2*2*19*11 + 22+9 + (30 * (29 + 27*28)) * 14 * 32 # Which is 10551267
        R0 = 0
    print(f"Running part {part}")
    print("Start with regs 0 to 5 as: ", R0,R1,R2,R3,R4,R5)
    for f in range(1, R1+1):
        for g in range(1, R1+1):
            R4 = f * g
            if R4 == R1:
                R0 += f
    print(R0)
# Part B is still too slow
# Inspection of the code brings out the meaning - it is equivalent to calculating:
#  For PART A: The sum of the Factors of 867 which is 1228
#  For PART B: The sum of the Factors of 10551267 which is 15285504
# The factors were looked up at: https://www.calculatorsoup.com/calculators/math/factors.php
# and added together!
