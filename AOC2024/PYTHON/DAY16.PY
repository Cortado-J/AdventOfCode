#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
import heapq

lines = text.split('\n')
grid = {}
start, end = None, None
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        pos = (x, y)
        grid[pos] = char
        if char == "S":
            start = pos
        elif char == "E":
            end = pos

# Directions: 0=North, 1=East, 2=South, 3=West
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # (dx, dy) for N,E,S,W
start_dir = 1  # Start facing East

dist = {}
for d in range(4):
    dist[(start[0], start[1], d)] = float('inf')
dist[(start[0], start[1], start_dir)] = 0

pq = []
heapq.heappush(pq, (0, start[0], start[1], start_dir))

min_cost = None
end_states = []  # Will hold all (x, y, d) states at the end tile that achieve minimal cost

while pq:
    cost, x, y, d = heapq.heappop(pq)
    if dist[(x, y, d)] < cost:
        continue

    # If we've already found a minimal cost path to end and this cost is greater, we can stop
    if min_cost is not None and cost > min_cost:
        break

    if (x, y) == end:
        # If we haven't found a min_cost yet, this is our minimal cost
        if min_cost is None:
            min_cost = cost
            end_states = [(x, y, d)]
        elif cost == min_cost:
            # Another end state with the same minimal cost
            end_states.append((x, y, d))
        # If cost > min_cost won't happen here due to the if-check above.
        # Do not break here; continue to find all same-cost end states.
        continue

    # Move forward
    nx = x + directions[d][0]
    ny = y + directions[d][1]
    if (nx, ny) in grid and grid[(nx, ny)] != '#':
        forward_cost = cost + 1
        if forward_cost < dist.get((nx, ny, d), float('inf')):
            dist[(nx, ny, d)] = forward_cost
            heapq.heappush(pq, (forward_cost, nx, ny, d))

    # Rotate left
    ld = (d - 1) % 4
    left_cost = cost + 1000
    if left_cost < dist.get((x, y, ld), float('inf')):
        dist[(x, y, ld)] = left_cost
        heapq.heappush(pq, (left_cost, x, y, ld))

    # Rotate right
    rd = (d + 1) % 4
    right_cost = cost + 1000
    if right_cost < dist.get((x, y, rd), float('inf')):
        dist[(x, y, rd)] = right_cost
        heapq.heappush(pq, (right_cost, x, y, rd))

# Print the minimal cost
print(f"Part A: {min_cost}")

# Now for Part B:
# Backtrack from end_states to find all states that lead to these minimal paths
on_best_path = set()  # store (x,y) positions on best paths
visited_states = set()
stack = end_states[:]

while stack:
    x, y, d = stack.pop()
    if (x, y, d) in visited_states:
        continue
    visited_states.add((x, y, d))
    on_best_path.add((x, y))

    current_cost = dist[(x, y, d)]

    # Check forward predecessor
    # If we came here by moving forward, we had:
    # predecessor: (px, py, d) with dist = current_cost - 1
    px = x - directions[d][0]
    py = y - directions[d][1]
    if (px, py, d) in dist and dist[(px, py, d)] == current_cost - 1:
        stack.append((px, py, d))

    # Check rotation predecessors:
    # Rotating left: came from direction (d+1) mod 4 with cost = current_cost - 1000
    ld = (d + 1) % 4
    if (x, y, ld) in dist and dist[(x, y, ld)] == current_cost - 1000:
        stack.append((x, y, ld))

    # Rotating right: came from direction (d-1) mod 4 with cost = current_cost - 1000
    rd = (d - 1) % 4
    if (x, y, rd) in dist and dist[(x, y, rd)] == current_cost - 1000:
        stack.append((x, y, rd))

# Count how many on_best_path tiles are not walls
count = 0
for (xx, yy) in on_best_path:
    if grid.get((xx, yy), '#') != '#':
        count += 1

# Print the count of tiles on at least one best path
print(f"Part B: {count}")
