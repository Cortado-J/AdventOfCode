def run_intcode(program):
    memory = program.copy()
    pointer = 0

    while True:
        opcode = memory[pointer]

        if opcode == 99:
            break
        elif opcode == 1:
            param1 = memory[memory[pointer + 1]]
            param2 = memory[memory[pointer + 2]]
            memory[memory[pointer + 3]] = param1 + param2
        elif opcode == 2:
            param1 = memory[memory[pointer + 1]]
            param2 = memory[memory[pointer + 2]]
            memory[memory[pointer + 3]] = param1 * param2
        else:
            raise Exception(f"Unknown opcode {opcode} at position {pointer}")

        pointer += 4

    return memory

def find_noun_verb(program, target_output):
    for noun in range(100):
        for verb in range(100):
            test_program = program.copy()
            test_program[1] = noun
            test_program[2] = verb
            output_memory = run_intcode(test_program)
            if output_memory[0] == target_output:
                return 100 * noun + verb
    raise Exception("No valid noun and verb found")

# Replace this with your actual puzzle input
puzzle_input = [1,9,10,3,2,3,11,0,99,30,40,50,0,0,0,0,0,0,0,0,0,0,0]
puzzle_input = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,6,19,23,1,10,23,27,2,27,13,31,1,31,6,35,2,6,35,39,1,39,5,43,1,6,43,47,2,6,47,51,1,51,5,55,2,55,9,59,1,6,59,63,1,9,63,67,1,67,10,71,2,9,71,75,1,6,75,79,1,5,79,83,2,83,10,87,1,87,5,91,1,91,9,95,1,6,95,99,2,99,10,103,1,103,5,107,2,107,6,111,1,111,5,115,1,9,115,119,2,119,10,123,1,6,123,127,2,13,127,131,1,131,6,135,1,135,10,139,1,13,139,143,1,143,13,147,1,5,147,151,1,151,2,155,1,155,5,0,99,2,0,14,0]

# puzzle_inputs = [
#     [1,0,0,0,99],
#     [2,3,0,3,99],
#     [2,4,4,5,99,0],
#     [1,1,1,4,99,5,6,0,99]]

# for puzzle_input in puzzle_inputs:
#     program_part1 = puzzle_input.copy()
#     output_memory = run_intcode(program_part1)
#     print(puzzle_input, output_memory)
    


# Part 1
program_part1 = puzzle_input.copy()
program_part1[1] = 12
program_part1[2] = 2
output_memory = run_intcode(program_part1)
result_part1 = output_memory[0]
print(f"Part 1 Result: {result_part1}")

# Part 2
target_output = 19690720
result_part2 = find_noun_verb(puzzle_input, target_output)
print(f"Part 2 Result: {result_part2}")
