#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n\n')

flows = {}
for line in lines[0].split("\n"):
    bits = line.split("{")
    name = bits[0]
    rules_txt = bits[1][0:-1].split(",")
    rules = []
    # print(name)
    for rule in rules_txt:
        bits = rule.split(":")
        if len(bits) == 1:
            # It's the final condition so force to be true:
            rating = "a"
            condition = ">"
            amount = -1
            result = bits[0]
        else:
            cond = bits[0]
            rating = cond[0]
            condition = cond[1]
            amount = int(cond[2:])
            result = bits[1]
        # print("   ", rating, condition, amount, result)
        rules.append((rating, condition, amount, result))
    flows[name] = rules

parts = [dict([(att.split("=")[0], int(att.split("=")[1])) for att in line[1:-1].split(",")]) for line in lines[1].split("\n")]

resulta = 0
for part in parts:
    next = "in"
    while next not in 'AR':
        for rating, condition, amount, result in flows[next]:
            flip = 1 if condition == "<" else -1  
            if part[rating] * flip < amount * flip:
                next = result
                break
    if next == 'A':
        resulta += sum(part.values())
print("Result A = ", resulta)

resultb = 0
rating_max = 4000
full_rang = dict([ (rating, (1, rating_max+1)) for rating in 'xmas'])
# print(full_rang)

import math

def combos(rang, flow, flow_step):
    if flow == 'R':
        return 0
    if flow == 'A':
        range_lens = [rang[rating][1] - rang[rating][0] for rating in 'xmas']
        return math.prod(range_lens)
    rating, condition, amount, result = flows[flow][flow_step]
    rating_range = rang[rating]
    min_rang = rating_range[0]
    max_rang = rating_range[1]

    if condition == '<':
        if max_rang < amount:
            # Condition met so do this step
            return combos(rang, result, 0)
        elif min_rang > amount:
            # Condition not met so go to next step:
            return combos(rang, flow, flow_step+1)
        else:
            # amount to split the range:
            ranga = rang.copy()
            ranga[rating] = (rating_range[0], amount)

            rangb = rang.copy()
            rangb[rating] = (amount, rating_range[1])

            return combos(ranga, result, 0) + combos(rangb, flow, flow_step+1)
    else: # condition == '>':
        if min_rang > amount:
            # Condition met so do this step
            return combos(rang, result, 0)
        elif max_rang < amount:
            # Condition not met so go to next step:
            return combos(rang, flow, flow_step+1)
        else:
            # amount to split the range:
            ranga = rang.copy()
            ranga[rating] = (rating_range[0], amount+1)

            rangb = rang.copy()
            rangb[rating] = (amount+1, rating_range[1])

            return combos(rangb, result, 0) + combos(ranga, flow, flow_step+1)

resultb = combos(full_rang, "in", 0)    
print("Result B = ", resultb)
