#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')

import networkx as nx
import itertools as it

G = nx.Graph()
G.add_edges_from((line[0:2], line[3:5]) for line in lines)
cliques = list(nx.find_cliques(G))
sets_of_three = {
    tuple(sorted(three))
    for clique in cliques
    for three in it.combinations(clique, 3)
    if any(node.startswith("t") for node in three)
}
parta = len(sets_of_three)
print("Part A:", parta)

largest_clique = max(cliques, key=len)
partb = ",".join(sorted(largest_clique))
print("Part B:", partb)







