import re
import copy

class Group:
    def __init__(self, units, hit_points, weaknesses, immunities, attack_damage, attack_type, initiative, group_id, army):
        self.units = units
        self.hit_points = hit_points
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.group_id = group_id
        self.army = army
        self.unique_id = f"{army}_{group_id}"  # Unique identifier

    def effective_power(self):
        return self.units * self.attack_damage

    def damage_to(self, other):
        if self.attack_type in other.immunities:
            return 0
        elif self.attack_type in other.weaknesses:
            return 2 * self.effective_power()
        else:
            return self.effective_power()

    def take_damage(self, damage):
        lost_units = damage // self.hit_points
        if lost_units > 0:
            self.units = max(0, self.units - lost_units)

    def __repr__(self):
        return f"{self.army} group {self.group_id} contains {self.units} units"

def parse_group(line, group_id, army, boost=0):
    """
    Parses a single line of group description and returns a Group object.
    If the group belongs to the Immune System, its attack_damage is boosted by the specified amount.
    """
    # Adjusted regex to make attributes optional
    pattern = r"(\d+) units each with (\d+) hit points(?: \((.*?)\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)"
    match = re.match(pattern, line)
    if not match:
        print(f"Failed to parse line: {line}")
        return None
    units, hit_points, attributes, attack_damage, attack_type, initiative = match.groups()
    units, hit_points, attack_damage, initiative = map(int, [units, hit_points, attack_damage, initiative])
    
    # Apply boost if the group is part of the Immune System
    if army == "Immune System":
        attack_damage += boost

    weaknesses, immunities = set(), set()

    if attributes:
        for attr in attributes.split('; '):
            if attr.startswith('weak to '):
                weaknesses.update(map(str.strip, attr[len('weak to '):].split(',')))
            elif attr.startswith('immune to '):
                immunities.update(map(str.strip, attr[len('immune to '):].split(',')))

    return Group(units, hit_points, weaknesses, immunities, attack_damage, attack_type, initiative, group_id, army)

def target_selection(groups):
    print("\nTarget selection phase:")
    # Sort groups by effective power and initiative
    selection_order = sorted(groups, key=lambda x: (-x.effective_power(), -x.initiative))
    targets = {}
    chosen_targets = set()
    
    for group in selection_order:
        # Potential enemies are from the opposing army and not yet chosen
        enemies = [enemy for enemy in groups if enemy.army != group.army and enemy.unique_id not in chosen_targets and enemy.units > 0]
        # Sort enemies by damage potential, then by effective power and initiative
        enemies = sorted(enemies, key=lambda x: (-group.damage_to(x), -x.effective_power(), -x.initiative))
        
        if enemies and group.damage_to(enemies[0]) > 0:
            target = enemies[0]
            targets[group.unique_id] = target
            chosen_targets.add(target.unique_id)
            print(f"{group.army} group {group.group_id} would deal defending group {target.group_id} {group.damage_to(target)} damage")
        else:
            print(f"{group.army} group {group.group_id} does not select a target")

    return targets

def attack_phase(groups, targets):
    print("\nAttack phase:")
    # Sort groups by descending initiative
    attack_order = sorted(groups, key=lambda x: -x.initiative)

    for group in attack_order:
        if group.units <= 0:
            continue  # Dead groups cannot attack
        if group.unique_id not in targets:
            continue  # Did not select a target
        target = targets[group.unique_id]
        if target.units <= 0:
            continue  # Target already dead

        damage = group.damage_to(target)
        if damage <= 0:
            continue  # No damage dealt

        killed_units = damage // target.hit_points
        actual_kills = min(killed_units, target.units)
        if actual_kills > 0:
            print(f"{group.army} group {group.group_id} attacks defending group {target.group_id}, killing {actual_kills} units")
            target.take_damage(damage)
        else:
            print(f"{group.army} group {group.group_id} attacks defending group {target.group_id}, but kills no units")

def simulate_battle(immune_groups, infection_groups):
    """
    Simulates the battle between immune_groups and infection_groups.
    Returns the surviving groups for both armies.
    """
    round_number = 1
    while immune_groups and infection_groups:
        print(f"\n--- Round {round_number} ---")
        print("Immune System:")
        for group in immune_groups:
            print(f"Group {group.group_id} contains {group.units} units")
        print("Infection:")
        for group in infection_groups:
            print(f"Group {group.group_id} contains {group.units} units")

        # Combine all groups for target selection
        groups = immune_groups + infection_groups
        targets = target_selection(groups)
        
        # Capture the total units before the attack phase to detect stalemates
        initial_units = sum(g.units for g in groups)
        attack_phase(groups, targets)
        final_units = sum(g.units for g in groups)

        units_killed = initial_units - final_units
        if units_killed == 0:
            print("\nStalemate detected: No units were killed in this round.")
            break  # Prevent infinite loops

        # Remove dead groups
        immune_groups = [g for g in immune_groups if g.units > 0]
        infection_groups = [g for g in infection_groups if g.units > 0]
        round_number += 1

    return immune_groups, infection_groups

def smallest_boost(initial_immune_input, initial_infection_input):
    """
    Finds the smallest boost needed for the Immune System to win.
    Returns the number of units remaining in the Immune System after the battle.
    """
    boost_min = 0
    boost_max = 100000  # An upper bound for the boost; adjust as needed
    result = None

    while boost_min <= boost_max:
        mid_boost = (boost_min + boost_max) // 2
        print(f"\nTesting boost: {mid_boost}")
        
        # Deep copy the initial groups to avoid mutating the originals
        immune_groups = [copy.deepcopy(group) for group in initial_immune_input]
        infection_groups = [copy.deepcopy(group) for group in initial_infection_input]
        
        # Apply the boost to the Immune System groups
        for group in immune_groups:
            group.attack_damage += mid_boost

        # Simulate the battle
        surviving_immune, surviving_infection = simulate_battle(immune_groups, infection_groups)
        
        if surviving_infection:
            # Infection won or stalemate; need to increase the boost
            print(f"Boost {mid_boost} insufficient. Infection wins or stalemate.")
            boost_min = mid_boost + 1
        else:
            # Immune System won; record the result and try to find a smaller boost
            total_units = sum(g.units for g in surviving_immune)
            print(f"Boost {mid_boost} successful. Immune System wins with {total_units} units remaining.")
            result = (mid_boost, total_units)
            boost_max = mid_boost - 1

    if result:
        return result
    else:
        print("No boost found that allows the Immune System to win.")
        return None

def main():
    # Initial group inputs
    immune_input_data = [
        "17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2",
        "989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3"
    ]
    infection_input_data = [
        "801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1",
        "4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"
    ]

       # Immune System:
    immune_input_data = """
2743 units each with 4149 hit points with an attack that does 13 radiation damage at initiative 14
8829 units each with 7036 hit points with an attack that does 7 fire damage at initiative 15
1928 units each with 10700 hit points (weak to cold; immune to fire, radiation, slashing) with an attack that does 50 slashing damage at initiative 3
6051 units each with 11416 hit points with an attack that does 15 bludgeoning damage at initiative 20
895 units each with 10235 hit points (immune to slashing; weak to bludgeoning) with an attack that does 92 bludgeoning damage at initiative 10
333 units each with 1350 hit points with an attack that does 36 radiation damage at initiative 12
2138 units each with 8834 hit points (weak to bludgeoning) with an attack that does 35 cold damage at initiative 11
4325 units each with 1648 hit points (weak to cold, fire) with an attack that does 3 bludgeoning damage at initiative 8
37 units each with 4133 hit points (immune to radiation, slashing) with an attack that does 1055 radiation damage at initiative 1
106 units each with 3258 hit points (immune to slashing, radiation) with an attack that does 299 cold damage at initiative 13
""".strip().split("\n")
    
    # Infection:
    infection_input_data = """
262 units each with 8499 hit points (weak to cold) with an attack that does 45 cold damage at initiative 6
732 units each with 47014 hit points (weak to cold, bludgeoning) with an attack that does 127 bludgeoning damage at initiative 17
4765 units each with 64575 hit points with an attack that does 20 radiation damage at initiative 18
3621 units each with 19547 hit points (immune to radiation, cold) with an attack that does 9 cold damage at initiative 5
5913 units each with 42564 hit points (immune to radiation, bludgeoning, fire) with an attack that does 14 slashing damage at initiative 9
7301 units each with 51320 hit points (weak to radiation, fire; immune to bludgeoning) with an attack that does 11 fire damage at initiative 2
3094 units each with 23713 hit points (weak to slashing, fire) with an attack that does 14 radiation damage at initiative 19
412 units each with 36593 hit points (weak to radiation, bludgeoning) with an attack that does 177 slashing damage at initiative 16
477 units each with 35404 hit points with an attack that does 146 cold damage at initiative 7
332 units each with 11780 hit points (weak to fire) with an attack that does 70 slashing damage at initiative 4
""".strip().split("\n")

    # Parse the groups without any boost initially
    initial_immune_groups = []
    for i, line in enumerate(immune_input_data):
        group = parse_group(line, i + 1, "Immune System")
        if group:
            initial_immune_groups.append(group)

    initial_infection_groups = []
    for i, line in enumerate(infection_input_data):
        group = parse_group(line, i + 1, "Infection")
        if group:
            initial_infection_groups.append(group)

    # Simulate the battle with a boost of 1570
    print("\n=== Battle with Boost of 1570 ===")
    # Deep copy the initial groups to avoid mutating the originals
    boosted_immune_groups = [copy.deepcopy(group) for group in initial_immune_groups]
    boosted_infection_groups = [copy.deepcopy(group) for group in initial_infection_groups]
    
    # Apply a boost of 1570 to the Immune System groups
    boost_amount = 1570
    for group in boosted_immune_groups:
        group.attack_damage += boost_amount

    # Run the simulation
    surviving_immune, surviving_infection = simulate_battle(boosted_immune_groups, boosted_infection_groups)

    # Determine the outcome
    if surviving_immune and not surviving_infection:
        print("\nImmune System wins with a boost of 1570!")
        print(f"Units remaining: {sum(g.units for g in surviving_immune)}")
    elif surviving_infection and not surviving_immune:
        print("\nInfection wins even with a boost of 1570.")
        print(f"Units remaining: {sum(g.units for g in surviving_infection)}")
    else:
        print("\nNo groups remain or a stalemate was detected with a boost of 1570.")

    # Find the smallest boost where the Immune System wins
    # Uncomment the following lines to run the smallest_boost function
    print("\n=== Finding the Smallest Boost ===")
    boost_result = smallest_boost(initial_immune_groups, initial_infection_groups)
    if boost_result:
        boost_value, remaining_units = boost_result
        print(f"\nThe smallest boost needed is {boost_value} with {remaining_units} units remaining in the Immune System.")
    else:
        print("\nCould not determine a boost that allows the Immune System to win.")

if __name__ == "__main__":
    main()
