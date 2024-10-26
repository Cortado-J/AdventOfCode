from heapq import heappop, heappush
from collections import defaultdict, deque
import itertools

def shortest_path_all_keys_with_robots(grid):
    def neighbors(x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            yield x + dx, y + dy

    def replace_center_with_robots(grid):
        grid = [list(row) for row in grid]
        mid_x, mid_y = None, None

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == '@':
                    mid_x, mid_y = i, j
                    break
            if mid_x is not None:
                break

        assert mid_x is not None and mid_y is not None, "Central '@' not found."

        grid[mid_x - 1][mid_y - 1] = '@'
        grid[mid_x - 1][mid_y + 1] = '@'
        grid[mid_x + 1][mid_y - 1] = '@'
        grid[mid_x + 1][mid_y + 1] = '@'

        grid[mid_x][mid_y] = '#'
        grid[mid_x - 1][mid_y] = '#'
        grid[mid_x + 1][mid_y] = '#'
        grid[mid_x][mid_y - 1] = '#'
        grid[mid_x][mid_y + 1] = '#'

        new_starts = [(mid_x - 1, mid_y - 1), (mid_x - 1, mid_y + 1), (mid_x + 1, mid_y - 1), (mid_x + 1, mid_y + 1)]
        return grid, new_starts

    def bfs_distances_from(start, grid, keys_bitmask):
        distances = {}
        queue = deque([(start, 0)])
        visited = set([start])
        while queue:
            (x, y), d = queue.popleft()
            if grid[x][y].islower() and (x, y) != start:
                distances[grid[x][y]] = d
            elif (x, y) in key_positions.values():
                key = [k for k, v in key_positions.items() if v == (x, y)][0]
                distances[key] = d
            for nx, ny in neighbors(x, y):
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and (nx, ny) not in visited and grid[nx][ny] != '#':
                    if grid[nx][ny].isupper() and not (keys_bitmask & (1 << (ord(grid[nx][ny].lower()) - ord('a')))):
                        continue  # Skip the door if the corresponding key is not collected
                    visited.add((nx, ny))
                    queue.append(((nx, ny), d + 1))
        return distances

    def mst_heuristic(remaining_keys, distances):
        if not remaining_keys:
            return 0
        edges = [(distances[a][b], a, b) for a, b in itertools.combinations(remaining_keys, 2) if b in distances[a]]
        edges.sort()
        parent = {k: k for k in remaining_keys}

        def find(k):
            if parent[k] != k:
                parent[k] = find(parent[k])
            return parent[k]

        mst_cost = 0
        for cost, a, b in edges:
            root_a, root_b = find(a), find(b)
            if root_a != root_b:
                parent[root_a] = root_b
                mst_cost += cost
        return mst_cost

    grid, start_positions = replace_center_with_robots(grid)
    key_positions = {}
    door_positions = {}
    all_keys_bitmask = 0

    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char.islower():
                key_positions[char] = (i, j)
                all_keys_bitmask |= (1 << (ord(char) - ord('a')))
            elif char.isupper():
                door_positions[char] = (i, j)

    start_identifiers = [f'@{i}' for i in range(4)]
    all_positions = {**key_positions, **{start_identifiers[i]: pos for i, pos in enumerate(start_positions)}}

    distances = defaultdict(dict)
    for key, pos in all_positions.items():
        bfs_result = bfs_distances_from(pos, grid, 0)  # Initial keys_bitmask is 0
        for target, dist in bfs_result.items():
            distances[key][target] = dist
            distances[target][key] = dist  # Ensure bi-directional distances

    initial_state = (0, *start_positions[0], *start_positions[1], *start_positions[2], *start_positions[3], 0)

    queue = [(mst_heuristic(list(key_positions.keys()), distances), 0, initial_state)]
    visited = set()
    distances_to_state = defaultdict(lambda: float('inf'))
    distances_to_state[initial_state] = 0

    while queue:
        _, steps, state = heappop(queue)
        robot_positions = state[1:9]
        keys_bitmask = state[9]

        if keys_bitmask == all_keys_bitmask:
            return steps

        for i in range(4):
            robot_x, robot_y = robot_positions[2 * i], robot_positions[2 * i + 1]
            for nx, ny in neighbors(robot_x, robot_y):
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                    char = grid[nx][ny]
                    if char == '#':
                        continue

                    new_keys_bitmask = keys_bitmask
                    if char.islower():
                        new_keys_bitmask |= (1 << (ord(char) - ord('a')))
                    elif char.isupper() and not (keys_bitmask & (1 << (ord(char) - ord('A')))):
                        continue

                    new_robot_positions = list(robot_positions)
                    new_robot_positions[2 * i], new_robot_positions[2 * i + 1] = nx, ny

                    new_state = (steps + 1, *new_robot_positions, new_keys_bitmask)

                    if distances_to_state[new_state] > steps + 1:
                        distances_to_state[new_state] = steps + 1
                        remaining_keys = [k for k in key_positions if not (new_keys_bitmask & (1 << (ord(k) - ord('a'))))]
                        heappush(queue, (steps + 1 + mst_heuristic(remaining_keys, distances), steps + 1, new_state))

    return -1  # In case no solution is found

# Test grids
test_grids = [
    [
        "#######",
        "#a.#Cd#",
        "##...##",
        "##.@.##",
        "##...##",
        "#cB#Ab#",
        "#######"
    ],
    [
        "#############",
        "#DcBa.#.GhKl#",
        "#.###...#I###",
        "#e#d#.@.#j#k#",
        "###C#...###J#",
        "#fEbA.#.FgHi#",
        "#############"
    ],
    [
        "#############",
        "#g#f.D#..h#l#",
        "#F###e#E###.#",
        "#dCba...BcIJ#",
        "#####.@.#####",
        "#nK.L...G...#",
        "#M###N#H###.#",
        "#o#m..#i#jk.#",
        "#############"
    ]
]

for i, grid in enumerate(test_grids):
    print(f"Test grid {i + 1}:")
    print(f"  Result: {shortest_path_all_keys_with_robots(grid)}")
