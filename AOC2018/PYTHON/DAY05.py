#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
from datetime import datetime, timedelta
from collections import defaultdict

def swap(x):
    switcher = ord('a') - ord('A')
    return chr(ord(x) ^ 32)

def countit(polymer):
    gather = ''
    for ch in polymer:
        if len(gather) > 0 and gather[-1] == swap(ch):
            gather = gather[:-1]
        else:
            gather = gather + ch
        # print(ch, gather)
    return len(gather)

resulta = countit(text)
print("Result A = ", resulta)

resultb = 1000000
for ch in 'abcdefghijklmnopqrstuvwxyz':
   resultb = min(resultb, countit(text.replace(ch, '').replace(swap(ch),'')))
print("Result B = ", resultb)


