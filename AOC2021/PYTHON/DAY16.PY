#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
bits = bin(int(text, 16))[2:]  # [2:] to remove the '0b' prefix
leadingzeroesneeded = len(text) * 4 - len(bits)
bits = ("0" * leadingzeroesneeded) + bits

index = 0 # Next bit to read

def get(length):
    global index
    if length == 0: return 0
    val = int(bits[index:index+length],2)
    index += length
    return val

# return sum of versions, sum of values
def packet():
    global index
    global indent
    version = get(3)
    versiontotal = version
    typeid  = get(3)
    result = None
    if typeid == 4: # Literal value
        value = 0
        running = True
        while running:
            running = get(1) == 1
            value = value * 16 + get(4)
        result = value
    else: # Non-literal
        def recurse():
            nonlocal result
            nonlocal versiontotal
            version, value = packet()
            versiontotal += version
            if typeid == 0: # Sum packet:
                if result == None: result = 0
                result += value
            elif typeid == 1: # Product packet:
                if result == None: result = 1
                result *= value
            elif typeid == 2: # Minimum packet:
                if result == None: result = 1000000000
                result = min(result, value)
            elif typeid == 3: # Maximum packet:
                if result == None: result = -1000000000
                result = max(result, value)
            elif typeid == 5: # Greater than packet:
                if result == None: result = value
                else: result = 1 if result > value else 0 
            elif typeid == 6: # Less than packet:
                if result == None: result = value
                else: result = 1 if result < value else 0 
            elif typeid == 7: # Equal to packet:
                if result == None: result = value
                else: result = 1 if result == value else 0 

        lengthtypeid = get(1)
        if lengthtypeid == 0:
            totallengthofsubpackets = get(15)
            base = index
            while index < base + totallengthofsubpackets:
                recurse()
        else:
            numberofsubpackets = get(11)
            for _ in range(numberofsubpackets):
                recurse()
    return versiontotal, result

resulta, resultb = packet()
print("Result A = ", resulta)
print("Result B = ", resultb)
