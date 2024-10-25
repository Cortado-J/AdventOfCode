from collections import deque

def run_intcode_program(program, input_values, pc=0, relative_base=0):
    program = program[:] + [0] * 10000  # Extend memory
    outputs = []
    input_index = 0

    def get_value(mode, param):
        if mode == 0:
            return program[param] if param < len(program) else 0
        elif mode == 1:
            return param
        elif mode == 2:
            return program[relative_base + param] if (relative_base + param) < len(program) else 0
        else:
            raise ValueError(f"Unknown parameter mode: {mode}")

    def get_address(mode, param):
        if mode == 0:
            return param
        elif mode == 2:
            return relative_base + param
        else:
            raise ValueError(f"Invalid mode for writing: {mode}")

    while True:
        instruction = str(program[pc]).zfill(5)
        opcode = int(instruction[-2:])
        modes = list(map(int, instruction[:-2][::-1]))

        if opcode == 99:
            break

        elif opcode in (1, 2):
            param1 = get_value(modes[0], program[pc + 1])
            param2 = get_value(modes[1], program[pc + 2])
            dest = get_address(modes[2], program[pc + 3])
            if opcode == 1:
                program[dest] = param1 + param2
            elif opcode == 2:
                program[dest] = param1 * param2
            pc += 4

        elif opcode == 3:
            dest = get_address(modes[0], program[pc + 1])
            if input_index < len(input_values):
                program[dest] = input_values[input_index]
                input_index += 1
            else:
                return outputs, program, pc, relative_base  # Return state for further input if none is available
            pc += 2

        elif opcode == 4:
            param1 = get_value(modes[0], program[pc + 1])
            outputs.append(param1)
            pc += 2

        elif opcode in (5, 6):
            param1 = get_value(modes[0], program[pc + 1])
            param2 = get_value(modes[1], program[pc + 2])
            if (opcode == 5 and param1 != 0) or (opcode == 6 and param1 == 0):
                pc = param2
            else:
                pc += 3

        elif opcode in (7, 8):
            param1 = get_value(modes[0], program[pc + 1])
            param2 = get_value(modes[1], program[pc + 2])
            dest = get_address(modes[2], program[pc + 3])
            if (opcode == 7 and param1 < param2) or (opcode == 8 and param1 == param2):
                program[dest] = 1
            else:
                program[dest] = 0
            pc += 4

        elif opcode == 9:
            param1 = get_value(modes[0], program[pc + 1])
            relative_base += param1
            pc += 2

        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    return outputs, program, pc, relative_base

def explore_area(program):
    directions = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}
    queue = deque([((0, 0), program[:], 0, 0, 0)])  # position, program, pc, relative_base, distance
    visited = {(0, 0)}
    grid = {(0, 0): 1}
    oxygen_system_position = None

    while queue:
        (x, y), current_program, pc, relative_base, distance = queue.popleft()

        for direction, (dx, dy) in directions.items():
            new_pos = (x + dx, y + dy)

            if new_pos not in visited:
                output, next_program, next_pc, next_relative_base = run_intcode_program(current_program[:], [direction], pc, relative_base)
                if len(output) == 0:
                    continue
                status = output[0]
                grid[new_pos] = status
                visited.add(new_pos)

                if status != 0:  # Not a wall
                    if status == 2:  # Found the oxygen system
                        print(f"Oxygen system found at {new_pos} with distance {distance + 1}")
                        oxygen_system_position = new_pos
                    queue.append((new_pos, next_program, next_pc, next_relative_base, distance + 1))

    return grid, oxygen_system_position

def fill_with_oxygen(grid, oxygen_system_position):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    queue = deque([oxygen_system_position])
    visited = {oxygen_system_position}
    minutes = 0

    while queue:
        next_queue = deque()
        while queue:
            x, y = queue.popleft()
            for dx, dy in directions:
                neighbor = (x + dx, y + dy)
                if neighbor in grid and grid[neighbor] == 1 and neighbor not in visited:
                    visited.add(neighbor)
                    next_queue.append(neighbor)
        queue = next_queue
        if queue:
            minutes += 1

    return minutes

if __name__ == "__main__":
    program = [3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1001,1034,0,1039,1001,1036,0,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,102,1,1034,1039,1001,1036,0,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1106,0,124,1001,1034,-1,1039,1008,1036,0,1041,1001,1035,0,1040,101,0,1038,1043,101,0,1037,1042,1106,0,124,1001,1034,1,1039,1008,1036,0,1041,1002,1035,1,1040,102,1,1038,1043,1001,1037,0,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,37,1032,1006,1032,165,1008,1040,5,1032,1006,1032,165,1102,1,2,1044,1105,1,224,2,1041,1043,1032,1006,1032,179,1102,1,1,1044,1106,0,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,64,1044,1106,0,224,1101,0,0,1044,1105,1,224,1006,1044,247,1002,1039,1,1034,101,0,1040,1035,102,1,1041,1036,102,1,1043,1038,101,0,1042,1037,4,1044,1106,0,0,13,40,97,1,18,1,79,93,56,16,38,41,78,11,78,25,46,84,31,38,76,17,96,5,78,50,8,67,77,54,42,82,39,2,8,5,11,85,37,93,37,7,97,12,94,2,44,70,74,78,34,45,94,75,19,8,84,72,2,9,69,74,6,11,75,79,42,35,86,83,23,82,88,40,81,70,8,58,46,57,77,65,76,68,79,61,24,80,61,88,70,42,32,71,16,23,99,77,73,57,45,99,39,29,97,4,90,76,3,5,86,11,95,94,90,59,13,37,94,29,57,42,99,4,45,96,22,74,33,73,70,24,96,4,82,10,3,79,37,81,97,72,42,66,3,27,98,4,73,49,55,86,12,41,65,38,21,66,27,80,87,53,86,26,85,80,42,26,92,17,79,76,58,69,2,71,7,88,12,61,73,16,67,48,83,87,8,21,72,67,50,70,7,71,9,53,46,81,99,47,3,70,11,23,68,22,86,43,32,92,30,78,94,61,81,32,60,89,97,58,23,27,52,99,85,90,41,20,11,87,73,57,83,30,79,2,58,93,32,81,16,86,35,87,38,73,88,11,6,65,32,20,81,87,89,12,11,66,42,84,12,79,14,23,72,37,85,95,15,48,80,92,59,56,7,95,85,21,82,53,93,45,73,29,79,6,17,68,79,34,72,47,39,81,93,63,83,51,67,99,1,74,56,89,47,86,95,51,94,46,3,95,18,81,20,85,19,90,60,24,65,65,46,91,17,82,37,87,21,83,80,22,28,75,17,68,72,40,67,82,19,9,79,42,86,55,93,91,41,76,55,22,74,61,91,42,96,73,11,1,79,60,85,82,40,76,88,84,2,14,97,89,29,69,39,43,65,19,58,97,68,45,50,2,91,54,52,93,82,61,76,22,15,77,63,76,60,81,42,89,77,45,80,3,92,17,10,98,16,92,38,71,2,46,81,81,11,7,43,82,68,82,93,25,44,87,60,49,48,7,47,82,82,26,65,93,50,75,57,92,57,78,11,39,99,2,93,42,69,6,66,60,96,79,50,20,75,84,48,98,57,5,93,98,62,78,85,53,85,32,37,90,90,30,43,74,57,81,19,35,19,94,50,65,60,98,65,46,86,75,68,16,31,83,75,56,93,35,42,89,32,69,35,2,60,82,58,53,1,87,18,66,82,41,73,73,7,99,91,89,48,83,20,81,31,66,17,93,23,41,86,65,57,72,13,13,82,94,79,77,54,89,90,62,95,35,74,82,37,43,33,66,77,3,86,26,87,35,69,19,24,85,62,18,9,72,42,69,25,95,57,34,41,82,36,90,24,36,27,67,49,30,70,75,82,44,33,67,70,35,36,69,33,85,10,87,50,72,8,74,97,18,95,25,97,5,84,16,65,60,89,15,86,81,9,75,73,58,72,39,91,10,55,3,11,86,96,18,98,97,28,22,98,49,89,19,84,18,98,34,92,67,37,80,17,8,65,72,2,91,95,55,76,19,30,78,40,96,78,34,91,99,23,14,71,38,37,71,59,93,78,83,61,24,31,97,25,85,8,16,84,15,65,77,14,96,98,6,89,33,98,59,4,84,66,18,74,48,12,41,86,31,45,33,74,97,86,55,85,16,34,54,91,77,3,19,65,70,18,90,41,98,25,55,22,95,15,92,14,67,20,88,5,51,69,92,33,69,75,56,36,91,3,80,13,78,36,88,50,88,79,65,24,66,5,99,45,98,88,66,30,92,98,84,5,90,13,67,95,96,33,77,30,80,39,99,81,95,55,86,0,0,21,21,1,10,1,0,0,0,0,0,0]

    # Part 1: Find the oxygen system
    grid, oxygen_system_position = explore_area(program)
    print("Shortest distance to oxygen system:", grid.get(oxygen_system_position))

    # Part 2: Fill with oxygen
    if oxygen_system_position:
        minutes_to_fill = fill_with_oxygen(grid, oxygen_system_position)
        print("Minutes to fill with oxygen:", minutes_to_fill)

    # oxygen_system_position = (16,-16)
    # distance = 236
