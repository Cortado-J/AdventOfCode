#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
input = text.splitlines()

length = 10
xs = [0 for _ in range(length)]
ys = [0 for _ in range(length)]
visiteda = set()
visitedb = set()

def movehead(dir):
    if dir == 'R':
        xs[0] += 1
    if dir == 'L':
        xs[0] -= 1
    if dir == 'U':
        ys[0] += 1
    if dir == 'D':
        ys[0] -= 1

def check(cell):
    x = xs[cell]
    y = ys[cell]
    xp = xs[cell-1]
    yp = ys[cell-1]
    xd = x-xp
    yd = y-yp
    # If the head is ever two steps directly up, down, left, or right from the tail,
    # the tail must also move one step in that direction so it remains close enough:
    if xd == 2 and yd == 0:
        xs[cell] = xs[cell]-1
    if xd == -2 and yd == 0:
        xs[cell] = xs[cell]+1
    if xd == 0 and yd == 2:
        ys[cell] = ys[cell]-1
    if xd == 0 and yd == -2:
        ys[cell] = ys[cell]+1

    # Otherwise, if the head and tail aren't touching and aren't in the same row or column,
    # the tail always moves one step diagonally to keep up:
    if xd != 0 and yd != 0 and (abs(xd) > 1 or abs(yd) > 1):
        if xd > 0:
            xs[cell] = xs[cell]-1
        if xd < 0:
            xs[cell] = xs[cell]+1
        if yd > 0:
            ys[cell] = ys[cell]-1
        if yd < 0:
            ys[cell] = ys[cell]+1

def show():
    display = {}
    display[(0,0)] = 's'
    for cell in range(length-1,-1,-1):
        display[(xs[cell], ys[cell])] = cell
    print('==============================================')
    for y in range(15, -15, -1):
        for x in range(-15, 15):
            ch = '.'
            d = display.get((x, y))
            if d != None:
                if d == 0:
                    d = 'H'
                ch = d
            print(ch, end='')
        print('')

def move(dir):
    movehead(dir)
    for index in range(1,length):
        check(index)
    visiteda.add((xs[1], ys[1]))
    visitedb.add((xs[length-1], ys[length-1]))

def multimove(dir, num):
    for _ in range(num):
        move(dir)
        # show()

for line in input:
    bits = line.split(" ")
    multimove(bits[0], int(bits[1]))

parta = len(visiteda)
partb = len(visitedb)
print(f"Day {daytext}: Part A = {parta}")
print(f"Day {daytext}: Part B = {partb}")
