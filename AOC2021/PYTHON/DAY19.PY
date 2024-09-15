#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
lines = text.splitlines()
#=============================================================
# all below form ChatGPT o1-mini
import sys
import math
import itertools
from collections import defaultdict
from typing import List, Tuple, Set

def parse_input(lines: List[str]) -> List[List[Tuple[int, int, int]]]:
    """
    Parses the input into a list of scanners, each with a list of beacon coordinates.
    """
    scanners = []
    current_scanner = []
    for line in lines:
        if line.startswith('---'):
            if current_scanner:
                scanners.append(current_scanner)
                current_scanner = []
        elif line.strip() == '':
            continue
        else:
            coords = tuple(map(int, line.strip().split(',')))
            current_scanner.append(coords)
    if current_scanner:
        scanners.append(current_scanner)
    return scanners

def get_rotations():
    """
    Generates all 24 rotation functions for 3D space.
    Each rotation is represented as a function that takes (x, y, z) and returns rotated (x, y, z).
    """
    rotations = []
    # Define the basic rotations around the axes
    for rx in range(4):
        for ry in range(4):
            for rz in range(4):
                # Avoid duplicate rotations
                # Each rotation can be represented as a combination of axis rotations
                def rotate(point, rx=rx, ry=ry, rz=rz):
                    x, y, z = point
                    for _ in range(rx):
                        x, y, z = x, -z, y
                    for _ in range(ry):
                        x, y, z = -z, y, x
                    for _ in range(rz):
                        x, y, z = y, -x, z
                    return (x, y, z)
                rotated_point = rotate((1,2,3))
                if rotated_point not in [rot((1,2,3)) for rot in rotations]:
                    rotations.append(rotate)
                    if len(rotations) == 24:
                        return rotations
    return rotations

def rotate_beacons(beacons: List[Tuple[int, int, int]], rotation) -> List[Tuple[int, int, int]]:
    """
    Applies a rotation to a list of beacons.
    """
    return [rotation(beacon) for beacon in beacons]

def subtract(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Subtracts two 3D points.
    """
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def add(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Adds two 3D points.
    """
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def manhattan(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> int:
    """
    Computes the Manhattan distance between two 3D points.
    """
    return sum(abs(a[i] - b[i]) for i in range(3))

def align_scanners(scanners: List[List[Tuple[int, int, int]]]) -> Tuple[Set[Tuple[int, int, int]], List[Tuple[int, int, int]]]:
    """
    Aligns all scanners and returns the set of all unique beacons and the list of scanner positions.
    """
    rotations = get_rotations()
    aligned_scanners = {0}
    scanner_positions = {0: (0, 0, 0)}
    beacons = set(scanners[0])
    remaining_scanners = set(range(1, len(scanners)))

    while remaining_scanners:
        aligned = False
        for scanner in list(remaining_scanners):
            for rot in rotations:
                rotated = rotate_beacons(scanners[scanner], rot)
                # Count how many overlaps for each possible translation
                translation_counts = defaultdict(int)
                for beacon in rotated:
                    for existing in beacons:
                        translation = subtract(existing, beacon)
                        translation_counts[translation] += 1
                # Find the translation with the highest count
                translation, count = max(translation_counts.items(), key=lambda x: x[1])
                if count >= 12:
                    # Align this scanner
                    scanner_positions[scanner] = translation
                    # Add all beacons with the translation applied
                    for beacon in rotated:
                        absolute_beacon = add(beacon, translation)
                        beacons.add(absolute_beacon)
                    aligned_scanners.add(scanner)
                    remaining_scanners.remove(scanner)
                    aligned = True
                    print(f"Scanner {scanner} aligned at {translation} with {count} overlapping beacons.")
                    break
            if aligned:
                break
        if not aligned:
            print("No more scanners can be aligned. This should not happen if input is correct.")
            break
    return beacons, [scanner_positions[i] for i in range(len(scanners))]

def main():
    # Read input from standard input
    scanners = parse_input(lines)

    # Align all scanners
    beacons, scanner_positions = align_scanners(scanners)

    # Part 1: Number of unique beacons
    print(f"Part 1: Number of unique beacons is {len(beacons)}")

    # Part 2: Largest Manhattan distance between any two scanners
    max_distance = 0
    for a, b in itertools.combinations(scanner_positions, 2):
        distance = manhattan(a, b)
        if distance > max_distance:
            max_distance = distance
    print(f"Part 2: Largest Manhattan distance between any two scanners is {max_distance}")

main()

