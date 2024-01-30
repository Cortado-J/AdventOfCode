#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
rows = text.splitlines()
code = []
regs = {"a":0, "b":0, "c":0, "d":0, "e":0, "f":0, "g":0, "h":0}
for row in rows:
    bits = row.split(" ")
    code.append(tuple(bits))
# print(code)
# print(regs)
current = 0
mulcount = 0
while 0 <= current < len(code):
    C, X, Y = code[current]
    Xval = regs[X] if X in regs else int(X)
    Yval = regs[Y] if Y in regs else int(Y)
    # print(f"{current =}, {C =}, {X =}, {Y =}", end="")
    if C == "set":
        # set X Y sets register X to the value of Y.
        regs[X] = Yval
    elif C == "sub":
        # sub X Y decreases register X by the value of Y.
        regs[X] -= Yval
    elif C == "mul":
        # mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
        regs[X] *= Yval
        mulcount += 1
    elif C == "jnz":
        # jnz X Y jumps with an offset of the value of Y, but only if the value of X is not zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)
        current = current + (0 if Xval == 0 else Yval-1)
    else:
        #  Ignore others
        pass
    # print(f" ==> ", end="")
    # print(f"{regs =}, ", end="")
    # print()
    current += 1
resulta = mulcount
print(f"Result A = {resulta}")

# Translating the code into python we have:
# mulcount = 0
# a,b,c,d,e,f,g,h = 0,0,0,0,0,0,0,0
# b, c = 93, 93
# if a != 0:
#     b = 109300
#     mulcount += 1
#     c = b + 17000
# for x in range(b, c+1, 17):
#     found = 1
#     for d in range(2, b):
#         for e in range(2, b):
#             mulcount += 1
#             if d*e == b:
#                 found = 0
#     if found == 0:
#         h += 1
# print(mulcount)

#  Which is counting the number of factorisable numbers in a certain range with a step of 17

def factorisable(number):
    if number < 2: return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0: return True
    return False

# Part B is to count the numbers from b, b+17, b+17*2 up to b+17000 which are not prime
count = 0
for n in range(109300, 109300 + 17000 + 1, 17):
    if factorisable(n):
        count += 1
resultb = count
print(f"Result B = {resultb}")
