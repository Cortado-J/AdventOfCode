#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
sections = text.split('\n\n\n\n')
effectslines = sections[0].split('\n\n')
trials = []
for block in effectslines:
    lines = block.splitlines()
    before = [int(x) for x in lines[0].split('[')[1].split(']')[0].split(',')]
    after  = [int(x) for x in lines[2].split('[')[1].split(']')[0].split(',')]
    ops    = [int(x) for x in lines[1].split(' ')]
    trial = (before, ops, after)
    trials.append(trial)

# Extract program for Part B:
program = []
for line in sections[1].splitlines():
    program.append([int(x) for x in line.split(' ')])

def exec(regs, OP, A, B, C):
    R = regs.copy()
    if   OP == 'addr': R[C] = R[A] + R[B]
    elif OP == 'addi': R[C] = R[A] + B
    elif OP == 'mulr': R[C] = R[A] * R[B]
    elif OP == 'muli': R[C] = R[A] * B
    elif OP == 'banr': R[C] = R[A] & R[B]
    elif OP == 'bani': R[C] = R[A] & B
    elif OP == 'borr': R[C] = R[A] | R[B]
    elif OP == 'bori': R[C] = R[A] | B
    elif OP == 'setr': R[C] = R[A]
    elif OP == 'seti': R[C] = A
    elif OP == 'gtir': R[C] = 1 if A > R[B] else 0
    elif OP == 'gtri': R[C] = 1 if R[A] > B else 0
    elif OP == 'gtrr': R[C] = 1 if R[A] > R[B] else 0
    elif OP == 'eqir': R[C] = 1 if A == R[B] else 0
    elif OP == 'eqri': R[C] = 1 if R[A] == B else 0
    elif OP == 'eqrr': R[C] = 1 if R[A] == R[B] else 0
    return R

oplist = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']

def couldbe(trial, opname):
    before, instruction, after = trial
    result = exec(before, opname, instruction[1], instruction[2], instruction[3])
    return result == after

def couldbelist(trial):
    return [opname for opname in oplist if couldbe(trial, opname)]

def couldbecount(trial):
    return len(couldbelist(trial))

resulta = sum([1 for trial in trials if couldbecount(trial) >= 3])
print("Result A = ", resulta)

possibles = {} # {opcode, <set of possible opnames>}

# The key step in the code below is the intersection: only a possibility if ALL trials of that opcode allow that name
for trial in trials:
    opcode = trial[1][0]
    poss = couldbelist(trial)
    if opcode not in possibles:
        possibles[opcode] = poss
    else:
        possibles[opcode] = set(poss).intersection(possibles[opcode])

def onlyelementof(s):
    assert len(s) == 1
    return list(s)[0]

# Now repeatedly identify opcodes with a single possible opname and remove the opname from all the other opcode's possibilities
available = set(oplist)
while available:
    for opcode, setofposs in possibles.items():
        if len(setofposs) == 1:
            opname = onlyelementof(setofposs)
            if opname in available:
                # Remove from all other opcodes:
                for opcoderem, setofpossrem in possibles.items():
                    if opcoderem != opcode: # The line representing 'other'
                        setofpossrem.discard(opname)
                available.discard(opname)
    
regs = [0,0,0,0]
for step in program:
    regs = exec(regs, onlyelementof(possibles[step[0]]), step[1], step[2], step[3]) # Note list(s)[0] is a way to extract the only element from the set s
resultb = regs[0]
print("Result B = ", resultb)
