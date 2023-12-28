from collections import Counter
from itertools import accumulate
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')

def poss(springs, target):
    MEMO = {}
    target_len = len(target)

    def poss_recurse(next_pos_to_fill, override, next_pos_target, damage_of_next_done, need_operational):
        params = (next_pos_to_fill, override, next_pos_target, damage_of_next_done, need_operational)
        if params in MEMO:
            return MEMO[params]
        def answer(x):
            MEMO[params] = x
            return x

        def damage():
            if next_pos_target == target_len:
                # We've hit a # when we don't need any!
                return 0
            if need_operational:
                # We needed an operational one
                return 0
            # Damage is fine:
            if damage_of_next_done+1 == target[next_pos_target]:
                # We've completed the damage group so move to next target:
                return answer(poss_recurse(next_pos_to_fill+1, None, next_pos_target+1, 0, True))
            else:
                # Stick with the same target but increase the damage for that target:
                return answer(poss_recurse(next_pos_to_fill+1, None, next_pos_target, damage_of_next_done+1, False))

        def operational():
            if damage_of_next_done > 0:
                # We're in the midst of a damage group but we've found an operational one so this not valid:
                return 0
            #  We have fulfilled the need for an operational one so can clear the flag and carry on:
            return answer(poss_recurse(next_pos_to_fill+1, None, next_pos_target, 0, False))

        if next_pos_to_fill == len(springs):
            # No more positions to fill
            if next_pos_target == target_len:
                # We've also no more targets to fulfil so we've found a valid sequence:
                # print(springs)
                # print(work)
                return 1
            else:
                # Although we've filled completely there's unfulfilled targets remaining so this is not a valid sequence:
                return 0

        next_char = override if override != None else springs[next_pos_to_fill]
        if next_char == '#':
            return damage()
        elif next_char == '.':
            return operational()
        else:
            return answer(
                poss_recurse(next_pos_to_fill, '#', next_pos_target, damage_of_next_done, need_operational)
                + poss_recurse(next_pos_to_fill, '.', next_pos_target, damage_of_next_done, need_operational)
                )

    return poss_recurse(0, None, 0, 0, False)

for partb in [False, True]:
    result = 0
    for i, line in enumerate(lines):
        bits = line.split(" ")        
        springs = bits[0]
        pattern = [int(x) for x in bits[1].split(",")]

        if partb:
            springs = springs+"?"+springs+"?"+springs+"?"+springs+"?"+springs
            pattern = pattern + pattern + pattern + pattern + pattern

        # print(i, "of", len(lines), springs, pattern, end="")
        score = poss(springs, pattern)
        # print(score)
        result += score
    print(f"Result {'B' if partb else 'A'} = ", result)

