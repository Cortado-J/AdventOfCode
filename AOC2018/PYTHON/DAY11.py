size = 300
serial = 8
for y in range(1+1,size-1+1):
    for x in range(1+1,size-1+1):
        rackid = x+10
        power = (rackid * y + serial) * rackid
        val = (power - (power % 100))/100 - 5
