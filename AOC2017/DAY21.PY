#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
rows = text.splitlines()

# Sample: "../.# => ##./#../..."
def size(pat): return len(pat.split("/")) 
def get(pat,x,y): return pat[(size(pat)+1)*y+x]
def fliph(pat): return "/".join([line[::-1] for line in pat.split("/")])
def flipv(pat): return "/".join(pat.split("/")[::-1])
def rotc(pat):
    gather = ""
    siz = size(pat)
    for x in range(siz):
        for y in range(siz):
            gather += get(pat, x, siz-y-1)
        if x != siz-1:
            gather += "/"
    return gather

rules2x2 = {}
rules3x3 = {}
for row in rows:
    pattern = row.split(" => ")[0]
    output  = row.split(" => ")[1]
    rules = rules2x2 if size(pattern) == 2 else rules3x3
    flip = fliph(pattern)
    
    rules[pattern] = output
    rules[rotc(pattern)] = output
    rules[rotc(rotc(pattern))] = output
    rules[rotc(rotc(rotc(pattern)))] = output
    rules[flip] = output
    rules[rotc(flip)] = output
    rules[rotc(rotc(flip))] = output
    rules[rotc(rotc(rotc(flip)))] = output

print("2x2")
for input, output in rules2x2.items():
    print(input, "=>", output)
print("3x3")
for input, output in rules3x3.items():
    print(input, "=>", output)

def extract(pat, basex, basey, extractsize):
    gather = ""
    for dy in range(extractsize):
        for dx in range(extractsize):
            gather += get(pat, basex+dx, basey+dy)
            # gather += pat[(basex+dx)+(patsize+1)*(basey+dy)]
        if dy != extractsize-1:
            gather += "/"
    return gather

start = ".#./..#/###"
working = start

def gen():
    global working
    siz = size(working)
    out = {}
    outsize = None
    if siz % 2 == 0:
        tilesiz = siz // 2
        for tx in range(tilesiz):
            for ty in range(tilesiz):
                tile = extract(working, tx*2, ty*2, 2)
                tileout = rules2x2[tile]
                for x in range(3):
                    for y in range(3):
                        pos = (tx*3+x, ty*3+y)
                        out[pos] = get(tileout, x, y)
        outsize = tilesiz * 3
    else:
        tilesiz = siz // 3
        for tx in range(tilesiz):
            for ty in range(tilesiz):
                tile = extract(working, tx*3, ty*3, 3)
                tileout = rules3x3[tile]
                for x in range(4):
                    for y in range(4):
                        pos = (tx*4+x, ty*4+y)
                        out[pos] = get(tileout, x, y)
        outsize = tilesiz * 4
    gather = ""
    for y in range(outsize):
        for x in range(outsize):
            pos = (x, y)
            gather += out[pos]
        if y != outsize-1:
            gather += "/"
    working = gather

def show(pat):
    for line in pat.split("/"):
        print(line)
print("=================")
show(working)
for generation in range(1, 18+1):
    print(f"Generation {generation} ...", end="")
    gen()
    number = working.count('#')
    print(f" Cell count = {number}")
    # if generation <= 5:
    #     show(working)
    if generation == 5:
        resulta = number
        print(f"Result A ({generation =})= {resulta}")
    if generation == 18:
        resultb = number
        print(f"Result B ({generation =})= {resultb}")
