#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
lines = open(file_path).read().splitlines()
#=============================================================
print(lines)
# lines = ["80871224585914546619083218645595"]

data =  lines[0]

def mult(position, element):
    return [0,1,0,-1][int(( (position+1) / (element+1) ) % 4)]

def stepit(input):
    array = [int(digit) for digit in input] # Convert to Ints

    output = []
    for newPosition in range(len(array)):
        sum = 0
        for oldPosition in range(len(array)):
            multiplier = mult(oldPosition, newPosition)
            bit = array[oldPosition] * multiplier
            # print("Value: \(array[oldPosition]) which is from Position: \(oldPosition) : Element: \(newPosition) creates multiplier \(multiplier) -> \(bit)")
            sum += bit
        lastDigit = sum % 10 if sum > 0 else (-sum) % 10
        # print("Sum is \(sum) which has last digit \(lastDigit)")
        output.append(lastDigit)
        # print("===========")
    return output

def parta():
    working = data
    # print(working)
    for step in range(1,100+1):
        working = stepit(working)
        # print(working)
    
    return ''.join(map(str, working[:8]))

def fft_efficient(input_signal, phases):
    signal_length = len(input_signal)
    signal = [int(digit) for digit in input_signal] * 10000
    
    # Get the message offset
    offset = int(input_signal[:7])


    # Only consider the part of the signal starting from the offset
    signal = signal[offset:]
    
    for _ in range(phases):
        # Compute the new signal using reverse prefix sum
        new_signal = [0] * len(signal)
        total = 0
        for i in range(len(signal) - 1, -1, -1):
            total += signal[i]
            new_signal[i] = total % 10
        signal = new_signal
    
    # Get the first eight digits of the final output list
    return ''.join(map(str, signal[:8]))

def partb():
    return fft_efficient(data, 100)

print("Part A: ",parta())
print("Part B: ",partb())
