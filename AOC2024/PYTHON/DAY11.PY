#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================

memo = {}

def pluto(n, turns):
    if turns == 0:
        return 1
    if (n,turns) in memo:
        return memo[(n,turns)]

    def next(x):
        return pluto(x, turns-1)

    if n == 0:
        r = next(1)
    else:
        s = str(n)
        lens = len(s)
        if lens % 2 == 0:
            cut =lens//2
            r = next(int(s[:cut]))+ next(int(s[cut:]))
        else:
            r = next(n * 2024)
    memo[(n,turns)] = r
    return r

def calc(xs, t):
    return sum(pluto(x, t) for x in xs)

nums = [2, 54, 992917, 5270417, 2514, 28561, 0, 990]

parta = calc(nums, 25)
print("Part A:", parta)

partb = calc(nums, 75)
print("Part B:", partb)
