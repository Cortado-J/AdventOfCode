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
net = {}
nodes = set()
for line in lines:
    bits = line.split(":")
    a = bits[0]
    b = bits[1].strip().split(" ")
    net[a] = b
    nodes.add(a)
    for bnode in b:
        nodes.add(bnode)

shownet = Network('1000px', '1000px', notebook=True)
# blue = '#1785b6'

# Nodes
for node in nodes:
    shownet.add_node(node, label=node, font='24px')
    
# Edges
for name, dests in net.items():
    for dest in dests:
        shownet.add_edge(name, dest, width=4, arrows='to')
shownet.show("day25visual.html")
# This produces a webpage visualisation which makes it easy to see which edges need to be cut...

def cut(a,b):
    if a in net:
        if b in net[a]:
            net[a].remove(b)
    if b in net:
        if a in net[b]:
            net[b].remove(a)
 
cut('ffv', 'mfs')
cut('mnh', 'qnv')
cut('tbg', 'ljh')

def size(node):
    gather = set()
    didinc = False

    def addnode(nod):
        if nod not in gather:
            gather.add(nod)
            return True
        return False
    didinc = addnode(node)

    while didinc:
       didinc = False
       for nod, dests in net.items():
            if nod in gather:
               for dest in dests:
                   if addnode(dest):
                       didinc = True
            for dest in dests:
                if dest in gather:
                    if addnode(nod):
                        didinc = True
    return len(gather)

# Find the sizes of two sizes of the cut:
sizea = size('ffv')
sizeb = size('mfs')

resulta = sizea * sizeb
print("Result A = ", resulta)
