size = 300
serial = 9306

powers = {}
for y in range(1,size+1):
    for x in range(1,size+1):
        rackid = x + 10
        power = (rackid * y + serial) * rackid
        power = ((power - (power % 100))/100 ) % 10 - 5
        power = int(power)
        powers[(x,y)] = power

def solve(windowmin, windowmax):
    boxpowers = {}
    for windowsize in range(1, windowmax+1): # Note that even though the windowmin may be greater than 1 the range here starts from 1 because the boxpowers are worked out based on smaller box sizes.
        print(windowsize, end=" ")
        rangemax = size-(windowsize-1)+1
        for y in range(1,rangemax):
            for x in range(1,rangemax):
                boxpower = None
                if windowsize == 1:
                    boxpower = powers[(x,y)]
                else:
                    boxpower = boxpowers[(x,y,windowsize-1)]
                    for dy in range(windowsize):
                        boxpower += powers[(x+windowsize-1,y+dy)]
                    for dx in range(windowsize-1): # Note the -1 to avoid doublecounting
                        boxpower += powers[(x+dx,y+windowsize-1)]
                boxpowers[(x,y,windowsize)] = boxpower
    print()
    maxpower = -100000000
    bigx = None
    bigy = None
    bigwindow = None
    for windowsize in range(windowmin, windowmax+1):
        rangemax = size-(windowsize-1)+1
        for y in range(1,rangemax):
            for x in range(1,rangemax):
                boxpower = boxpowers[(x,y,windowsize)]
                if boxpower > maxpower:
                    maxpower = boxpower
                    bigx = x
                    bigy = y
                    bigwindow = windowsize
    return bigx, bigy, bigwindow

bigx, bigy, bigwindow = solve(3,3)
print(f"Result A = '{bigx},{bigy}' (Enter answer 'X,Y' with no spaces!)")

print("Warning - For Part B when max windowsize is 300 the calculations take about 10 minutes.")
print("Because the answer is known to be less than 20 the max windowsize is reduced to 20 so it runs faster.")
bigx, bigy, bigwindow = solve(1,20)
print(f"Result B = '{bigx},{bigy},{bigwindow}' (Enter answer 'X,Y,W' with no spaces!)")
