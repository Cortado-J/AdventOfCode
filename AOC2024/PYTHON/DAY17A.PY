#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
import math

# A = 729
# PROG = [0,1,5,4,3,0]

A = 59590048
PROG = [2,4,1,5,7,5,0,3,1,6,4,3,5,5,3,0]

# A = 117440
# PROG = [0,3,5,4,3,0]

B = 0
C = 0

IP = 0
LEN = len(PROG)
count = 0
while IP < LEN:
    count += 1
    if count > 10000:
        break
    opcode = PROG[IP]
    IP += 1
    operand = PROG[IP]
    IP += 1

    # The value of a literal operand is the operand itself.
    # For example, the value of the literal operand 7 is the number 7.
    liter = operand

    # Combo operands 0 through 3 represent literal values 0 through 3.
    # Combo operand 4 represents the value of register A.
    # Combo operand 5 represents the value of register B.
    # Combo operand 6 represents the value of register C.
    # Combo operand 7 is reserved and will not appear in valid programs.
    combo = [0,1,2,3,A,B,C,-7777][operand]   

    if opcode == 0:
        # The adv instruction (opcode 0) performs division. The numerator is the value in the A register.
        # The denominator is found by raising 2 to the power of the instruction's combo operand.
        # (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
        # The result of the division operation is truncated to an integer and then written to the A register.
        A = A // (2**combo)

    elif opcode == 1:
        # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal
        # operand, then stores the result in register B.
        B ^= liter

    elif opcode == 2:
        # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only
        # its lowest 3 bits), then writes that value to the B register.
        B = (combo % 8)

    elif opcode == 3:
        # The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is
        # not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this
        # instruction jumps, the instruction pointer is not increased by 2 after this instruction.
        if A > 0:
            IP = liter
            
    elif opcode == 4:
        # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores
        # the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
        B ^= C

    elif opcode == 5:
        # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that
        # value. (If a program outputs multiple values, they are separated by commas.)
        print(f"{combo % 8},",end="")

    elif opcode == 6:
        # The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored
        # in the B register. (The numerator is still read from the A register.)
        B = A // (2**combo)

    elif opcode == 7:
        # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored
        # in the C register. (The numerator is still read from the A register.)
        C = A // (2**combo)
print()


