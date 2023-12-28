# Use pyvis to display the network of nodes in a webpage
import pyvis
from pyvis.network import Network
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
modules = {}
states = {}
for line in lines:
    bits = line.split(" -> ")
    name = bits[0]
    type = None
    if name[0] in '%&':
        type = name[0]
        name = name[1:]
    dests = bits[1].split(", ")
    modules[name] = (type, dests)

net = Network('1000px', '1000px', notebook=True)
def add(name, color):
    net.add_node(name, label=name, color=color, font='24px')
    
# Nodes
for index, (name, (type, dests)) in enumerate(modules.items()):
    yellow = '#efd8a2'; peach = '#faac64'; blue = '#1785b6'; red = '#DE3737'
    color = {None:yellow, '%':peach, '&':blue}[type]
    add(name, color)
add('rx', color=red)

# Edges
for index, (name, (type, dests)) in enumerate(modules.items()):
    for dest in dests:
        net.add_edge(name, dest, width=4, arrows='to')

net.show("day20visual.html")
