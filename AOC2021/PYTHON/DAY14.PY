#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
lines = text.splitlines()
#=============================================================
# all below from ChatGPT o1-mini
#=============================================================
import sys
from collections import defaultdict
from typing import Dict, Tuple, List

def parse_input(lines: List[str]) -> Tuple[str, Dict[str, str]]:
    """
    Parses the input into the polymer template and pair insertion rules.
    """
    template = lines[0]
    rules = {}
    for line in lines[2:]:  # Skip the first line and the empty line
        pair, insertion = line.strip().split(" -> ")
        rules[pair] = insertion
    return template, rules

def initialize_pair_counts(template: str) -> Dict[str, int]:
    """
    Initializes the pair counts from the initial polymer template.
    """
    pair_counts = defaultdict(int)
    for i in range(len(template) - 1):
        pair = template[i:i+2]
        pair_counts[pair] += 1
    return pair_counts

def count_elements(template: str) -> Dict[str, int]:
    """
    Counts the occurrences of each element in the initial polymer template.
    """
    element_counts = defaultdict(int)
    for element in template:
        element_counts[element] += 1
    return element_counts

def apply_insertions(pair_counts: Dict[str, int], rules: Dict[str, str], element_counts: Dict[str, int]) -> Dict[str, int]:
    """
    Applies one step of pair insertion and updates the pair and element counts.
    """
    new_pair_counts = defaultdict(int)
    for pair, count in pair_counts.items():
        if pair in rules:
            insertion = rules[pair]
            # Update element counts for the inserted element
            element_counts[insertion] += count
            # Create new pairs after insertion
            new_pair1 = pair[0] + insertion
            new_pair2 = insertion + pair[1]
            new_pair_counts[new_pair1] += count
            new_pair_counts[new_pair2] += count
        else:
            # If no rule applies, carry over the pair as is
            new_pair_counts[pair] += count
    return new_pair_counts

def simulate_steps(template: str, rules: Dict[str, str], steps: int) -> int:
    """
    Simulates the polymerization process for a given number of steps and
    returns the difference between the most and least common elements.
    """
    pair_counts = initialize_pair_counts(template)
    element_counts = count_elements(template)

    for step in range(1, steps + 1):
        pair_counts = apply_insertions(pair_counts, rules, element_counts)
        # Debug: Uncomment the following lines to see intermediate results
        # print(f"After step {step}:")
        # print(f"Pair counts: {dict(pair_counts)}")
        # print(f"Element counts: {dict(element_counts)}\n")

    # Calculate the difference between most and least common elements
    quantities = element_counts.values()
    return max(quantities) - min(quantities)

def main():
    # Read input from standard input
    template, rules = parse_input(lines)

    # Part A: 10 steps
    part_a_result = simulate_steps(template, rules, 10)
    print(f"Part A: Quantity difference after 10 steps is {part_a_result}")

    # Part B: 40 steps
    part_b_result = simulate_steps(template, rules, 40)
    print(f"Part B: Quantity difference after 40 steps is {part_b_result}")

main()
