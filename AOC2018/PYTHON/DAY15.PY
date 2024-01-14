#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
rows = text.splitlines()
H = len(rows)
W = len(rows[0])
cave = set() # Just a set of walls

units = {}  # { (x,y): (type, hitpoints)  }  type = 'G' or 'E'
starthp = 200
elfattackpower = 3
goblinattackpower = 3
dirs = [(0,-1), (-1,0), (1,0), (0,1)] # In reading order!

for y in range(H):
    for x in range(W):
        pos = (x,y)
        char = rows[y][x]
        if char in 'GE':
            units[pos] = (char, starthp)
        elif char == '#':
            cave.add(pos)

startunits = units.copy()

def setup(elfattack):
    global elfattackpower
    global units
    elfattackpower = elfattack
    units = startunits.copy()

def countunitsoftype(type):
    return len([unit for unit in units.values() if unit[0] == type])

def attackpower(pos):
    type = units[pos][0]
    if type == 'G':
        return goblinattackpower
    if type == 'E':
        return elfattackpower
    return None

def offset(pos, dir):
    return (pos[0]+dir[0], pos[1]+dir[1])

def neighbours(pos):
    for dir in dirs:
        newpos = offset(pos, dir)
        if 0 <= newpos[0] < W and 0 <= newpos[1] < H:
            yield newpos

def get(pos):
    if pos in cave: return '#'
    if pos in units.keys(): return units[pos][0]
    return '.'

def show():
    for y in range(H):
        gather = ""
        for x in range(W):
            pos = (x,y)
            char = get(pos)
            print(char, end="")
            if char in "GE":
                if gather:
                    gather += ", "
                hitpoints = units[pos][1]
                gather += f"{char}({hitpoints})"
        if gather:
            print(f"   {gather}", end="")
        print()
    print()

def isenemy(type, potentialenemytype):
    assert type in 'GE'
    return potentialenemytype in 'GE' and potentialenemytype != type

def enemyneighbours(pos):
    type = get(pos)
    assert type in 'GE'
    for neigh in neighbours(pos):
        neightype = get(neigh)
        if isenemy(type, neightype):
            yield neigh

def enemyneighbourswithhp(pos):
    for neigh in enemyneighbours(pos):
        hitpoints = units[neigh][1]
        posandhp = (neigh, hitpoints)
        yield posandhp

def allopen():
    for y in range(H):
        for x in range(W):
            pos = (x,y)
            if get(pos) == '.':
                yield pos

# Find all open spaces adjacent to pos
def openadjacent(pos):
    for neigh in neighbours(pos):
        if get(neigh) == '.':
            yield neigh

# Find all enemies of pos
def allenemies(pos):
    type = get(pos)
    for pos, (enemytype, _) in units.items():
        if isenemy(type, enemytype):
            yield pos

# Find all open spaces adjacent to any enemies of pos
def allopenadjacenttoenemies(pos):
    adjacents = set()
    for enemy in allenemies(pos):
        adjacenttoenemy = openadjacent(enemy)
        adjacents = adjacents.union(adjacenttoenemy)
    return adjacents
        
def isearlier(pos, posthan):
    return pos[0] < posthan[0] if pos[1] == posthan[1] else pos[1] < posthan[1]

def readingorder(posns):
    return sorted(posns , key=lambda pos: [pos[1], pos[0]]) if posns else []

def earliestreadingorder(posns):
    return readingorder(posns)[0] if posns else None

# We're moving from posa to posb with open spaces as a set called opens
# This is recursive and when we move, we remove the used spaces from the opens set
# Return is: (distance, firststeps) where :
#    distance is the shortest found distance (there may be more than one!)
#    firststeps is a set containing the first steps on each of the shortest paths
def shortest(posa, posb, opens):
    for neigh in neighbours(posa):
        if neigh == posb:
            setwithposb = set()
            setwithposb.add(posb)
            return (1, setwithposb)
    shortestdistance = 1000000
    firststeps = set()
    newopens = set(openadjacent(posa))
    if len(newopens) == 0:
        return (1000000, None)
    for next in newopens:
        openscopy = opens.copy()
        if next in openscopy:
            openscopy.remove(next)
            distance, positionsoffirststepofshortestpathinreadingorder = shortest(next, posb, openscopy)
            # distance, positionsoffirststepofshortestpathinreadingorder = shortest(posb, next, openscopy)
            nextdistance = distance + 1
            if nextdistance < shortestdistance:
                shortestdistance = nextdistance
                firststeps.clear()
                firststeps.add(next)
            elif nextdistance == shortestdistance:
                if positionsoffirststepofshortestpathinreadingorder:
                    firststeps.add(next)
    return shortestdistance, firststeps

# We're moving from posa to posb with open spaces as a set called opens
# Return is: (distance, firststep) where :
#    distance is the shortest found distance (there may be more than one!)
#    firststep is the earliest (in reading order) first step of any of those shortest paths
def earliestshortest(posa, posb, opens):
    shortestdistance, firststeps = shortest(posa, posb, opens)
    return shortestdistance, earliestreadingorder(firststeps)

def readingorderunits():
    return sorted(units.items() , key=lambda u: [u[0][1], u[0][0]])

def delta(posa, posb):
    return (posa[0]-posb[0], posa[1]-posb[1])

def manhattandelta(d):
    return abs(d[0]) + abs(d[1])

def adjacent(posa, posb):
    return manhattandelta(delta(posa, posb)) == 1

# take a return and return the number of targets found in that turn
def doturn(unit, type):
    # Turn
    current = unit

    active = False
    enemyneigh = set(enemyneighbourswithhp(current))
    if not enemyneigh:
        ########################
        ######## MOVING ########
        ########################

        # Get a set of all the cells which are open (i.e. don't have a cave, goblin or elf)
        opens = set(allopen())
        # As we search for paths, opens will gradually be used up!
        # We're going to effectively do a flood fill on the open space starting at the current cell
        # We're going to do it step by step so at each step we generate the next layer of cells which can be reached
        # And for each endpoint we keep track of where the startpoint was which led here
        # If there are multiple starts which led to the same end in the same number of steps then we keep the earliest (in reading order)

        # Create the first "layer"
        layer = {} # {end: earlieststart}
        # Get the possible starting points for paths as the first layer
        for start in openadjacent(current):
            layer[start] = start # paths start at their own start !!!
            opens.discard(start)
        targets = set(allopenadjacenttoenemies(current))
        startofearliesttarget = None
        while layer:
            # Let's see if there's any targets in the layer
            targetsinlayer = set(layer.keys()).intersection(targets)
            if targetsinlayer:
                # This layer includes at least one target:
                # Find the earliest of those targets:
                earliesttarget = earliestreadingorder(targetsinlayer)
                startofearliesttarget = layer[earliesttarget]
                # And we're done hunting for an accessible
                break

            # No targets in the layer so we need do another layer:
            nextlayer = {} # nextlayer which is structured same as layer: {end: earlieststart}
            for pos, earlieststartofpathtopos in layer.items():
                for neigh in openadjacent(pos):
                    if neigh in opens: # Because we don't want to go back into areas we have already looked at
                        assert neigh not in layer # Because none of layer should be in opens!
                        earlierstart = earlieststartofpathtopos
                        if neigh in nextlayer:
                            # We've already found path to this cell so need to just keep the one with the earlier (reading order) start:
                            earlieststartofanypreviouspaths = nextlayer[neigh]
                            earlierstart = earliestreadingorder([earlierstart, earlieststartofanypreviouspaths])
                        nextlayer[neigh] = earlierstart
                        # It's tempting to remove neigh from opens here but there might be another path to the same point!
                        # So instead the whole of the next layer is constructed and then removed from opens below
            # We've prepared the next layer:
            # First lets remove it from opens:
            for pos in nextlayer.keys():
                opens.discard(pos)
            # And now we can treat this as layer in the next round:
            layer = nextlayer
            # Of course if nextlayer is empty then so will layer be and the while loop will end

        if startofearliesttarget != None:
            # Do the move by:
            units[startofearliesttarget] = units[current] # Copying the unit to the new chosen position
            del units[current]                            # Deleting the old position
            current = startofearliesttarget
            active = True

        # The logic specifies that if none reachable then end the turn
        #   This is handled without any code because if none are reachable then in the attack code below
        #   There won't be any enemy neighbours!

    ##########################
    ####### ATTACKING ########
    ##########################
    # At this point we are dealing with unit at current:
    #   EITHER we found ourselves next to a valid enemy;
    #   OR     we have moved a step towards the chosen one and that might mean we are next to a valid enemy
    # We now drop any previous working and consider what enemies are adjacent to us:
    enemyneigh = set(enemyneighbourswithhp(current))
    if enemyneigh:
        # We've found at least one enemy neighbour so
        # Work out minimum hitpoints
        minhitpoints = min([hp for _, hp in enemyneigh])
        # Get all with that number of hitpoints
        enemieswithminhitpoints = [enemy for enemy, hp in enemyneigh if hp == minhitpoints]
        # Choose the earliest in reading order
        chosenenemy = earliestreadingorder(enemieswithminhitpoints)
        # Do the actual attack
        enemytype, enemyhitpoints = units[chosenenemy]
        power = attackpower(current)
        if enemyhitpoints <= power:
            # The enemy has been killed:
            del units[chosenenemy]
        else:
            units[chosenenemy] = (enemytype, enemyhitpoints - power)
        active = True
    return active

def doround():
    turnsinround = readingorderunits() #.copy()?
    activity = 0
    for unit, (type, hitpoints) in turnsinround:
        if unit in units: # Need this because units can be killed in previous turns!!
             if doturn(unit, type):
                 activity += 1
    return activity

def combat(elfpower):
    setup(elfpower)
    elfcountatstart = countunitsoftype('E')
    print("Initially with elfattackpower = ", elfpower)
    show()
    round = 0
    while doround() > 0:
        round += 1
        print(f"After {round} round{'' if round == 1 else 's'}:")
        show()
    completerounds = round # For tests this is one less!!  To do with whether the round is complete!
    remaininghitpoints = sum([hp for type, hp in units.values()])
    winningside = list(units.values())[0][0]
    elfcountatend = countunitsoftype('E')
    elfdeaths = elfcountatend - elfcountatstart
    print(f"COMBAT: elfattack={elfpower}, completerounds={completerounds}, remaininghitpoints={remaininghitpoints}, winningside={winningside}, elfdeaths={elfdeaths}")
    return completerounds, remaininghitpoints, winningside, elfdeaths

# Part A:
completerounds, remaininghitpoints, winningside, elfdeaths = combat(3)
outcome1 = completerounds * remaininghitpoints
outcome2 = (completerounds-1) * remaininghitpoints
print("Result A = ", outcome1, "OR", outcome2)

elfenough = 4
while True:
    completerounds, remaininghitpoints, winningside, elfdeaths = combat(elfenough)
    if elfdeaths == 0:
        outcome1 = completerounds * remaininghitpoints
        outcome2 = (completerounds-1) * remaininghitpoints
        print("Result B = ", outcome1, "OR", outcome2)
        break
    elfenough += 1
