#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split(',')

def hash(s):
    current = 0
    for char in s:
        # Determine the ASCII code for the current character of the string.
        ascii = ord(char)
        # Increase the current value by the ASCII code you just determined.
        current += ascii
        # Set the current value to itself multiplied by 17.
        # Set the current value to the remainder of dividing itself by 256.
        current = (current * 17) % 256
    return current

print("HASH", hash("HASH"))
resulta = 0
for line in lines:
    h = hash(line)
    print(line, h)
    resulta += h
print("Part A = ", resulta)

boxes = [[] for _ in range(256)]
focals = [[] for _ in range(256)]
print(boxes)
for line in lines:
    if line[-1] == "-":
        label = line[0:-1]
        box = hash(label)
        print(f"Remove label {label} from box {box}")
        if label in boxes[box]:
            slot = boxes[box].index(label)
            del boxes[box][slot]
            del focals[box][slot]
    else:
        label = line[0:-2]
        box = hash(label)
        focal = int(line[-1])
        print(f"Add label {label} with focal length {focal} to box {box}")
        if label in boxes[box]:
            slot = boxes[box].index(label)
            focals[box][slot] = focal
        else:
            boxes[box].append(label)
            focals[box].append(focal)
print("=========================")
resultb = 0
for box in range(256):
    if boxes[box] != []:
        print(boxes[box])
        print(focals[box])
        for slot, lens in enumerate(boxes[box]):
            power = (box+1) * (slot+1) * (focals[box][slot])
            resultb += power
print("Part B = ", resultb)
