#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
parta, partb = 0, 0

import re
pattern = r'mul\((0|[1-9][0-9]{0,2}),(0|[1-9][0-9]{0,2})\)'
matches = re.findall(pattern, text)
muls = [int(x) * int(y) for x,y in matches]
parta = sum(muls)
print(parta)
print("========================")
# text = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

token_regex = r"do\(\)|don't\(\)|mul\((0|[1-9][0-9]{0,2}),(0|[1-9][0-9]{0,2})\)"

enabled = True
for match in re.finditer(token_regex, text):
    token = match.group(0)
    if token == "do()":
        enabled = True
    elif token == "don't()":
        enabled = False
    elif token.startswith("mul") and enabled:
        x, y = map(int, re.findall(r'\d+', token))
        partb += x * y
print("========================")
print(partb)
print("========================")

