#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
input = text
# input="bvwbjplbgvbhsrlpgdmjqwftvncz"

def start(length):
    for i in range(length - 1, len(input)):
        s = input[i - length + 1:i + 1]
        if len(set(s)) == length:
            return (i + 1)

parta = start(4)
partb = start(14)
print(f"Day {daytext}: Part A = {parta}")
print(f"Day {daytext}: Part B = {partb}")
