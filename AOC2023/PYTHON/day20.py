import numpy as np
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
# broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a

modules = {} # { name : (type, [dest1, dest2, ...]) }
states = {}  # { name : 
             #           For flip-flops:    state } (state = True means "on")
             #           For conjunctions:  {input_name: hilo} } (dictionary of inputs mapped to states)
for line in lines:
    bits = line.split(" -> ")
    name = bits[0]
    type = None
    if name[0] in '%&':
        type = name[0]
        name = name[1:]
    dests = bits[1].split(", ")
    modules[name] = (type, dests)
    if type == "%":
        states[name] = False
    elif type == "&":
        states[name] = {} # Start with empty conjunction inputs
print(modules)
print(states)

# Set "memory" of conjunctions:
for name, (type, dests) in modules.items():
    for dest in dests:
        if dest in modules: # This needed to cope with modules that don't have a rule (such as "rx")
            if modules[dest][0] == '&': # It's the destination type being a conjunction we're concerned about
                states[dest][name] = 0

stack = [] # [(source, hilo, name)] # Sending a pulse from source to the module 'name' 

def push(source, hilo, name):
    stack.append((source, hilo, name))

def pushall(hilo, name):
    for dest in modules[name][1]:
        push(name, hilo, dest)

rx_low = False

def button():
    push('button', 0, 'broadcaster')

presses = 0
states_to_monitor = ['hh', 'lk', 'fh', 'fn']
keep_states = dict([(name,None) for name in states_to_monitor])
def done():
    return sum(1 for step in keep_states.values() if step is None) == 0

def exec(command):
    source, hilo, name = command
    if name not in modules:
        # This module doesn't do anything
        if name == 'rx':
            rx_low = True
        return
    
    type = modules[name][0]

    if type == '%':
        # Flip-flop
        if hilo == 0: # Low
            if states[name] == False:
                states[name] = True
                pushall(1, name) # High
            else:
                states[name] = False
                pushall(0, name) # Low
    elif type == '&':
        # Conjunction
        # When a pulse is received, the conjunction module first updates its memory for that input.
        states[name][source] = hilo

        # Keep the first time the pulse goes low for the selected conjunctions:
        if hilo == 0:
            if name in states_to_monitor:
                if keep_states[name] == None:
                    keep_states[name] = presses

        # Then, if it remembers high pulses for all inputs,        
        if min(states[name].values()) == 1:
            # it sends a low pulse;
            pushall(0, name)
        else:
            # otherwise, it sends a high pulse.
            pushall(1, name)
    else:
        # It's just an ordinary module so
        # pass on pulse to all destinations
        pushall(hilo, name)

def run():
    lo_count = 0
    hi_count = 0
    while len(stack) > 0 or rx_low:
        next = stack.pop(0)
        # print(next)
        if next[1] == 0:
            lo_count += 1
        else:
            hi_count += 1
        exec(next)
    return lo_count, hi_count

lo_total = 0
hi_total = 0
rx_low = False
for loop in range(1000000):
# while not rx_low:

    presses += 1
    if presses % 10000 == 0:
        print(presses)

    button()
    lo, hi = run()
    lo_total += lo
    hi_total += hi
    if loop == 999:
        resulta = lo_total * hi_total 
    if done():
        break

resulta = lo_total * hi_total
print("Result A=", resulta )

resultb = np.lcm.reduce(list(keep_states.values()))
print("Result B=", resultb )
