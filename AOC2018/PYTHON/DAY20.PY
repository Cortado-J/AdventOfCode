#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
# ^ENWWW(NEEE|SSE(EE|N))$
reg = text
assert reg[0] == '^'
assert reg[-1] == '$'
reg = reg[1:-1]
# print(reg)

dirs = {'N':(0,-1), 'E':(1,0), 'S':(0,1), 'W':(-1,0)}

maze = {} # ((x,y): (east, south)) where (x,y) is the coordinates of the position and east and south are chars for the doors in those directions

# If a room doesn;t exist then build it
def recroom(pos):
    if pos not in maze:
        maze[pos] = ('?', '?')

# Record a door from the current cell in an easterly or southerly direction
# This is a helper function for the more general recdoor
def recdoorEastOrSouth(pos, dir):
    assert dir in 'ES', "dir must be E or S"
    recroom(pos) # To check room exists)
    if dir == 'E':
        maze[pos] = ('.', maze[pos][1])
        recroom((pos[0]+1,pos[1])) # To check the room on the other side of the door exists too!
    elif dir == 'S':
        maze[pos] = (maze[pos][0], '.')
        recroom((pos[0],pos[1]+1)) # To check the room on the other side of the door exists too!

# Record a door from the current cell (works for NSEW)
# And return the new position from going through that door
def recdoor(pos, dir):
    if dir not in 'NSEW':
        return pos
    newpos = (pos[0]+dirs[dir][0], pos[1]+dirs[dir][1])
    if dir in 'ES':
        recdoorEastOrSouth(pos, dir)
    elif dir == 'N':
        recdoorEastOrSouth(newpos, 'S')
    elif dir == 'W':
        recdoorEastOrSouth(newpos, 'E')
    return newpos

# Show the maze
def show(room, doorH, doorV):
    print("======================================================================")
    minx, miny, maxx, maxy = 10000, 10000, -10000, -10000
    for (x,y), (east,south) in maze.items():
        minx = min(minx, x)
        maxx = max(maxx, x)
        miny = min(miny, y)
        maxy = max(maxy, y)
    for y in range(miny-1, maxy+1):
        if y > miny-1:
            for x in range(minx-1, maxx+1):
                pos = (x,y)
                east = maze[pos][0] if pos in maze else "#"
                if x > minx-1:
                    print("X" if x == 0 and y == 0 else room, end="")
                print(doorV if east == '.' else "#", end="")
            print("")
        for x in range(minx-1, maxx+1):
            pos = (x,y)
            south = maze[pos][1] if pos in maze else "#"
            if x > minx-1:
                print(doorH if south == '.' else "#", end="")
            print("#", end="")
        print("")
    print("======================================================================")

# Construct the page rcursively:
def construct(frompos, command):
    pos = frompos
    while command:
        char = command[0]
        command = command[1:]
        if char in "NSEW":
            pos = recdoor(pos, char)
        elif char == "(":
            nest = 1
            charindex = 0
            options = ['']
            while nest > 0:
                ch = command[charindex]
                if ch == "(":
                    nest += 1
                if nest > 1:
                    # We're within nested brackets so don;t parse, just record the characters as any further nesting/options will be dealt with in the next level of recursion
                    options[-1] += ch
                else: # nest == 1:
                    # At nest level 1 we do want to parse options
                    if ch == "|":
                        # Another options so create an empty one:
                        options.append('')
                    elif ch in 'NSEW':
                        # Extend the option with commands:
                        options[-1] += ch
                if ch == ")":
                    nest -= 1
                charindex += 1
            command = command[charindex:]
            for option in options:
                construct(pos, option)


# Construct the maze:
startpos = (0,0)
recroom(startpos)
construct(startpos, reg)
# And show it:
show(" ", " ", " ")
# show(".", "-", "|") # Alternative version that matches the instructions style

# For the "shortest path to a room would require passing through the most doors"
# We can simply count the number of steps to flood fill the whole maze (beginning at the starting position)!
# Because we won;t need the maze after this we can dismantle it and see how many cycles that takes.
# For efficiency we will keep a frontier from which we find the next strip to dismantle

def reachabledir(pos, dir):
    if pos not in maze:
        return False
    if dir == "E":
        return maze[pos][0] == "."
    if dir == "S":
        return maze[pos][1] == "."
    if dir == "W":
        frompos = (pos[0]-1, pos[1]) # The room to the west
        if frompos not in maze:
            return False
        return maze[frompos][0] == "." # Which is the east door of the room to the west
    if dir == "N":
        frompos = (pos[0], pos[1]-1) # The room to the north
        if frompos not in maze:
            return False
        return maze[frompos][1] == "." # Which is the south door of the room to the north

def reachable(pos):
    result = set()
    for dir, (dx, dy) in dirs.items():  # dirs = {'N':(0,-1), 'E':(1,0), 'S':(0,1), 'W':(-1,0)}
        if reachabledir(pos, dir):
            newpos = (pos[0]+dx, pos[1]+dy)
            if newpos in maze:
                result.add(newpos)
    return result

step = 0
frontier = set()
frontier.add(startpos)
resultb = None
while maze:
    # Create a newfrontier as all positions reachable from the frontier
    newfrontier = set()
    for pos in frontier:
        newfrontier.update(reachable(pos))
    # print("Frontier:", frontier, "New Frontier:", newfrontier)
    # Then remove the frontier from the maze
    for pos in frontier:
        if pos in maze:
            del maze[pos]
    # And finally make the frontier be the newfrontier for the next iteration
    frontier = newfrontier
    step += 1
    if step == 1000:
        resultb = len(maze) # Part B is just counting the number of rooms left in the maze at step 1000!

resulta = step-1
print("Result A = ", resulta)
print("Result B = ", resultb)
