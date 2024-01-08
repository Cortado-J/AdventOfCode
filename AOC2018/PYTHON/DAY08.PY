#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
from collections import defaultdict
nums = [int(x) for x in text.split(' ')]

resulta = 0
def calc():
    global resulta
    result = 0
    childcount = nums.pop(0)
    metacount  = nums.pop(0)
    results = [calc() for _ in range(childcount)]
    for _ in range(metacount):
        meta = nums.pop(0)
        resulta += meta
        result += meta if childcount == 0 else (0 if not (0 < meta <= len(results)) else results[meta-1])
    return result

resultb = calc()
print("Result A = ", resulta)
print("Result B = ", resultb)
