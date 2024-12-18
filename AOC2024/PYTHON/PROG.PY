# A = n
# B = 0
# C = 0
# 0: B = A % 8
# 2: B = B XOR 5
# 4: C = A >> B
# 6: A = A >> 3
# 8: B = B XOR 6
# 10: B = B XOR C
# 12: OUTPUT B % 8 (bottom 3 bits)
# 14: IF A > 0 JUMP TO 0

# A = n
# B = 0
# C = 0

# 0: B = (A % 8)  # MOD 8
# 2: B = B XOR 5  # SWITCH B'S BITS 0 AND 2
# 4: C = A >> B   # MOVE A RIGHT BY B BITS AND PUT IN C
# 6: A = A >> 3   # MOVE A RIGHT BY 3 BITS
# 8: B = B XOR 6  # SWITCH B'S BITS 1 AND 2
# 10: B = B XOR C # SWITCH B'S BITS ACCORDING TO C

# 12: OUTPUT B % 8 (bottom 3 bits)
# 14: IF A > 0 JUMP TO 0
PROG = [2,4,1,5,7,5,0,3,1,6,4,3,5,5,3,0]
PROG = [0,3,5,4,3,0]

TRYA = 0
while True:
    out = []
    A, B, C = TRYA, 0, 0

    while A > 0:
        B = (A % 8)  # MOD 8
        B ^= 5  # SWITCH B'S BITS 0 AND 2
        C = A >> B   # MOVE A RIGHT BY B BITS AND PUT IN C
        A = A >> 3   # MOVE A RIGHT BY 3 BITS
        B ^= 6  # SWITCH B'S BITS 1 AND 2
        B ^= C # SWITCH B'S BITS ACCORDING TO C
        out.append(B % 8)

    if TRYA % 10000 == 0:
        print(TRYA,out,PROG)
    if out == PROG:
        print(TRYA,out,PROG)
        break
    TRYA += 1

