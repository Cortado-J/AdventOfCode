#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
# print(text)

lines = text.splitlines()

# all below from ChatGPT o1-mini

import sys
from typing import List, Tuple
import itertools

def parse_snailfish_number(s: str) -> List[Tuple[int, int]]:
    """Parses a snailfish number string into a list of (value, depth) tuples."""
    number = []
    depth = 0
    i = 0
    while i < len(s):
        if s[i] == '[':
            depth += 1
            i += 1
        elif s[i] == ']':
            depth -= 1
            i += 1
        elif s[i] == ',':
            i += 1
        elif s[i].isdigit():
            # Read the full number
            num = 0
            while i < len(s) and s[i].isdigit():
                num = num * 10 + int(s[i])
                i += 1
            number.append((num, depth))
        else:
            # Should not reach here
            raise ValueError(f"Unexpected character: {s[i]}")
    return number

def add_snailfish_numbers(a: List[Tuple[int, int]], b: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Adds two snailfish numbers by concatenating them and increasing their depth."""
    return [(val, depth + 1) for val, depth in a + b]

def explode(number: List[Tuple[int, int]]) -> bool:
    """Performs one explode operation if possible. Returns True if an explosion occurred."""
    for i in range(len(number) - 1):
        val_left, depth_left = number[i]
        val_right, depth_right = number[i + 1]
        if depth_left > 4 and depth_left == depth_right:
            # Add to the left
            if i > 0:
                number[i - 1] = (number[i - 1][0] + val_left, number[i - 1][1])
            # Add to the right
            if i + 2 < len(number):
                number[i + 2] = (number[i + 2][0] + val_right, number[i + 2][1])
            # Replace the exploded pair with 0 at depth -1
            number[i] = (0, depth_left - 1)
            del number[i + 1]
            return True
    return False

def split(number: List[Tuple[int, int]]) -> bool:
    """Performs one split operation if possible. Returns True if a split occurred."""
    for i in range(len(number)):
        val, depth = number[i]
        if val >= 10:
            left = val // 2
            right = val - left
            # Replace current number with two new numbers at depth +1
            number[i:i+1] = [(left, depth + 1), (right, depth + 1)]
            return True
    return False

def reduce_snailfish_number(number: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Reduces the snailfish number by repeatedly exploding and splitting."""
    while True:
        if explode(number):
            continue
        if split(number):
            continue
        break
    return number

def magnitude(number: List[Tuple[int, int]]) -> int:
    """Calculates the magnitude of the snailfish number."""
    # Work with a copy to avoid modifying the original list
    num = number.copy()
    while len(num) > 1:
        # Find the deepest pair
        max_depth = max(depth for _, depth in num)
        for i in range(len(num) - 1):
            if num[i][1] == num[i + 1][1] == max_depth:
                # Calculate magnitude
                mag = 3 * num[i][0] + 2 * num[i + 1][0]
                # Replace the pair with its magnitude at depth -1
                num[i] = (mag, max_depth - 1)
                del num[i + 1]
                break
    return num[0][0]

def parse_input(lines: List[str]) -> List[List[Tuple[int, int]]]:
    """Parses input lines into a list of snailfish numbers in flat list format."""
    return [parse_snailfish_number(line.strip()) for line in lines]

def add_all_snailfish_numbers(numbers: List[List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    """Adds all snailfish numbers in the list sequentially."""
    current_sum = numbers[0]
    for number in numbers[1:]:
        current_sum = add_snailfish_numbers(current_sum, number)
        current_sum = reduce_snailfish_number(current_sum)
    return current_sum

def find_largest_magnitude(numbers: List[List[Tuple[int, int]]]) -> int:
    """Finds the largest magnitude from adding any two distinct snailfish numbers."""
    max_mag = 0
    for a, b in itertools.permutations(numbers, 2):
        # Make copies to prevent modifying original numbers
        a_copy = a.copy()
        b_copy = b.copy()
        sum_ab = add_snailfish_numbers(a_copy, b_copy)
        reduce_snailfish_number(sum_ab)
        mag = magnitude(sum_ab)
        if mag > max_mag:
            max_mag = mag
    return max_mag

def main():
    # Read input from standard input
    numbers = parse_input(lines)

    # Part 1: Add all numbers sequentially and calculate magnitude
    final_sum = add_all_snailfish_numbers(numbers.copy())
    final_magnitude = magnitude(final_sum)
    print(f"Part 1: Magnitude of the final sum is {final_magnitude}")

    # Part 2: Find the largest magnitude from adding any two distinct numbers
    largest_mag = find_largest_magnitude(numbers)
    print(f"Part 2: The largest magnitude of any sum of two distinct snailfish numbers is {largest_mag}")

main()
