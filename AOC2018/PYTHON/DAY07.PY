#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
from collections import defaultdict
lines = text.splitlines()
net = defaultdict(lambda: set())
steps = set()
for line in lines:
    words = line.split(' ')
    stepbefore = words[1]
    stepafter  = words[7]
    steps.add(stepbefore)
    steps.add(stepafter)
    net[stepafter].add(stepbefore)

for part in [1,2]:
    todo = steps.copy()
    order = ''
    workers = 1 if part == 1 else 5
    doing = [None for _ in range(workers)] # Jobs being done by workers (index is the worker number)
    workleft = [0 for _ in range(workers)] # Number of seconds left for this job (index is the worker number)

    def befores_all_done(x):
        for before in net[x]:
            if before in todo or before in doing:
                return False
        return True

    second = 0
    while todo or sum(workleft) > 0:
        for worker in range(workers):
            if workleft[worker] > 0:
                workleft[worker] -= 1
                if workleft[worker] == 0:
                    order += doing[worker]
                    doing[worker] = None
        for worker in range(workers):
            if doing[worker] == None:
                available = [step for step in todo if befores_all_done(step)]
                if available:
                    # Get first in alphabetical order
                    available.sort()
                    next = available[0]
                    doing[worker] = next
                    workduration = 1 if part == 1 else ord(next)-ord('A')+1+60
                    workleft[worker] = workduration
                    todo.remove(next)
        second += 1
        # print(second, doing, workleft, order)
    if part == 1:
        print("Result A =", order)
    else:
        print("Result B =", second-1)
