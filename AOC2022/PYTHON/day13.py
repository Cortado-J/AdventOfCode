import copy
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
pairs = text.split('\n\n')

def isnotlist(x):
    return not hasattr(x, "__len__")


def inorder(left, right):
    # print(f"Comparing: {left} with {right}")
    # If both values are integers, the lower integer should come first.
    if isnotlist(left) and isnotlist(right):
        # If the left integer is lower than the right integer, the inputs are in the right order.
        if left < right:
            return True
        # If the left integer is higher than the right integer, the inputs are not in the right order.
        if left > right:
            return False
        # Otherwise, the inputs are the same integer; continue checking the next part of the input.
        return None

    # If exactly one value is an integer, convert the integer to a list which contains that integer as its only value,
    # then retry the comparison.
    # For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2);
    # the result is then found by instead comparing [0,0,0] and [2].
    if isnotlist(left):
        left = [left]
    if isnotlist(right):
        right = [right]

    # If both values are lists, compare the first value of each list, then the second value, and so on.
    while len(left) > 0 and len(right) > 0:
        comp = inorder(left[0], right[0])
        if comp != None:
            # We have a result:
            return comp
        left = left[1:]
        right = right[1:]

    # If the left list runs out of items first, the inputs are in the right order.
    if len(left) == 0 and len(right) > 0:
        return True

    # If the right list runs out of items first, the inputs are not in the right order.
    if len(left) > 0 and len(right) == 0:
        return False

    # If the lists are the same length and no comparison makes a decision about the order,
    # continue checking the next part of the input.
    return None


index = 0
total = 0
packets = []
for pair in pairs:
    index += 1
    lines = pair.splitlines()
    left = eval(lines[0])
    right = eval(lines[1])
    # Part A
    if inorder(left, right):
        total += index
    # Keep for Part B
    packets.append(left)
    packets.append(right)

parta = total
print(f"Day {daytext}: Part A = {parta}")

divider1 = [[2]]
divider2 = [[6]]
packets += [divider1, divider2]

def bubbleSort(a):
    for i in range(len(a)):
        for j in range(len(a)-i-1):
            if not inorder(a[j], a[j+1]):
                a[j], a[j+1] = a[j+1], a[j]

bubbleSort(packets)
index1 = packets.index(divider1)+1
index2 = packets.index(divider2)+1
decoderkey = index1 * index2
partb = decoderkey
print(f"Day {daytext}: Part B = {partb}")
