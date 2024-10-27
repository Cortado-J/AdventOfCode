from collections import deque
import re

def parse_input(input_text):
    valves = {}
    tunnels = {}
    for line in input_text.strip().splitlines():
        parts = re.findall(r'[A-Z]{2}|\d+', line)
        valve, flow_rate = parts[0], int(parts[1])
        valves[valve] = flow_rate
        tunnels[valve] = parts[2:]
    return valves, tunnels

def build_distance_map(valves, tunnels):
    # Use BFS to compute shortest distances between all pairs of valves with positive flow rates (and 'AA')
    valves_to_consider = [v for v in valves if valves[v] > 0 or v == 'AA']
    distances = {v: {} for v in valves_to_consider}

    for valve in valves_to_consider:
        visited = set()
        queue = deque([(valve, 0)])
        while queue:
            current, dist = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            if current in valves_to_consider:
                distances[valve][current] = dist
            for neighbor in tunnels[current]:
                queue.append((neighbor, dist + 1))
    return distances

def compute_pressure_per_subset(valves, distances, time_limit):
    flow_valves = [v for v in valves if valves[v] > 0]
    valve_indices = {v: i for i, v in enumerate(flow_valves)}
    memo = {}
    pressures_per_subset = {}

    def dfs(valve, time, opened_bitmask, total_pressure):
        key = (valve, opened_bitmask, time)
        if key in memo and memo[key] >= total_pressure:
            return
        memo[key] = total_pressure
        # Update the results dictionary
        pressures_per_subset[opened_bitmask] = max(pressures_per_subset.get(opened_bitmask, 0), total_pressure)

        for next_valve in flow_valves:
            bit = 1 << valve_indices[next_valve]
            if opened_bitmask & bit:
                continue
            travel_time = distances[valve].get(next_valve, float('inf'))
            time_needed = travel_time + 1  # move and open
            if time + time_needed > time_limit:
                continue
            remaining_time = time_limit - (time + time_needed)
            pressure = valves[next_valve] * remaining_time
            dfs(next_valve, time + time_needed, opened_bitmask | bit, total_pressure + pressure)

    dfs('AA', 0, 0, 0)
    return pressures_per_subset

def part1(valves, distances):
    time_limit = 30
    pressures_per_subset = compute_pressure_per_subset(valves, distances, time_limit)
    max_pressure = max(pressures_per_subset.values())
    return max_pressure

def part2(valves, distances):
    time_limit = 26
    pressures_per_subset = compute_pressure_per_subset(valves, distances, time_limit)
    max_pressure = 0
    subsets = list(pressures_per_subset.items())
    n = len(subsets)
    print(f"Total subsets: {n}")

    # Sort subsets by pressure descending for potential optimization
    subsets.sort(key=lambda x: x[1], reverse=True)

    max_pressure = 0

    for i in range(n):
        bitmask1, pressure1 = subsets[i]
        for j in range(i, n):
            bitmask2, pressure2 = subsets[j]
            if bitmask1 & bitmask2 == 0:
                total_pressure = pressure1 + pressure2
                if total_pressure > max_pressure:
                    max_pressure = total_pressure
                # Since subsets are sorted by pressure descending, we can break early
                # if pressure1 + pressure2 <= max_pressure
                # But we need to ensure we don't miss any better combinations
            # Optional optimization: break inner loop if pressure1 + pressure2 <= max_pressure
            # But due to the possibility of bitmask overlap, we can't rely solely on pressure values
    return max_pressure

if __name__ == "__main__":
    input_text = """Valve PL has flow rate=4; tunnels lead to valves LI, GD, LB, IA, LZ
Valve LB has flow rate=0; tunnels lead to valves PL, VR
Valve QS has flow rate=0; tunnels lead to valves MG, YL
Valve RM has flow rate=17; tunnels lead to valves OQ, UN
Valve QM has flow rate=0; tunnels lead to valves RD, RO
Valve LI has flow rate=0; tunnels lead to valves AF, PL
Valve VR has flow rate=0; tunnels lead to valves YL, LB
Valve SJ has flow rate=0; tunnels lead to valves RO, TU
Valve PZ has flow rate=14; tunnels lead to valves KU, HE
Valve OQ has flow rate=0; tunnels lead to valves RM, OC
Valve YT has flow rate=0; tunnels lead to valves PX, IO
Valve TU has flow rate=5; tunnels lead to valves WS, GZ, MG, SJ, GD
Valve PC has flow rate=7; tunnels lead to valves RY, WK, OG, PD
Valve HE has flow rate=0; tunnels lead to valves PZ, OG
Valve IO has flow rate=20; tunnels lead to valves YT, TX
Valve OC has flow rate=19; tunnels lead to valves OQ, PD
Valve AA has flow rate=0; tunnels lead to valves NY, IA, WK, FU, NU
Valve UN has flow rate=0; tunnels lead to valves JY, RM
Valve NY has flow rate=0; tunnels lead to valves AA, WA
Valve HU has flow rate=0; tunnels lead to valves WA, RC
Valve GD has flow rate=0; tunnels lead to valves PL, TU
Valve WK has flow rate=0; tunnels lead to valves PC, AA
Valve RY has flow rate=0; tunnels lead to valves PV, PC
Valve GX has flow rate=0; tunnels lead to valves QX, YL
Valve RC has flow rate=0; tunnels lead to valves HU, RL
Valve TX has flow rate=0; tunnels lead to valves IO, WA
Valve PV has flow rate=12; tunnel leads to valve RY
Valve PP has flow rate=25; tunnel leads to valve KU
Valve RL has flow rate=9; tunnel leads to valve RC
Valve OG has flow rate=0; tunnels lead to valves PC, HE
Valve PD has flow rate=0; tunnels lead to valves OC, PC
Valve RO has flow rate=8; tunnels lead to valves SJ, QX, MO, QM
Valve QX has flow rate=0; tunnels lead to valves GX, RO
Valve WA has flow rate=6; tunnels lead to valves TX, AF, RG, HU, NY
Valve PX has flow rate=0; tunnels lead to valves YT, OE
Valve GZ has flow rate=0; tunnels lead to valves TU, FU
Valve RG has flow rate=0; tunnels lead to valves OE, WA
Valve MG has flow rate=0; tunnels lead to valves QS, TU
Valve AF has flow rate=0; tunnels lead to valves WA, LI
Valve WS has flow rate=0; tunnels lead to valves ND, TU
Valve OE has flow rate=18; tunnels lead to valves RG, PX
Valve YL has flow rate=3; tunnels lead to valves VR, GX, QS, NU
Valve ND has flow rate=0; tunnels lead to valves JY, WS
Valve FU has flow rate=0; tunnels lead to valves GZ, AA
Valve NU has flow rate=0; tunnels lead to valves YL, AA
Valve JY has flow rate=11; tunnels lead to valves UN, RD, ND
Valve IA has flow rate=0; tunnels lead to valves AA, PL
Valve KU has flow rate=0; tunnels lead to valves PZ, PP
Valve RD has flow rate=0; tunnels lead to valves JY, QM
Valve MO has flow rate=0; tunnels lead to valves RO, LZ
Valve LZ has flow rate=0; tunnels lead to valves PL, MO"""

    valves, tunnels = parse_input(input_text)
    distances = build_distance_map(valves, tunnels)

    # Part 1
    result1 = part1(valves, distances)
    print(f"Part 1: {result1}")

    # Part 2
    result2 = part2(valves, distances)
    print(f"Part 2: {result2}")
