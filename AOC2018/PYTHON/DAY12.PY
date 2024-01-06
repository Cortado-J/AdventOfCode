#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
sections = text.split("\n\n")
# initial state: #..#.#..##......###...###

# ...## => #
# ..#.. => #
initialstate = sections[0].split(":")[1].strip()
genmap = {}
for line in sections[1].splitlines():
    bits = line.split(" => ")
    genmap[bits[0]] = bits[1]

state = initialstate
indexoffset = 0
memoise = {}

def plantsum():
    sum = 0
    index = -indexoffset
    for ch in state:
        if ch == '#':
            sum += index
        index += 1
    return sum

def ensuredotsonends():
    global state
    global indexoffset
    if state[:3] != "...":
        extra = (3-state.index("#"))
        state = ("." * extra) + state
        indexoffset += extra
    if state[-3:] != "....":
        extra = (3-state[::-1].index("#"))
        state = state + ("." * extra)

ensuredotsonends()

def generate():
    global state
    newstate = '..'
    ensuredotsonends()
    for index in range(2, len(state)-2):
        bit = state[index-2:index+2+1]
        next = genmap[bit] if bit in genmap else '.'
        newstate += next
    newstate += '..'
    state = newstate
    ensuredotsonends()

genforresulta = 20
# Testing tells us the pattern is the same but just sliding right after generation 100
genmaxneeded = 200

stepthatisrepeatedlater = None
stepthatrepeatsanearlierone = None

for gen in range(1,genmaxneeded+1):
    generate()
    stateformemoise = state.strip(".")
    # print(stateformemoise, gen, plantsum())
    if gen == genforresulta:
        resulta = plantsum()
        print("Result A = ", resulta)

    if stepthatisrepeatedlater == None:
        if stateformemoise in memoise:
            stepthatrepeatsanearlierone = (gen, plantsum())
            stepthatisrepeatedlater = memoise[stateformemoise]
            # print("Repeated!!!! at ", gen+1)
        else:
            memoise[stateformemoise] = (gen, plantsum())

genearly, sumearly = stepthatisrepeatedlater
genlater, sumlater = stepthatrepeatsanearlierone
genforresultb = 50000000000
resultb = sumlater + (genforresultb - genlater) * (sumlater-sumearly) / (genlater-genearly)

print("Result B = ", resultb)