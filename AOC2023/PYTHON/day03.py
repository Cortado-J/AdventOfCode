#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')

num_rows = len(lines)
num_cols = len(lines[0])
def cell(row,col):
    if row < 0 or row >= num_rows:
        return "."
    if col < 0 or col >= num_cols:
        return "."
    return lines[row][col]

def is_symbol(x):
    return x not in '.0123456789'

gear_dict = {} # Lookup from gear coordinates to array of adjacent numbers
resulta = 0
for row, whole_row in enumerate(lines):
    whole_row = whole_row + "."  # Add a . to ensure numbers are ended
    in_number = False
    number_start = 0
    number = 0
    for col, char in enumerate(whole_row):
        if in_number:
            if char.isdigit():
                # We're staying ni a number
                number = number * 10 + int(char)
            else:
                # We've just ended a number
                number_end = col
                next_to_symbol = False
                print("- - - - - - - - - - - - -")
                print(row,col,number_start,number_end)
                for row_hunt in range(row-1, row+2):
                    for col_hunt in range(number_start-1, number_end+1):
                        print("...", row_hunt, col_hunt, cell(row_hunt, col_hunt))
                        if is_symbol(cell(row_hunt, col_hunt)):
                            next_to_symbol = True
                            if (row_hunt, col_hunt) not in gear_dict:
                                gear_dict[(row_hunt, col_hunt)] = [number]
                            else:
                                gear_dict[(row_hunt, col_hunt)].extend([number])

                if next_to_symbol:
                    resulta += number
                in_number = False
        else:
            if char.isdigit():
                # We're starting a number
                in_number = True
                number_start = col
                number = int(char)
            else:
                # We've staying outside a number
                in_number = False

print(resulta)
# We've also gathered all possible gears in the gear dictionary.
# The ones we want are all those with exactly two neighbours - i.e. with an array of length 2
gear_ratios = [numbers[0] * numbers[1] for numbers in gear_dict.values() if len(numbers) == 2]
resultb = sum(gear_ratios)
print(resultb)
