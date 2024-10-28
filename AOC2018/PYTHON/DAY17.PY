import re
from collections import deque
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

def read_input():
    """Reads input from a file and parses clay coordinates."""
    clay = set()
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')

    script_dir = os.path.dirname(os.path.abspath(__file__))
    daytext = os.path.basename(__file__)[3:5]  # Get the day number as two digits from the 3rd and 4th characters of the script filename
    file_path = os.path.join(script_dir, f"day{daytext}.txt")

    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r'([xy])=(\d+), ([xy])=(\d+)..(\d+)', line)
            if not m:
                continue
            a_axis, a_value, b_axis, b_start, b_end = m.groups()
            a_value = int(a_value)
            b_start = int(b_start)
            b_end = int(b_end)
            if a_axis == 'x':
                x_values = [a_value]
                y_values = range(b_start, b_end + 1)
            else:
                y_values = [a_value]
                x_values = range(b_start, b_end + 1)
            for x in x_values:
                for y in y_values:
                    clay.add((x, y))
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

    # Expand the x range by 1 to account for water spreading
    min_x -= 1
    max_x += 1
    print(f"Clay positions: {len(clay)}")
    print(f"min_x: {min_x}, max_x: {max_x}, min_y: {min_y}, max_y: {max_y}")
    return clay, min_x, max_x, min_y, max_y

def plot_grid(clay, flowing_water, settled_water, min_x, max_x, min_y, max_y):
    """
    Plots the final state of the grid using matplotlib.

    Parameters:
    - clay: Set of (x, y) tuples representing clay.
    - flowing_water: Set of (x, y) tuples representing flowing water.
    - settled_water: Set of (x, y) tuples representing settled water.
    - min_x, max_x, min_y, max_y: Boundaries of the grid.
    """
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    grid_array = np.full((height, width), '.', dtype=str)  # Initialize with sand (.)

    # Populate clay
    for (x, y) in clay:
        grid_array[y - min_y, x - min_x] = '#'

    # Populate flowing water
    for (x, y) in flowing_water:
        if min_y <= y <= max_y:
            grid_array[y - min_y, x - min_x] = '|'

    # Populate settled water
    for (x, y) in settled_water:
        if min_y <= y <= max_y:
            grid_array[y - min_y, x - min_x] = '~'

    # Set the water source
    source_x = 500 - min_x
    source_y = 0 - min_y
    if min_y <= 0 <= max_y:
        grid_array[source_y, source_x] = '+'

    # Define a color map
    cmap = plt.cm.colors.ListedColormap(['white', 'black', 'blue', 'cyan', 'red'])
    norm = plt.cm.colors.BoundaryNorm([0, 1, 2, 3, 4, 5], cmap.N)

    # Convert grid symbols to numerical values for coloring
    symbol_to_num = {'.': 0, '#': 1, '+': 2, '|': 3, '~': 4}
    numeric_grid = np.vectorize(symbol_to_num.get)(grid_array)

    plt.figure(figsize=(12, 8))
    plt.imshow(numeric_grid, cmap=cmap, norm=norm, origin='upper', aspect='auto')
    plt.title("Final Reservoir State")
    plt.axis('off')  # Remove axis ticks
    plt.show()

def flow_water(clay, min_x, max_x, min_y, max_y):
    """Simulates the water flow and returns sets of flowing and settled water."""
    flowing_water = set()
    settled_water = set()
    queue = deque([(500, min_y - 1)])  # Start just above the minimum y
    queued_positions = set(queue)  # To prevent adding duplicates

    current_max_y = min_y - 1  # Initialize with one above the minimum y

    step_counter = 0
    max_steps = 1000000  # Safety limit to prevent infinite loops

    while queue and step_counter < max_steps:
        x, y = queue.popleft()
        queued_positions.discard((x, y))
        step_counter += 1

        # Debug: print progress every 10000 steps
        if step_counter % 10000 == 0:
            print(f"Processed {step_counter} steps. Queue size: {len(queue)}. Current max y: {current_max_y}")

        # Move down until we hit clay or settled water
        while True:
            if y > max_y:
                break
            if (x, y) in clay or (x, y) in settled_water:
                y -= 1
                break
            flowing_water.add((x, y))
            y += 1

            # Debugging: Update and print maximum y if it increases
            if y > current_max_y:
                current_max_y = y
                print(f"New maximum y reached by water: {current_max_y}")

        # Now y is the last valid position before hitting clay or settled water
        if y < min_y:
            continue

        # Attempt to spread left and right
        bounded = True
        left_x = x
        while True:
            left_x -= 1
            if (left_x, y) in clay:
                break
            below = (left_x, y + 1)
            if below not in clay and below not in settled_water:
                bounded = False
                if (left_x, y) not in queued_positions:
                    queue.append((left_x, y))
                    queued_positions.add((left_x, y))
                break
            flowing_water.add((left_x, y))

        right_x = x
        while True:
            right_x += 1
            if (right_x, y) in clay:
                break
            below = (right_x, y + 1)
            if below not in clay and below not in settled_water:
                bounded = False
                if (right_x, y) not in queued_positions:
                    queue.append((right_x, y))
                    queued_positions.add((right_x, y))
                break
            flowing_water.add((right_x, y))

        # If the region is bounded, convert flowing water to settled water
        if bounded:
            for fill_x in range(left_x + 1, right_x):
                settled_water.add((fill_x, y))
                flowing_water.discard((fill_x, y))
            # Add the position above to the queue for potential settling
            if (x, y - 1) not in queued_positions:
                queue.append((x, y - 1))
                queued_positions.add((x, y -1))

    if step_counter >= max_steps:
        print("Reached maximum step limit. The simulation may be stuck in an infinite loop.")

    return flowing_water, settled_water

def count_water(flowing_water, settled_water, min_y, max_y):
    """Counts the number of tiles reached by water."""
    total_flowing = sum(min_y <= y <= max_y for (x, y) in flowing_water)
    total_settled = sum(min_y <= y <= max_y for (x, y) in settled_water)
    total = total_flowing + total_settled
    return total, total_settled

def main():
    clay, min_x, max_x, min_y, max_y = read_input()
    flowing_water, settled_water = flow_water(clay, min_x, max_x, min_y, max_y)
    total, settled = count_water(flowing_water, settled_water, min_y, max_y)
    print("Total water tiles (flowing + settled):", total)
    print("Settled water tiles:", settled)
    plot_grid(clay, flowing_water, settled_water, min_x, max_x, min_y, max_y)

if __name__ == '__main__':
    main()
