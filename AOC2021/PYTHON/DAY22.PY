#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
# print(text)

lines = text.splitlines()
# on x=-20..26,y=-36..17,z=-47..7
# off x=-20..33,y=-21..23,z=-26..28

# all below form ChatGPT o1-mini

from dataclasses import dataclass
from typing import List, Tuple, Optional
import sys

@dataclass(frozen=True)
class Cuboid:
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int

    def intersect(self, other: 'Cuboid') -> Optional['Cuboid']:
        nx1 = max(self.x1, other.x1)
        nx2 = min(self.x2, other.x2)
        ny1 = max(self.y1, other.y1)
        ny2 = min(self.y2, other.y2)
        nz1 = max(self.z1, other.z1)
        nz2 = min(self.z2, other.z2)
        if nx1 <= nx2 and ny1 <= ny2 and nz1 <= nz2:
            return Cuboid(nx1, nx2, ny1, ny2, nz1, nz2)
        else:
            return None

    def volume(self) -> int:
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)

def parse_steps(lines: List[str]) -> List[Tuple[str, Cuboid]]:
    steps = []
    for line in lines:
        action, rest = line.strip().split(' ')
        coords = rest.split(',')
        x_range = coords[0][2:].split('..')
        y_range = coords[1][2:].split('..')
        z_range = coords[2][2:].split('..')
        cuboid = Cuboid(
            int(x_range[0]),
            int(x_range[1]),
            int(y_range[0]),
            int(y_range[1]),
            int(z_range[0]),
            int(z_range[1])
        )
        steps.append( (action, cuboid) )
    return steps

def part_a(steps: List[Tuple[str, Cuboid]]) -> int:
    on_cubes = set()
    initialization_region = Cuboid(-50, 50, -50, 50, -50, 50)
    for action, cuboid in steps:
        intersection = cuboid.intersect(initialization_region)
        if not intersection:
            continue
        # Iterate through all points in the intersection
        for x in range(intersection.x1, intersection.x2 + 1):
            for y in range(intersection.y1, intersection.y2 + 1):
                for z in range(intersection.z1, intersection.z2 + 1):
                    if action == 'on':
                        on_cubes.add( (x, y, z) )
                    else:
                        on_cubes.discard( (x, y, z) )
    return len(on_cubes)

def part_b(steps: List[Tuple[str, Cuboid]]) -> int:
    cuboids: List[Tuple[Cuboid, int]] = []  # List of (cuboid, sign)
    for action, current in steps:
        additions = []
        for existing, sign in cuboids:
            intersection = existing.intersect(current)
            if intersection:
                additions.append( (intersection, -sign) )
        if action == 'on':
            additions.append( (current, 1) )
        cuboids.extend(additions)
    total = 0
    for cuboid, sign in cuboids:
        total += cuboid.volume() * sign
    return total

# Read input from standard input
steps = parse_steps(lines)

# Part A
result_a = part_a(steps)
print(f"Part A: {result_a}")

# Part B
result_b = part_b(steps)
print(f"Part B: {result_b}")
