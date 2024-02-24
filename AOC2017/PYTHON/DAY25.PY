#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
rows = text.splitlines()
# Begin in state A.
start_state = rows[0].split(" ")[-1][0]
# Perform a diagnostic checksum after 6 steps.
steps = int(rows[1].split(" ")[-2])
turing = {}
for state_index in range(3,len(rows),10):
    state = rows[state_index].split(" ")[-1][0]
    plan = [
        (
            int(rows[state_index+2].split(" ")[-1][0])
            ,1 if rows[state_index+3].split(" ")[-1] == "right." else -1
            ,rows[state_index+4].split(" ")[-1][0]
        ),
        (
            int(rows[state_index+6].split(" ")[-1][0])
            ,1 if rows[state_index+7].split(" ")[-1] == "right." else -1
            ,rows[state_index+8].split(" ")[-1][0]
        )
    ]
    turing[state] = plan

print(turing)

# The state is kept as the set of indexes of all the ones in the current state
ones = set()
position = 0
state = start_state
for step in range(steps):
    (write_value, position_delta, next_state) = turing[state][1 if position in ones else 0]
    if write_value == 1:
        ones.add(position)
    else:
        ones.discard(position)
    position += position_delta
    state = next_state

# In state A:
#   If the current value is 0:
#     - Write the value 1.
#     - Move one slot to the right.
#     - Continue with state B.
#   If the current value is 1:
#     - Write the value 0.
#     - Move one slot to the left.
#     - Continue with state B.

resulta = len(ones)
resultb = 777

print("Result Part A = ", resulta)
print("Result Part B = ", resultb)
