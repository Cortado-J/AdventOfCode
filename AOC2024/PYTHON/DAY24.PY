#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n\n')
# x00: 1
# x01: 1
# y00: 0
# y01: 1
REG={}
for line in lines[0].split("\n"):
    # print(f"#{line}#")
    REG[line[0:3]] = int(line[5:6])
print(REG)
# x00 AND y00 -> z00
# x01 XOR y01 -> z01
# x02 OR y02 -> z02
GATES = {}
WIRES = {}
def addwire(wire, link):
    if wire not in WIRES:
        WIRES[wire] = set()
    if link not in WIRES:
        WIRES[link] = set()
    WIRES[wire].add(link)
for line in lines[1].split("\n"):
    bits = line.split(" ")
    a, OP, b, dest = bits[0], bits[1], bits[2], bits[4]
    GATES[dest] = ((a, OP, b))
    addwire(a,dest)
    addwire(b,dest)

def eval(dest):
    if dest in REG:
        return REG[dest]
    
    (a, OP, b) = GATES[dest]
    a, b = eval(a), eval(b)

    result = None
    if OP == "AND":
        result = a & b
    elif OP == "OR":
        result = a | b
    elif OP == "XOR":
        result = a ^ b
    return result

parta = 0
for reg in GATES.keys():
    if reg[0] == "z":
        zval = eval(reg)
        zmult = 2**int(reg[1:3])
        parta += zmult * zval

print("Part A:", parta)
print("-------------------------------------")

partb = 0
# Adder requires:
# 2 XOR gates 
# 2 AND gates
# 1 OR gate

# 44 Adders requires:
# 88 XOR gates 
# 88 AND gates
# 44 OR gate

# Count of gate types in main input:
# ANDS 	89
# XORS	69
# ORS	44

from pyvis.network import Network
import webbrowser

# Create a network object
net = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="black")

# METHOD 1: Nodes are wires and Edges are Gates 
for node in WIRES.keys():
    net.add_node(node, label=node, color="black", font='120px')

for dest, (a,op,b) in GATES.items():
    yellow = '#efd8a2'; peach = '#faac64'; blue = '#1785b6'; red = '#DE3737'
    color = {"AND":yellow, 'OR':peach, 'XOR':blue}[op]
    net.add_edge(a, dest, width=12, arrows='to', color=color)
    net.add_edge(b, dest, width=12, arrows='to', color=color)

# Physics layout for optimal node placement
net.toggle_physics(True)

# Save the HTML file
output_path = "network2.html"
net.show(output_path, notebook=False)

# Open the HTML file in the default web browser
absolute_path = os.path.abspath(output_path)
webbrowser.open(f"file://{absolute_path}")

# By inspection need to swap:
# In bit 5: z05, gdd
# In bit 9: z09, cwt
# In bit 20: css, jmv
# In bit 37: z37, pqt
# Which gives answer as:
partb = "css,cwt,gdd,jmv,pqt,z05,z09,z37"
print("Part B:", partb)
print("-------------------------------------")