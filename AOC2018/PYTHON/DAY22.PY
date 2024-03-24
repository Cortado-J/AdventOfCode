from heapq import heappush, heappop

# Constants for location types
ROCKY = 0
WET = 1
NARROW = 2

# Constants for tool types
TORCH = 0
GEAR = 1
NEITHER = 2

def erosion_level(x, y, depth, target, memo):
    if (x, y) in memo:
        return memo[(x, y)]

    if (x, y) == (0, 0) or (x, y) == target:
        geological_index = 0
    elif y == 0:
        geological_index = x * 16807
    elif x == 0:
        geological_index = y * 48271
    else:
        geological_index = erosion_level(x - 1, y, depth, target, memo) * erosion_level(x, y - 1, depth, target, memo)

    erosion = (geological_index + depth) % 20183
    memo[(x, y)] = erosion
    return erosion

def region_type(erosion_level):
    return erosion_level % 3

def calculate_risk_level(depth, target):
    memo = {}
    risk_level = 0

    for y in range(target[1] + 1):
        for x in range(target[0] + 1):
            erosion = erosion_level(x, y, depth, target, memo)
            risk_level += region_type(erosion)

    return risk_level


def dijkstra(depth, target):
    memo = {}
    queue = [(0, 0, 0, TORCH)]  # (total_time, x, y, tool) - starting with the torch
    visited = {} # { (x,y,tool) : time }
    min_time = float('inf')
    keeplenq = 1

    while queue:
        time, x, y, tool = heappop(queue)
        if (x > 10 * target[0]) or (y > 10 * target[1]):
            # Don't bother with routes that go a long way to the right or down
            continue

        if time >= min_time:
            continue

        if (x, y) == target and tool == TORCH:
            min_time = min(min_time, time)
            continue

        xyt = (x, y, tool)
        if xyt in visited:
            if time >= visited[xyt]:
                # We've found a slower route to the same point with the same tool so that's no good: 
                continue
        # So either xny has not been visited OR it has bee visited but took longer to get there before
        visited[xyt] = time
        
        current_type = region_type(erosion_level(x, y, depth, target, memo))

        # Move to adjacent positions
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0:
                continue

            new_type = region_type(erosion_level(nx, ny, depth, target, memo))

            if (new_type == ROCKY and tool != NEITHER) or (new_type == WET and tool != TORCH) or (new_type == NARROW and tool != GEAR):
                heappush(queue, (time + 1, nx, ny, tool))

        # Change tools
        for new_tool in [TORCH, GEAR, NEITHER]:
            if new_tool != tool and ((current_type == ROCKY and new_tool != NEITHER) or (current_type == WET and new_tool != TORCH) or (current_type == NARROW and new_tool != GEAR)):
                heappush(queue, (time + 7, x, y, new_tool))

    return min_time

# Puzzle input
depth = 11820
target = (7, 782)

# Test input
# depth = 510
# target = (10, 10)

risk_level = calculate_risk_level(depth, target)
print(f"PART A: The total risk level is: {risk_level}")

min_time = dijkstra(depth, target)
print(f"PART B: The fewest number of minutes to reach the target is: {min_time}")