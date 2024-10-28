import re

def parse_blueprints(input_text):
    blueprints = []
    lines = input_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue  # Skip empty lines or comments
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

def solve(blueprints, max_time):
    geode_counts = []
    for blueprint in blueprints[:3]:  # Only the first three blueprints
        max_geodes = max_geodes_for_blueprint(blueprint, max_time)
        geode_counts.append(max_geodes)
        print(f"Blueprint {blueprint['id']} can open {max_geodes} geodes")
    total_product = 1
    for geodes in geode_counts:
        total_product *= geodes
    print(f"Total product of geodes: {total_product}")
    return total_product

def max_geodes_for_blueprint(blueprint, max_time):
    costs = blueprint['costs']
    max_geodes = 0
    memo = {}

    def dfs(time, ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geodes_opened):
        nonlocal max_geodes
        # Base case
        if time == max_time:
            if geodes_opened > max_geodes:
                max_geodes = geodes_opened
            return

        # Upper bound pruning
        remaining_time = max_time - time
        # Potential geodes if we build a geode robot every remaining minute
        potential_geodes = geodes_opened + geode_robots * remaining_time + (remaining_time * (remaining_time - 1)) // 2
        if potential_geodes <= max_geodes:
            return

        # State key for memoization
        state_key = (time, ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian)
        if state_key in memo and memo[state_key] >= geodes_opened:
            return
        memo[state_key] = geodes_opened

        # Possible actions
        actions = []

        # Prioritize building geode robots
        if ore >= costs['geode_robot']['ore'] and obsidian >= costs['geode_robot']['obsidian']:
            actions.append('geode_robot')
        else:
            # If we can't build a geode robot, consider other robots
            if ore >= costs['obsidian_robot']['ore'] and clay >= costs['obsidian_robot']['clay']:
                actions.append('obsidian_robot')
            if ore >= costs['clay_robot']['ore']:
                actions.append('clay_robot')
            if ore >= costs['ore_robot']['ore']:
                actions.append('ore_robot')
            # Always consider waiting
            actions.append('wait')

        for action in actions:
            # Initialize new resource counts and robot counts
            new_ore = ore
            new_clay = clay
            new_obsidian = obsidian
            new_geodes_opened = geodes_opened

            # Spend resources to build the robot
            if action == 'geode_robot':
                new_ore -= costs['geode_robot']['ore']
                new_obsidian -= costs['geode_robot']['obsidian']
            elif action == 'obsidian_robot':
                new_ore -= costs['obsidian_robot']['ore']
                new_clay -= costs['obsidian_robot']['clay']
            elif action == 'clay_robot':
                new_ore -= costs['clay_robot']['ore']
            elif action == 'ore_robot':
                new_ore -= costs['ore_robot']['ore']

            # Check for negative resources
            if new_ore < 0 or new_clay < 0 or new_obsidian < 0:
                continue  # Invalid action

            # Collect resources from existing robots
            new_ore += ore_robots
            new_clay += clay_robots
            new_obsidian += obsidian_robots

            # Geode robots crack geodes
            new_geodes_opened += geode_robots

            # Update robot counts after resource collection
            if action == 'geode_robot':
                geode_robots_new = geode_robots + 1
                dfs(time + 1, ore_robots, clay_robots, obsidian_robots, geode_robots_new, new_ore, new_clay, new_obsidian, new_geodes_opened)
            elif action == 'obsidian_robot':
                obsidian_robots_new = obsidian_robots + 1
                dfs(time + 1, ore_robots, clay_robots, obsidian_robots_new, geode_robots, new_ore, new_clay, new_obsidian, new_geodes_opened)
            elif action == 'clay_robot':
                clay_robots_new = clay_robots + 1
                dfs(time + 1, ore_robots, clay_robots_new, obsidian_robots, geode_robots, new_ore, new_clay, new_obsidian, new_geodes_opened)
            elif action == 'ore_robot':
                ore_robots_new = ore_robots + 1
                dfs(time + 1, ore_robots_new, clay_robots, obsidian_robots, geode_robots, new_ore, new_clay, new_obsidian, new_geodes_opened)
            elif action == 'wait':
                dfs(time + 1, ore_robots, clay_robots, obsidian_robots, geode_robots, new_ore, new_clay, new_obsidian, new_geodes_opened)

    dfs(0, 1, 0, 0, 0, 0, 0, 0, 0)
    return max_geodes

# Example Input for Testing
input_text = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""
input_text = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 11 clay. Each geode robot costs 3 ore and 8 obsidian.
Blueprint 2: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 14 clay. Each geode robot costs 3 ore and 16 obsidian.
Blueprint 3: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 15 clay. Each geode robot costs 3 ore and 9 obsidian.
"""

# Parse the blueprints and solve
blueprints = parse_blueprints(input_text)
total_product = solve(blueprints, 32)
print(f"Final Answer (Product of Geodes): {total_product}")
