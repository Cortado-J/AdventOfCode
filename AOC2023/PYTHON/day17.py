#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')

dirs = {'N': (0,-1), 'S': (0,1), 'E': (1,0), 'W': (-1,0)}
opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E', None: None}

lava = {} # { (x,y) : heat }
height = len(lines)
width = len(lines[0])
for y, row in enumerate(lines):
    for x, char in enumerate(row):
        lava[(x,y)] = int(char)
start_pos = (0,0)
end_pos = (width-1, height-1)

def mini(pos, min_straight, max_straight):
    # Dictionary of minimum travel
    tried = {} # = { (pos, straight_dist, straight_dir): dist }
    # where
    #  pos = position
    #  straight_dist = direction travelled in straight line to here
    #  straight_dir = direction travelled in straight line to here (or can be None if straight_dist is 0)
    #  dist = minimum distance found so far
    # The routine keeps a list of path ends needing search and repeatedley steps forward until all are longer than the minimum found
    lowest = width * height * 10 # Far too large!!

    nexts = set() # = { (pos, straight_dist, straight_dir) } The ones we need to try
    # energized = set() # {(x, y)} to keep track of what positions we have visited

    def do_step(pos, straight_dist, straight_dir, cost_so_far, path_so_far):
        step = (pos, straight_dist, straight_dir)
        new_cost = cost_so_far + lava[pos]
        if step in tried:
            old_cost, old_path = tried[step] # Don't actually need old_path as it is the previously found path
            if new_cost >= old_cost:
                # We're trying the same step but the distance is the same or longer
                # so this is not going to give us a better solution
                return
        # We've found a better solution so:
        # Store the better solution:
        new_path = path_so_far + (straight_dir if straight_dir != None else '')
        tried[step] = (new_cost, new_path)
        # And put this step down to be explored further:
        nexts.add(step)

    # Start by exploring the first position
    do_step(pos, 0, None, 0, '')
    # Set shortest to be unknown at the moment
    shortest = None
    shortest_path = None
    while len(nexts) > 0:
        next = nexts.pop()
        pos, straight_dist, straight_dir = next
        (cost_to_here, path_to_here) = tried[next] # We can rely on this being there because all steps put into "nexts" have also been put into tried
        if pos == end_pos:
            if straight_dist >= min_straight and straight_dist <= max_straight:
                if shortest == None or cost_to_here < shortest:
                    # First solution or better solution found
                    shortest = cost_to_here
                    shortest_path = path_to_here
                # We've got to the end so don't explore further
                continue

        # We haven't reached the end:
        if shortest != None and cost_to_here > shortest:
            # The distance is longer than a known solution
            # So we can abandon this path
            # (Note that if no solution has been found (shortest = = none) then we don't abandon the path) 
            continue
        
        for next_dir in ['N', 'E', 'S', 'W']:
            loop_straight_dist = straight_dist
            if next_dir == straight_dir:
                # We're going in the same direction
                if straight_dist >= max_straight:
                    # We've gone three so go no more!
                    continue
                # We haven't gone three so fine to carry on :-)
                loop_straight_dist += 1            
            elif next_dir == opposite[straight_dir]:
                # We can't reverse direction:
                continue
            else:
                # We're changing direction:
                if straight_dir != None and straight_dist < min_straight:
                    # We haven't gone far enough so go no more!
                    continue
                loop_straight_dist = 1
            next_x = pos[0] + dirs[next_dir][0]
            next_y = pos[1] + dirs[next_dir][1]
            if next_x < 0 or next_x >= width or next_y < 0 or next_y >= height:
                continue
            next_pos = (next_x, next_y)
            do_step(next_pos, loop_straight_dist, next_dir, cost_to_here, path_to_here)

    return(shortest, shortest_path)

resulta, shortest_path = mini(start_pos, 1, 3)
resulta = resulta - lava[start_pos]

print("Result A = ", resulta)
print(shortest_path)

resultb, shortest_path = mini(start_pos, 4, 10)
resultb = resultb - lava[start_pos]

print("Result B = ", resultb)
print(shortest_path)
