# ip 2 means that R2 is the instruction pointer
def terminate(part):
    R4 = 0x10000
    R3 = 0x2137C0
    R3seen = set()
    lastR3 = None
    while True:
        R3 += (R4 & 0xFF)
        R3 *= 0x1016B
        R3 &= 0xFFFFFF
        if R4 < 0x100:
            if part == "A":
                return R3
            if R3 in R3seen:
                return lastR3            
            R3seen.add(R3)
            lastR3 = R3
            R4 = R3 | 0x10000
            R3 = 0x2137C0
            continue
        R4 = R4 // 256

parta = terminate("A")
print(f"Part A = {parta}")

partb = terminate("B")
print(f"Part B = {partb}")
