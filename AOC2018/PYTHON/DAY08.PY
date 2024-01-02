#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
from collections import defaultdict
nums = [int(x) for x in text.split(' ')]
print(nums)

tree = []
resulta = 0
work = nums.copy()

def loadnext():
    global resulta
    childcount = work.pop(0)
    metacount  = work.pop(0)
    for childindex in range(childcount):
        loadnext()
    for metaindex in range(metacount):
        meta = work.pop(0)
        print(meta)
        resulta += meta

loadnext()

print(resulta)

work = nums.copy()
def calc():
    childcount = work.pop(0)
    metacount  = work.pop(0)
    results = []
    for childindex in range(childcount):
        results.append(calc())
    result = 0
    for metaindex in range(metacount):
        meta = work.pop(0)
        result += 0 if meta == 0 else (meta if childcount == 0 else results[meta-1])
    return result

print(calc())
