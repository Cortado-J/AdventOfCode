#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')

def calc(arr):
    nums = [[int(i) for i in line if i.isdigit()] for line in arr]
    print(nums)
    first_and_last = [ 10*num[0] + num[-1] for num in nums]
    return sum(first_and_last)

# print(calc(lines))

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

lines2 = []
for line in lines:
    print("====================")
    print(line)
    linegather = ""
    for index in range(len(line)):
        if line[index].isdigit():
            linegather = linegather + line[index]
        else:
            for number, number_str in enumerate(numbers):
                if (line+"----------")[index:index+len(number_str)] == number_str:
                    linegather = linegather + str(number+1)
    print("->", linegather)
    lines2.append(linegather) 

print(calc(lines2))

