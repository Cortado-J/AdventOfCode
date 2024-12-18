#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
PROG = [2,4,1,5,7,5,0,3,1,6,4,3,5,5,3,0]

def calc(witha):
    A, B, C, OUT = witha, 0, 0, []
    while True:
        B = (A % 8)  # MOD 8
        B ^= 5  # SWITCH B'S BITS 0 AND 2
        C = A >> B   # MOVE A RIGHT BY B BITS AND PUT IN C
        A = A >> 3   # MOVE A RIGHT BY 3 BITS
        B ^= 6  # SWITCH B'S BITS 1 AND 2
        B ^= C # SWITCH B'S BITS ACCORDING TO C
        OUT.append(B % 8)
        if A == 0:
            # if witha % 1 == 0:
            #     print(f"{witha},{A},{B},{C},{OUT}")
            return OUT

def solve():
    base = 0
    size = len(PROG)
    for i in range(size-1, -1, -1):
        for trya in range(base, base + (8 ** (size - i))):
            out = calc(trya)
            if out == PROG[i:]:
                if len(out) == size:
                    return trya
                base = trya * 8
                break

parta = ",".join(map(str, calc(59590048)))
print(f"Part A: {parta}")

partb = solve()
print(f"Part B: {partb}")

def disassemble():
    for index in range(len(PROG)):
        if index % 2 == 0:
            opcode = PROG[index]
            operand = PROG[index+1]
            print(f"{index}: ",end="")

            # The value of a literal operand is the operand itself.
            # For example, the value of the literal operand 7 is the number 7.
            liter = operand

            # Combo operands 0 through 3 represent literal values 0 through 3.
            # Combo operand 4 represents the value of register A.
            # Combo operand 5 represents the value of register B.
            # Combo operand 6 represents the value of register C.
            # Combo operand 7 is reserved and will not appear in valid programs.
            combo = "0123ABC#"[operand]

            if opcode == 0:
                # The adv instruction (opcode 0) performs division. The numerator is the value in the A register.
                # The denominator is found by raising 2 to the power of the instruction's combo operand.
                # (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
                # The result of the division operation is truncated to an integer and then written to the A register.
                print(f"A = A >> {combo}")

            elif opcode == 1:
                # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal
                # operand, then stores the result in register B.
                print(f"B = B XOR {liter}")

            elif opcode == 2:
                # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only
                # its lowest 3 bits), then writes that value to the B register.
                print(f"B = {combo} % 8 (bottom 3 bits)") 

            elif opcode == 3:
                # The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is
                # not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this
                # instruction jumps, the instruction pointer is not increased by 2 after this instruction.
                print(f"IF A > 0 JUMP TO {liter}") 
                    
            elif opcode == 4:
                # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores
                # the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
                print(f"B = B XOR C") 

            elif opcode == 5:
                # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that
                # value. (If a program outputs multiple values, they are separated by commas.)
                print(f"OUTPUT {combo} % 8 (bottom 3 bits)")

            elif opcode == 6:
                # The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored
                # in the B register. (The numerator is still read from the A register.)
                print(f"B = A >> {combo}")

            elif opcode == 7:
                # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored
                # in the C register. (The numerator is still read from the A register.)
                print(f"C = A >> {combo}")

