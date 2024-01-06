#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.splitlines()
# print(lines)
# /->-\        
# |   |  /----\
# | /-+--+-\  |
# | | |  | v  |
# \-+-/  \-+--/
#   \------/   
dirs  = {'^': (0,-1), '>': (1,0), 'v': (0,1), '<': (-1,0)}
under = {'^': '|', 'v': '|', '>': '-', '<': '-'}
bounces = {('^', '/' ): '>',
           ('^', '\\'): '<',
           ('v', '/' ): '<',
           ('v', '\\'): '>',
           ('>', '/' ): '^',
           ('>', '\\'): 'v',
           ('<', '/' ): 'v',
           ('<', '\\'): '^'
           }
turndirs = '^<v>' # And can increase index by 1 (mod 3) to turn LEFT, 0 (mod 3) to go STRAIGHT, 3 (mod 3) to go RIGHT
turndelta = [1, 0, 3] # cycle of crossroad directions: increases in index into turndirs represents [LEFT, STRAIGHT, RIGHT]
def turncart(dir, turn): # Where turn is 0 for first turn, 1 for next, etc
    index = turndirs.index(dir)
    delta = turndelta[turn % 3]
    newindex = (index + delta) % 4
    return turndirs[newindex]

tracks  = {} # { (x,y): track }
carts = {} # { (x,y): (direction, turn) } (direction as ^v<>, turn as 0,1,2 which is index into turndelta)
for y, row in enumerate(lines):
    for x, char in enumerate(row):
        if char != '':
            pos = (x,y)
            track = char
            if char in dirs:
                carts[pos] = (char, 0)
                track = under[char]
            tracks[pos] = track
H = len(lines)
W = len(lines[0])

def show():
    for y in range(H):
        print("'", end='')
        for x in range(W):
            pos = (x,y)
            if pos in carts:
                print(carts[pos][0], end='')
            elif pos in tracks:
                print(tracks[pos], end='')
            else:
                print(' ', end='')
        print()

# show()

part = 'A'

def move(): #return False if ending
    global part
    # carts = { (x,y): (direction, turn) } 
    plan = sorted(carts.items() , key=lambda cart: [cart[0][1], cart[0][0]])
    for cartpos, (cartdir, cartturn) in plan:
        if cartpos in carts: # We need this extra check because it might have been removed because of a previous crash!
            newpos = (cartpos[0]+dirs[cartdir][0], cartpos[1]+dirs[cartdir][1])
            # Remove cart for now
            carts.pop(cartpos)
            if newpos in carts:
                if part == 'A':
                    print(f"Result A = '{newpos[0]},{newpos[1]}'")
                    part = 'B'
                # Remove cart we have hit!
                carts.pop(newpos)
                # And don't put back the one that just moved!
                if len(carts) == 1:
                    lastcartpos = list(carts.keys())[0]
                    print(f"Result B = '{lastcartpos[0]},{lastcartpos[1]}'")
                    return False
            else:
                # We know where cart will be next but we first need to find direction and turn:
                # Current direction is cartdir but need to establish new direction
                track = tracks[newpos]
                newdir = cartdir
                if track in '/\\':
                    # We need to bounce:
                    newdir = bounces[(cartdir, track)]
                if track == '+':
                    newdir = turncart(cartdir, cartturn)
                    cartturn = (cartturn + 1) % 3
                carts[newpos] = (newdir, cartturn)
    return True

while move():
    # show()
    pass
