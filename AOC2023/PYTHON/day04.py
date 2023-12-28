#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
def intify(ls):
    return [int(item.strip()) for item in ls if item != '']

resulta = 0
counts = [1 for _ in lines]
num_cards = len(lines)
for line in lines:
    colon_split = line.split(":")
    card_num = int(colon_split[0][4:].strip())
    base_offset = card_num-1
    pipe_split = colon_split[1].split("|")
    card = intify(pipe_split[0].split(" "))
    mynums = intify(pipe_split[1].split(" "))
    winning = set(card).intersection(mynums)
    number_of_wins = len(winning)
    points = math.floor(pow(2, number_of_wins-1))
    resulta += points

    for add_offset in range(number_of_wins):
        target = base_offset + add_offset+1
        if target < num_cards:
            counts[target] += counts[base_offset]
    
print(resulta)
print(sum(counts))
