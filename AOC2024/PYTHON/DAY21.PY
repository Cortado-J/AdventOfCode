# #=============================================================
# import os
# script_dir = os.path.dirname(os.path.abspath(__file__))
# daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
# file_path = os.path.join(script_dir, f"day{daytext}.txt")
# text = open(file_path).read()
# #=============================================================

# lines = text.split('\n')

# from itertools import permutations

# # +---+---+---+
# # | 7 | 8 | 9 |
# # +---+---+---+
# # | 4 | 5 | 6 |
# # +---+---+---+
# # | 1 | 2 | 3 |
# # +---+---+---+
# #     | 0 | A |
# #     +---+---+
# num = {
#     "7": (0,0), "8": (1,0), "9": (2,0),
#     "4": (0,1), "5": (1,1), "6": (2,1),
#     "1": (0,2), "2": (1,2), "3": (2,2),
#     "0": (1,3), "A": (2,3), " ": (0,3)
# }

# def allmoves(xd, yd):
#     moves = []
#     if xd > 0:
#         moves += '>' * xd
#     elif xd < 0:
#         moves += '<' * (-xd)
#     if yd > 0:
#         moves += 'v' * yd
#     elif yd < 0:
#         moves += '^' * (-yd)
#     unique_sequences = set(permutations(moves))
#     return ["".join(seq) for seq in unique_sequences]

# xdel = {"<":-1, ">":1, "^":0, "v":0}
# ydel = {"<":0, ">":0, "^":-1, "v":1}

# def valid(pad, start, seq):
#     x,y = start
#     for char in seq:
#         x += xdel[char]
#         y += ydel[char]
#         if (x,y) == pad[" "]:
#             return False
#     return True

# def allnummoves(a,b):
#     posa = num[a]
#     posb = num[b]
#     ax,ay = posa
#     bx,by = posb
#     xd = bx-ax
#     yd = by-ay
#     gather = []
#     for m in allmoves(xd,yd):
#         if valid(num, posa, m):
#             gather.append(m)
#     return gather

# #     +---+---+
# #     | ^ | A |
# # +---+---+---+
# # | < | v | > |
# # +---+---+---+
# dir = {
#     " ": (0,0), "^": (1,0), "A": (2,0),
#     "<": (0,1), "v": (1,1), ">": (2,1)
# }

# def alldirmoves(a,b):
#     posa = dir[a]
#     posb = dir[b]
#     ax,ay = posa
#     bx,by = posb
#     xd = bx-ax
#     yd = by-ay
#     gather = []
#     for m in allmoves(xd,yd):
#         if valid(dir, posa, m):
#             gather.append(m)
#     return gather

# def numall(s):
#     s = "A" + s
#     for b0 in allnummoves(s[0],s[1]):
#         for b1 in allnummoves(s[1],s[2]):
#             for b2 in allnummoves(s[2],s[3]):
#                 for b3 in allnummoves(s[3],s[4]):
#                     yield [b0,b1,b2,b3]

# # Assumes using directional keypad
# # Assumes start and end at A
# memo = {}
# def short(s, depth):
#     if (s,depth) in memo:
#         return memo[(s, depth)]
#     if depth == 0:
#         return len(s)
#     total = 0
#     full = "A" + s + "A"
#     for index in range(len(full)-1):
#         a, b = full[index], full[index+1]
#         shortest = float('inf')
#         for move in alldirmoves(a,b):
#             move_to_press = move
#             if b != 'A':
#                 move_to_press += 'A'
#             newshort = short(move_to_press, depth-1)
#             shortest = min(shortest, newshort)
#         total += shortest
#     memo[(s,depth)] = total
#     return total

# def shortest(s,depth):    
#     shortestlen = float('inf')
#     print(f"{s=}")
#     for robot in numall(s):
#         mincost = 0
#         for bot in robot:
#             mincost += short(bot+"A",depth)
#         if mincost < shortestlen:
#             shortestlen = mincost
#     return shortestlen

# print(shortest("029A",2))

# # def comp(x):
# #     pseq, plen = shortest(x)
# #     bit = x[:-1]
# #     q = int(bit)
# #     print(x,pseq,plen,q,plen*q)
# #     return plen*q

# # parta = sum(comp(x) for x in ["671A", "083A", "582A", "638A", "341A"])
# # print("Part A:", parta)

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5]  # Get the day number as two digits
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
lines = text.split('\n')

from itertools import permutations

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
num = {
    "7": (0,0), "8": (1,0), "9": (2,0),
    "4": (0,1), "5": (1,1), "6": (2,1),
    "1": (0,2), "2": (1,2), "3": (2,2),
    "0": (1,3), "A": (2,3), " ": (0,3)
}

def allmoves(xd, yd):
    """
    Given an x-distance and y-distance, return all permutations
    of arrows that achieve exactly that offset. e.g. xd=2,yd=-1
    -> permutations of '>>^' with no duplicates.
    """
    moves = []
    if xd > 0:
        moves += '>' * xd
    elif xd < 0:
        moves += '<' * (-xd)
    if yd > 0:
        moves += 'v' * yd
    elif yd < 0:
        moves += '^' * (-yd)
    unique_sequences = set(permutations(moves))
    return ["".join(seq) for seq in unique_sequences]

xdel = {"<": -1, ">": 1, "^": 0, "v": 0}
ydel = {"<": 0,  ">": 0, "^": -1, "v": 1}

def valid(pad, start, seq):
    """
    Check if following seq from start stays off any invalid " " gap.
    """
    x, y = start
    for char in seq:
        x += xdel[char]
        y += ydel[char]
        if (x, y) == pad[" "]:
            return False
    return True

def allnummoves(a,b):
    """
    Return all shortest ways to move from numeric keypad button a to b.
    Each way is just the arrow-string (no 'A' press at the end).
    """
    posa = num[a]
    posb = num[b]
    ax, ay = posa
    bx, by = posb
    xd = bx - ax
    yd = by - ay
    gather = []
    for m in allmoves(xd, yd):
        if valid(num, posa, m):
            gather.append(m)
    return gather

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
dir = {
    "^": (1,0), "A": (2,0),
    "<": (0,1), "v": (1,1), ">": (2,1),
    " ": (0,0)
}

def alldirmoves(a, b):
    """
    Return all shortest ways to move from directional keypad button a to b.
    Each way is just the arrow-string (no 'A' press at the end).
    """
    posa = dir[a]
    posb = dir[b]
    ax, ay = posa
    bx, by = posb
    xd = bx - ax
    yd = by - ay
    gather = []
    for m in allmoves(xd, yd):
        if valid(dir, posa, m):
            gather.append(m)
    return gather

def numall(s):
    """
    Yields all combinations of numeric-move-strings for s[0]->s[1], s[1]->s[2], ...
    The string s here includes a starting 'A' in the calling code, so be mindful.
    """
    s = "A" + s
    for b0 in allnummoves(s[0], s[1]):
        for b1 in allnummoves(s[1], s[2]):
            for b2 in allnummoves(s[2], s[3]):
                for b3 in allnummoves(s[3], s[4]):
                    yield [b0, b1, b2, b3]

###############################################################################
# Updated short(...) function that keeps track of current arm position
# and handles depth==0 in a more keypad-accurate way.
###############################################################################

# We'll store memo as: memo[(s, depth, current)] -> cost
memo = {}

def short_segment(a, b, depth):
    """
    Cost of going from 'a' to 'b' (directional keypad buttons) at the given depth,
    including the press if b != 'A'.
    
    Returns (cost, end_position).
    The end_position is always b if we don't do weird extra moves,
    but we might keep that in mind if we wanted to chain more carefully.
    """
    # If we don't need to press (when b=='A' to aim at 'A' but not press it),
    # then we do not append the final 'A' keystroke. 
    # If we want to push b, we do append 'A'.
    
    # We'll build a key for memo that also includes a->b.
    key = (a, b, depth)
    if key in memo:
        return memo[key]
    
    # Get all arrow-move possibilities from a to b:
    possible_moves = alldirmoves(a, b)
    
    best = float('inf')
    for move in possible_moves:
        move_to_press = move + 'A'
        cost = short(move_to_press, depth-1, current='A')  # type 'move_to_press' on the *next* keypad
        if cost < best:
            best = cost
    
    memo[key] = best
    return best

def short(s, depth, current='A'):
    key = (s, depth, current)
    if key in memo:
        return memo[key]
    
    if depth == 0:
        cost = len(s)
        memo[key] = cost
        return cost
    
    if not s:
        memo[key] = 0
        return 0
    
    full = [current] + list(s)
    
    total_cost = 0
    for i in range(len(full) - 1):
        a = full[i]
        b = full[i + 1]
        seg_cost = short_segment(a, b, depth)
        total_cost += seg_cost
    
    memo[key] = total_cost
    return total_cost

# 'shortest' uses numall(...) for enumerating numeric moves,
# then sums cost of typing on the chain of keypads.
def shortest(s, depth):
    shortest_len = float('inf')
    for robot_moves in numall(s):
        # robot_moves is a list of 4 arrow-strings, e.g. [b0, b1, b2, b3]
        # each is the path from s[i] to s[i+1] on the numeric keypad
        # then we do `bot + "A"` to press the numeric button (like in original)
        mincost = 0
        for bot in robot_moves:
            # We append 'A' so that we press the button.
            # Then we compute the cost to produce that arrow-sequence on the chain of directional keypads.
            mincost += short(bot + "A", depth)
        
        if mincost < shortest_len:
            shortest_len = mincost
    
    return shortest_len

def comp(x,depth):
    bit = x[:-1]
    q = int(bit)
    lena = shortest(x,depth)
    return lena*q

codes = ["671A", "083A", "582A", "638A", "341A"]

parta = sum(comp(x,2) for x in codes)
print("Part A:", parta)

partb = sum(comp(x,25) for x in codes)
print("Part B:", partb)