def memory_game(starting_numbers, target_turn):
    # Dictionary to store the last time each number was spoken
    last_spoken = {}
    
    # Initialize the game with the starting numbers, except the last one
    for i, num in enumerate(starting_numbers[:-1]):
        last_spoken[num] = i + 1
    
    # The last number spoken so far
    last_number = starting_numbers[-1]

    # Start from the turn after the starting numbers
    for turn in range(len(starting_numbers), target_turn):
        if last_number in last_spoken:
            # Calculate the age (difference between the current turn and the last time it was spoken)
            next_number = turn - last_spoken[last_number]
        else:
            # If the last number was spoken for the first time, the next number is 0
            next_number = 0
        
        # Update the last time the last_number was spoken
        last_spoken[last_number] = turn
        
        # Move to the next number
        last_number = next_number

    return last_number

# Example usage with the given starting numbers
starting_numbers = [0, 3, 6]
result = memory_game(starting_numbers, 2020)
print(f"The 2020th number spoken is: {result}")

# Test with other starting numbers
numbers = [0,1,4,13,15,12,16]
print(f"Starting numbers {numbers}")

def do_part(part, n):
    result = memory_game(numbers, n)
    print(f"Part {part}: the {n}th number spoken is: {result}")

do_part(1, 2010)
do_part(2, 30000000)
