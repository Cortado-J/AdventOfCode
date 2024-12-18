import collections
import heapq

# Function to find the shortest path that collects all keys
def shortest_path_to_collect_keys(vault):
    # Parsing the vault map to extract important information
    all_keys = 0
    start = None
    
    for y, row in enumerate(vault):
        for x, cell in enumerate(row):
            if cell == '@':
                start = (x, y)
            elif 'a' <= cell <= 'z':
                all_keys |= (1 << (ord(cell) - ord('a')))
    
    # Initialize BFS priority queue (for shortest path, use Dijkstra-like approach)
    pq = [(0, start[0], start[1], 0)] # (steps, x, y, keys_collected)
    visited = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while pq:
        steps, x, y, keys_collected = heapq.heappop(pq)

        # If we have collected all the keys, return the steps taken
        if keys_collected == all_keys:
            return steps

        # Avoid revisiting states that have already been processed
        if (x, y, keys_collected) in visited:
            continue
        visited.add((x, y, keys_collected))

        # Iterate through all possible moves
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(vault) and 0 <= nx < len(vault[0]):
                cell = vault[ny][nx]
                if cell == '#':
                    continue
                elif 'A' <= cell <= 'Z':  # Check if it's a door
                    # Check if we have the key to unlock this door
                    if not (keys_collected & (1 << (ord(cell.lower()) - ord('a')))):
                        continue
                elif 'a' <= cell <= 'z':  # If it's a key
                    # Add the key to the keys_collected
                    new_keys_collected = keys_collected | (1 << (ord(cell) - ord('a')))
                    heapq.heappush(pq, (steps + 1, nx, ny, new_keys_collected))
                    continue

                # Regular movement (open path)
                heapq.heappush(pq, (steps + 1, nx, ny, keys_collected))

    return -1

# Example usage
if __name__ == "__main__":
    vault_maps = [
        [
            "########################",
            "#f.D.E.e.C.b.A.@.a.B.c.#",
            "######################.#",
            "#d.....................#",
            "########################"
        ],
        [
            "########################",
            "#...............b.C.D.f#",
            "#.######################",
            "#.....@.a.B.c.d.A.e.F.g#",
            "########################"
        ],
        [
            "#################",
            "#i.G..c...e..H.p#",
            "########.########",
            "#j.A..b...f..D.o#",
            "########@########",
            "#k.E..a...g..B.n#",
            "########.########",
            "#l.F..d...h..C.m#",
            "#################"
        ],
        [
            "########################",
            "#@..............ac.GI.b#",
            "###d#e#f################",
            "###A#B#C################",
            "###g#h#i################",
            "########################"
        ]
    ]
    
    for i, vault_map in enumerate(vault_maps):
        result = shortest_path_to_collect_keys(vault_map)
        print(f"Example {i+1}: Shortest path to collect all keys: {result} steps")

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
"""
    vault_map = vault_map.strip().split("\n")
    result = shortest_path_to_collect_keys(vault_map)
    print(f"PART ONE: Shortest path to collect all keys: {result} steps")