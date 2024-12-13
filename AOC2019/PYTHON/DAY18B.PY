import heapq
from collections import deque

def modify_vault_for_part_two(vault):
    # Find the position of the original '@' symbol
    for y, row in enumerate(vault):
        for x, cell in enumerate(row):
            if cell == '@':
                start_x, start_y = x, y
                break

    # Replace the center 3x3 area with the new configuration
    vault[start_y - 1] = vault[start_y - 1][:start_x - 1] + '@#@' + vault[start_y - 1][start_x + 2:]
    vault[start_y]     = vault[start_y][:start_x - 1]     + '###' + vault[start_y][start_x + 2:]
    vault[start_y + 1] = vault[start_y + 1][:start_x - 1] + '@#@' + vault[start_y + 1][start_x + 2:]

def get_reachable_keys(vault, start_pos):
    """
    Performs BFS from the start_pos and returns a dictionary of reachable keys.
    Each entry in the dictionary is key: (distance, required_keys)
    """
    queue = deque()
    queue.append((start_pos[0], start_pos[1], 0, 0))  # x, y, distance, required_keys
    visited = set()
    reachable_keys = {}
    while queue:
        x, y, dist, req_keys = queue.popleft()
        cell = vault[y][x]
        new_req_keys = req_keys
        if 'A' <= cell <= 'Z':
            new_req_keys |= (1 << (ord(cell.lower()) - ord('a')))
        # Include required_keys in the visited state
        if (x, y, new_req_keys) in visited:
            continue
        visited.add((x, y, new_req_keys))
        if 'a' <= cell <= 'z' and (x, y) != start_pos:
            # Update reachable_keys if this is the shortest path to the key
            if cell not in reachable_keys or reachable_keys[cell][0] > dist:
                reachable_keys[cell] = (dist, new_req_keys)
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(vault) and 0 <= nx < len(vault[0]):
                next_cell = vault[ny][nx]
                if next_cell != '#':
                    queue.append((nx, ny, dist + 1, new_req_keys))
    return reachable_keys

def shortest_path_to_collect_keys_precomputed(vault):
    modify_vault_for_part_two(vault)
    # Find all starting positions (robots)
    start_positions = []
    all_keys_bitmask = 0
    for y, row in enumerate(vault):
        for x, cell in enumerate(row):
            if cell == '@':
                start_positions.append((x, y))
            elif 'a' <= cell <= 'z':
                all_keys_bitmask |= (1 << (ord(cell) - ord('a')))

    graph = {}
    positions_labels = []
    for idx, pos in enumerate(start_positions):
        label = '@' + str(idx)
        positions_labels.append(label)
        reachable = get_reachable_keys(vault, pos)
        graph[label] = reachable
    # Also get the reachable keys from each key
    for key, pos in [(vault[y][x], (x, y)) for y, row in enumerate(vault) for x, cell in enumerate(row) if 'a' <= cell <= 'z']:
        reachable = get_reachable_keys(vault, pos)
        graph[key] = reachable

    # Dijkstra's algorithm
    heap = []
    # State: (total_steps, positions of robots, keys_collected_bitmask)
    initial_positions = tuple(positions_labels)
    initial_state = (0, initial_positions, 0)
    heapq.heappush(heap, initial_state)
    visited = {}

    while heap:
        steps, positions, keys_collected = heapq.heappop(heap)

        if keys_collected == all_keys_bitmask:
            return steps

        # **Normalize robot positions in the state**
        state_positions = tuple(sorted(positions))
        state = (state_positions, keys_collected)

        # **Optimized visited dictionary check**
        if visited.get(state, float('inf')) <= steps:
            continue
        visited[state] = steps

        # For each robot, consider moving to reachable keys
        for robot_idx, robot_pos in enumerate(positions):
            current_label = robot_pos
            # Get reachable keys from current position
            for key, (dist, required_keys) in graph[current_label].items():
                key_bit = (1 << (ord(key) - ord('a')))
                if keys_collected & key_bit:
                    continue  # Already collected this key
                # **Correct required keys check**
                if (required_keys & keys_collected) != required_keys:
                    continue  # Missing some required keys
                # Move to this key
                new_positions = list(positions)
                new_positions[robot_idx] = key
                new_positions = tuple(new_positions)
                new_keys_collected = keys_collected | key_bit
                new_steps = steps + dist

                # Debugging output
                # print(f"Robot {robot_idx} moves to key '{key}' at distance {dist}, total steps now {new_steps}")

                # **Normalize positions for the new state**
                new_state_positions = tuple(sorted(new_positions))
                new_state = (new_state_positions, new_keys_collected)
                if visited.get(new_state, float('inf')) <= new_steps:
                    continue
                heapq.heappush(heap, (new_steps, new_positions, new_keys_collected))
    return -1

# Example usage
if __name__ == "__main__":
    # Convert the multiline string into a list of strings
    vault_map = """
#################################################################################
#.............#.#..g..........#t........#...#...................#.....#.....#...#
#W#########.#.#.#.#########.#.#.#####.###.#.#############.#####.###.#.#.#.#.###.#
#.#...#.....#...#.#...#...#.#.#.#...#...#.#.#....s..#..o#...#.#...#.#...#.#.#...#
#.###.#.#######.#.###.#.#.#.###.#.#.#.#.#.#.#.#####.#.#.#.#.#.###.###.###.#.#.###
#.....#.#.....#.#.#...#.#.#.....#.#.#.#.#.#...#...#.#.#.#.#.#...#...#...#.#.#...#
###.###.#.#.###.#.#.###.#.#######.#I###.#.#####.#.#.#.#.###.###.###.#.###.#.###.#
#.#.#...#.#.....#.#.#...#.....#...#.....#n..#...#.#...#...#.#...#.#.#.#...#...#.#
#.#.#.#####.#####.#.#.#####.###.###########.#.###########.#.#.#.#.#X###.#####.#.#
#.#.#x..Y.#.....#.#...#.....#...#.......#...#.#.............#.#...#.....#...#...#
#.#.#####.#######.#.###.#.###.###.#####.#.###.#.#############.###########.#.###.#
#...#...#.....#...#...#.#.#.E.#......j#.#.#...#.#.#.K.......#.#.....#.....#...#.#
#.###.#.#####.#.#######.###.#.#.#######.#.###.#.#.#.#######.#.#.#.#.#.###.#####.#
#.#...#.#.....#.#.....#.#...#.#.#.#.....#...#.....#.#b..#...#...#.#...#.#.#.....#
#.#.#.###.###.#.#.###.#.#.#####V#.#.#####.#.#######.#.#.#.###.###.#####.#Z#.#####
#.#.#.#...#.#.#...#...#.#.........#.....#.#...........#.#...#.#.#...#...#.#...#.#
#.#.###.###.#.#.#####.#.#########.#####.#.#################.#.#.###.###.#.###.#.#
#...#...#.....#.#...#.....#..q#.......#.#.......#...#.......#.#.#...#...#...#...#
#.###.###.#####.#.#.#######.#.#########.#########.#.#.#######.#.#.###.#####.###.#
#.#...#...#.....#.#.F.#.....#.........#.#.........#.#.#.........#...#.H...#...#.#
###.#######.#####.###.#.#############U#.#.###.#####.#.#########.###.#.###.#.###.#
#...#.....#.#...#...#.#.#...#.......#...#.#...#...#.#.....#...#...#.#...#...#...#
#.###.###.#.###.###.###.###.#.###.#.#####.#####.#.#.#####.#.#######.#########.###
#.....#...#.....#...#.....#...#...#.....#.....#.#.#.......#.#.......#.....#...#.#
#.#####.#######.#.###.###.#.###.#######.#.###.#.#.#######.#.#.###.###.###J#.###.#
#.....#.....#...#...#.#.#.#...#.....#...#...#...#.#.#.....#.#...#.#...#...#.#...#
#####.#####.#.#####.#.#.#.###.#####.#.###.#####.#.#.#.#####.#.#.#.#.###.#.#.###.#
#.....#...#.#.#.....#...#.#.#.#...#.#.#.#.#...#.#.#.....#...#.#.#.#..u#.#.#.....#
#.#######.#.#.#.#######.#.#.#.#.#.#.#.#.###.#.###.#######.###.#.###.###.#.#####.#
#.#.......#...#h#.......#.#...#.#.#.#.#c#...#...#...#.L.#...#.#...#.#...#.#.....#
#.###.#.#######.#.#######.#####.#.#.#.#.#.#####.###.#.#.###.#.###.#.#.#####.#####
#...#.#.....#...#...#...P.#.....#...#.#.#.#.........#.#.....#...#...#.....#.#...#
###.#####.#.#.#######.#####.#########.#.#.#.#########.#########.#########.#.#.#.#
#.#.....#.#.#.....#...#.....#.#.....#.#.#.#.#.....#...#...#...#.#..p..#.#.#...#.#
#.#####.#.#.#####.#.#####.###.#.#.###.#.#.###.###.#.###.###.#.#Q#.###.#.#.#####.#
#.......#.#.....#..z#.....#.#...#.....#.#...#...#.#.#...#...#.#...#.#.#.#..v..#.#
#.#######.#.###.#####.#.###.#.#########.###.###.#.#.#.#.#.###.#####.#.#.###.###.#
#.#.......#...#.#.....#.#.#...#...#...#.#...#...#.#.#.#.#.#.#.........#...#...#.#
#.###########.#.#######.#.#.###.#.#.#.#.#.###.###.#.#.#.#.#.#############.###.#.#
#.............#.........#.......#...#...........#...#.#....................f#...#
#######################################.@.#######################################
#.........#.....#.........#.....#.............#...............#.........#.......#
#.#####.###.###.#.#####.###.###.#.#.###.#.#.###.#########.###.#.#####.#.###.###.#
#.#.....#...#...#.....#...#.#.#...#...#.#.#.....#.......#.#...#.#.....#...#...#.#
###.#####.###.#.#####.###.#.#.#######.#.#.#######.###.###.###.#.#.#.#####.###.#.#
#...#.....#...#...#.#.#.#.#...#.....#.#.#.#...#...#.#...#...#.#.#.#.#...#.....#.#
#.###.#####.#####.#.#.#.#.###.#####.#.###.###.#.###.###.###.###.#.#.#.#.#.#######
#.#...#...#.....#.#.#.#.#...#.....#.#...#.#...#...#...#...#.....#.#.#.#.#.#.....#
#.#.###.#.#####.#.#.#.#.###.#####.#.###.#.#.#####.#.#.#.#.#######.###.#.###.###.#
#.#.#...#...#...#...#.#...#.....#.....#.#.#.........#.#.#.....#.#..d..#...#.#.#.#
#.#.#.#.###.#.#######.#.#.###.###.#####.#.#.#########.#.#####.#.#########.#.#A#.#
#...#.#.#.#.#...#.....#.#...#.#...#.....#.#.#...#.....#.#.#..m#.......#...#.#.#r#
#.#####.#.#.###.#.#######.#.#.#.###.###.#.###.#C#######.#.#.#########.#.###.#.#.#
#...#...#.#...#...#.......#.#...#l..#.#.#.....#.........#...#.........#.......#.#
###.#.###.###.#####.#####.#####.#.###.#.#################.###.###############.#.#
#.#.#.#.............#.....#...#.#...#...#.......#.........#...#.......#...#...#.#
#.#.#.###################.#.#.#####.#.###.#####.#.#########.###.#####.#.#.#####.#
#...#...#a..#...........#.#.#.......#...#.....#.#.....#.....#...#.......#.......#
#.#####.#.#.#.#########.#.#.#.###########.###.#.#####.###.#.#.###.#############.#
#...#...#.#.D.#...#...#.#.#.#.#.........#.#...#.#...#...#.#.#...#.....#.....#...#
###.#.#.#.###.#.#.#.#.#M###.###.#######.###.###.#.#.###.#.#####.###.###.###.#.###
#.....#.#.#...#.#...#.#...#.#...#.....#.#...#...#.#.......#..e#...#.#...#.#.#...#
#######.#.###.#.#########.#.#.###.###.#.#.#######.#########.#####.#.#.###.#.#####
#.....#.#...#.#.......#.....#.#...#...#.#.........#...#.....#...#.#.#.#...#.....#
#.###.#####.#########.#.#####.#####.#.#.#.#########.#.#.#####.#.#.###.#.#.#####.#
#.#.#.#...#.........#.#.#.....#.....#.#.#.#...#.....#.#i#.....#...#...#.#...#...#
#.#.#.#.#.###.#####.#.###.#####.#####.#.#.#.###.###.#.#.#.#########.#######.#.#.#
#.#.#...#.#...#.#...#.....#...#...#...#.#.#.#...#...#.#.#.............#.....#.#.#
#.#.#####.#.###.#.#########.###.#.#####.#.#.#.###.#####.#.###########.#.#####.###
#.#.....#.#.#.....#.......#.#...#...#...#.#.....#...#...#.#......w..#...#...#...#
#.#.#.###R#.#.#########.#.#.#.#####.#.###.#########.#.#####.#######.#####.#.###.#
#.#.#.......#.#.......#.#...#.#...#...#.#...........#...#...#.....#.......#...#.#
#.###########.#.#.###.#.#.###.#.#.#####.###.###########T#.#######.###########.#.#
#.#.....#.....#.#.#.#...#.#...#.#...#...#...#...........#.#.....#.........#.#...#
#.#.###.###.#####.#.#####.#.#####.#.#.#.#.###.###########.#.#.#.#.#####.#.#.#####
#.#.#.#...#...#...#.......#.....#.#...#.#.#.#.#...........#.#.#.#...#...#...#...#
#.#.#.###.###.#.#.#############.#####.#.#.#.#.###.###########.#.#####.#####.###.#
#.#.#...#.#.....#.#.S.........#.#...#.#y#..k#.G...#.........B.#.....#.....#...#.#
#.#.#.#.#.#########.#########.#.#.#.###.###.###########.###########.#####.###.#.#
#.....#.#...................#.O...#.....#...............#...........N.....#.....#
#################################################################################
""".strip().split("\n")

    result = shortest_path_to_collect_keys_precomputed(vault_map)
    print(f"PART TWO: Shortest path to collect all keys: {result} steps")
