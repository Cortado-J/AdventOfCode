import re
from functools import lru_cache

def parse_blueprints(input_text):
    blueprints = []
    lines = input_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        # Extract the blueprint ID
        blueprint_id = int(re.search(r'Blueprint (\d+):', line).group(1))
        # Extract the costs using regular expressions
        ore_robot_cost = int(re.search(r'Each ore robot costs (\d+) ore', line).group(1))
        clay_robot_cost = int(re.search(r'Each clay robot costs (\d+) ore', line).group(1))
        obsidian_robot_costs = re.search(r'Each obsidian robot costs (\d+) ore and (\d+) clay', line)
        obsidian_robot_ore_cost = int(obsidian_robot_costs.group(1))
        obsidian_robot_clay_cost = int(obsidian_robot_costs.group(2))
        geode_robot_costs = re.search(r'Each geode robot costs (\d+) ore and (\d+) obsidian', line)
        geode_robot_ore_cost = int(geode_robot_costs.group(1))
        geode_robot_obsidian_cost = int(geode_robot_costs.group(2))

        costs = {
            'ore_robot': {'ore': ore_robot_cost},
            'clay_robot': {'ore': clay_robot_cost},
            'obsidian_robot': {'ore': obsidian_robot_ore_cost, 'clay': obsidian_robot_clay_cost},
            'geode_robot': {'ore': geode_robot_ore_cost, 'obsidian': geode_robot_obsidian_cost},
        }

        blueprints.append({'id': blueprint_id, 'costs': costs})
    return blueprints

def solve(blueprints):
    total_quality = 0
    for blueprint in blueprints:
        max_geodes = max_geodes_for_blueprint(blueprint)
        quality = blueprint['id'] * max_geodes
        total_quality += quality
        print(f"Blueprint {blueprint['id']} can open {max_geodes} geodes; quality level {quality}")
    return total_quality

def max_geodes_for_blueprint(blueprint):
    max_time = 24
    costs = blueprint['costs']

    # Precompute maximum robots needed for each resource
    max_ore_needed = max(cost.get('ore', 0) for cost in costs.values())
    max_clay_needed = costs['obsidian_robot'].get('clay', 0)
    max_obsidian_needed = costs['geode_robot'].get('obsidian', 0)

    @lru_cache(maxsize=None)
    def dfs(time, ore_robots, clay_robots, obsidian_robots, geode_robots,
            ore, clay, obsidian):
        if time == max_time:
            return 0  # No more time left

        max_geodes = 0
        remaining_time = max_time - time

        # Upper bound pruning
        max_possible_geodes = geode_robots * remaining_time + (remaining_time * (remaining_time - 1)) // 2
        if max_possible_geodes <= 0:
            return 0

        # Decide which robots to build
        build_options = []

        # Option to build geode robot
        if ore >= costs['geode_robot'].get('ore', 0) and obsidian >= costs['geode_robot'].get('obsidian', 0):
            build_options.append('geode_robot')
        else:
            # Option to build obsidian robot
            if obsidian_robots < max_obsidian_needed and ore >= costs['obsidian_robot'].get('ore', 0) and clay >= costs['obsidian_robot'].get('clay', 0):
                build_options.append('obsidian_robot')
            # Option to build clay robot
            if clay_robots < max_clay_needed and ore >= costs['clay_robot'].get('ore', 0):
                build_options.append('clay_robot')
            # Option to build ore robot
            if ore_robots < max_ore_needed and ore >= costs['ore_robot'].get('ore', 0):
                build_options.append('ore_robot')
            # Option to build nothing
            build_options.append(None)

        max_result = 0
        for build in build_options:
            # Copy resources and robot counts
            new_ore = ore
            new_clay = clay
            new_obsidian = obsidian
            new_ore_robots = ore_robots
            new_clay_robots = clay_robots
            new_obsidian_robots = obsidian_robots
            new_geode_robots = geode_robots

            # Spend resources to build the robot
            if build == 'geode_robot':
                new_ore -= costs['geode_robot']['ore']
                new_obsidian -= costs['geode_robot']['obsidian']
            elif build == 'obsidian_robot':
                new_ore -= costs['obsidian_robot']['ore']
                new_clay -= costs['obsidian_robot']['clay']
            elif build == 'clay_robot':
                new_ore -= costs['clay_robot']['ore']
            elif build == 'ore_robot':
                new_ore -= costs['ore_robot']['ore']

            # Collect resources
            new_ore += ore_robots
            new_clay += clay_robots
            new_obsidian += obsidian_robots
            geodes_opened = geode_robots  # Geodes opened this minute

            # Add the new robot after resources are collected
            if build == 'geode_robot':
                new_geode_robots += 1
            elif build == 'obsidian_robot':
                new_obsidian_robots += 1
            elif build == 'clay_robot':
                new_clay_robots += 1
            elif build == 'ore_robot':
                new_ore_robots += 1

            # Prune states with negative resources
            if new_ore < 0 or new_clay < 0 or new_obsidian < 0:
                continue

            # Recurse to next minute
            result = geodes_opened + dfs(time + 1, new_ore_robots, new_clay_robots, new_obsidian_robots, new_geode_robots,
                                         new_ore, new_clay, new_obsidian)
            if result > max_result:
                max_result = result

            # If we built a geode robot, prioritize this path
            if build == 'geode_robot':
                break

        return max_result

    # Initial state: 1 ore robot, 0 other robots, 0 resources
    return dfs(0, 1, 0, 0, 0, 0, 0, 0)

# Input with each blueprint on a single line
input_text = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 11 clay. Each geode robot costs 3 ore and 8 obsidian.
Blueprint 2: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 14 clay. Each geode robot costs 3 ore and 16 obsidian.
Blueprint 3: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 15 clay. Each geode robot costs 3 ore and 9 obsidian.
Blueprint 4: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 15 clay. Each geode robot costs 2 ore and 8 obsidian.
Blueprint 5: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 8 clay. Each geode robot costs 2 ore and 18 obsidian.
Blueprint 6: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 7 clay. Each geode robot costs 4 ore and 20 obsidian.
Blueprint 7: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 6 clay. Each geode robot costs 2 ore and 20 obsidian.
Blueprint 8: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 10 clay. Each geode robot costs 4 ore and 10 obsidian.
Blueprint 9: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 15 clay. Each geode robot costs 4 ore and 16 obsidian.
Blueprint 10: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 4 ore and 19 clay. Each geode robot costs 4 ore and 12 obsidian.
Blueprint 11: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 19 clay. Each geode robot costs 3 ore and 17 obsidian.
Blueprint 12: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 19 clay. Each geode robot costs 2 ore and 12 obsidian.
Blueprint 13: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 16 clay. Each geode robot costs 4 ore and 17 obsidian.
Blueprint 14: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 18 clay. Each geode robot costs 4 ore and 9 obsidian.
Blueprint 15: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 17 clay. Each geode robot costs 3 ore and 7 obsidian.
Blueprint 16: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 4 ore and 15 clay. Each geode robot costs 4 ore and 9 obsidian.
Blueprint 17: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 3 ore and 8 obsidian.
Blueprint 18: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 11 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 19: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 18 clay. Each geode robot costs 2 ore and 19 obsidian.
Blueprint 20: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 19 clay. Each geode robot costs 4 ore and 8 obsidian.
Blueprint 21: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 9 clay. Each geode robot costs 3 ore and 7 obsidian.
Blueprint 22: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 5 clay. Each geode robot costs 3 ore and 12 obsidian.
Blueprint 23: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 3 ore and 19 obsidian.
Blueprint 24: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 16 clay. Each geode robot costs 3 ore and 9 obsidian.
Blueprint 25: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 9 clay. Each geode robot costs 4 ore and 16 obsidian.
Blueprint 26: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 12 clay. Each geode robot costs 2 ore and 10 obsidian.
Blueprint 27: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 8 clay. Each geode robot costs 3 ore and 19 obsidian.
Blueprint 28: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 7 clay. Each geode robot costs 3 ore and 9 obsidian.
Blueprint 29: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 14 clay. Each geode robot costs 4 ore and 11 obsidian.
Blueprint 30: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 13 clay. Each geode robot costs 2 ore and 20 obsidian."""

# Parse the blueprints and solve
blueprints = parse_blueprints(input_text)
total_quality = solve(blueprints)
print(f"Total quality level: {total_quality}")
