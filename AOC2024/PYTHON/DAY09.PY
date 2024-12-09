#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
text = text + "0"
max = len(text)*5

for part in ["A", "B"]:
    data = [-1] * max
    p = 0
    last = 0
    blocks = []
    for i in range(len(text)//2):
        l = int(text[i*2])
        block = (i,p,l)
        blocks.append(block)
        space = int(text[i*2+1])
        for x in range(l):
            data[p+x] = i
        last = p + l - 1
        p += (l+space)
    first = 0

    def gap(i, gaplen):
        for off in range(gaplen):
            if data[i+off] > -1:
                return False
        return True

    def firstgap(gaplen, max):
        for base in range(max):
            if gap(base, gaplen):
                return base
        return -1

    if part == "A":
        while True:
            if first >= last:
                break
            if data[first] > -1:
                first += 1
                continue
            if data[last] == -1:
                last -= 1
                continue
            data[first] = data[last]
            data[last] = -1
        total = 0
        for i, d in enumerate(data):
            if d >=0:
                total += i*d
        print("Part A:", total)

    else: # Part B:
        rev = blocks[::-1]
        for (id, blockstart, blocklen) in rev:
            if id % 100 == 0:
                print(".", end="", flush=True)
            g = firstgap(blocklen, blockstart)
            if g > -1:
                for i in range(blocklen):
                    data[g+i] = data[blockstart+i]
                    data[blockstart+i] = -1
        print()

        total = 0
        for i, d in enumerate(data):
            if d > 0:
                total += i*d
        print("Part B:", total)
