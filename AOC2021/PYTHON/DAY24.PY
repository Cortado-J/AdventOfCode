import time

def alu_program(instructions, inputs):
    # Use a dictionary to store the variables w, x, y, z
    vars = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    input_counter = 0

    def get_value(val):
        if val in vars:
            return vars[val]
        return int(val)

    for instr in instructions:
        parts = instr.split()
        op = parts[0]
        a = parts[1]

        if op == 'inp':
            vars[a] = inputs[input_counter]
            input_counter += 1
        else:
            b = parts[2]
            b_value = get_value(b)

            if op == 'add':
                vars[a] += b_value
            elif op == 'mul':
                vars[a] *= b_value
            elif op == 'div':
                if b_value == 0:
                    raise ValueError("Attempt to divide by zero")
                vars[a] //= b_value
            elif op == 'mod':
                if vars[a] < 0 or b_value <= 0:
                    raise ValueError("Invalid mod operation")
                vars[a] %= b_value
            elif op == 'eql':
                vars[a] = 1 if vars[a] == b_value else 0

    return vars['w'], vars['x'], vars['y'], vars['z']


def find_largest_model_number(instructions):
    # Split instructions into chunks, each starting with an 'inp' instruction
    chunks = []
    current_chunk = []
    for instr in instructions:
        if instr.startswith('inp') and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
        current_chunk.append(instr)
    chunks.append(current_chunk)

    # Cache to store already visited states
    cache = {}

    def search(index, z, model_number):
        if index == 14:
            return model_number if z == 0 else None

        if (index, z) in cache:
            return None

        # Loop over possible digits from 9 to 1 (for the largest model number)
        for digit in range(9, 0, -1):
            new_model_number = model_number + [digit]
            w, x, y, new_z = alu_program(chunks[index], [digit] + [z])

            result = search(index + 1, new_z, new_model_number)
            if result is not None:
                return result

        # Cache the failed state
        cache[(index, z)] = None
        return None

    # Start the search from the first chunk with z = 0
    largest_model_number = search(0, 0, [])
    if largest_model_number:
        return int(''.join(map(str, largest_model_number)))
    return None


# Inline MONAD instructions
instructions = """
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 14
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x 0
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -6
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 3
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -3
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 14
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -2
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 7
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -9
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -2
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y""".strip().split("\n")

# Find the largest valid model number
largest_model_number = find_largest_model_number(instructions)
print(f"Largest valid model number: {largest_model_number}")
