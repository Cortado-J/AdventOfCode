from collections import deque
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.splitlines()
nums = [int(line) for line in lines]

def solve(part):
    tups = [(index, num * (811589153 if part == 'b' else 1)) for index, num in enumerate(nums)]
    d = deque(tups)
    size = len(d)
    for _ in range(10 if part == 'b' else 1):
        for i in range(size):
            while not d[0][0] == i:  # Find our number
                d.append(d.popleft())
            put = d.popleft()
            newpos = put[1] % (size - 1)
            d.insert(newpos, put)
    while not d[0][1] == 0:  # Find zero:
        d.append(d.popleft())
    return sum([d[1000 % size][1], d[2000 % size][1], d[3000 % size][1]])

parta = solve('a')
print(f"Day {daytext}: Part A = {parta}")
partb = solve('b')
print(f"Day {daytext}: Part B = {partb}")
