#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
blocks = text.split('\n\n')
resulta = 0
resultb = 0
for block in blocks:
    d = {}
    lines = block.split('\n')
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            d[(x,y)] = char
    print(d)
    H = len(lines)
    W = len(lines[0])

    def mirror_hunt(avoid_v, avoid_h):
        hunt_score = 0
        found = 0

        def is_mirror_v(vert):
            for x in range(vert):
                reflect_x = 2*vert - x - 1
                if reflect_x >= 0 and reflect_x < W:
                    for y in range(H):
                        # print(f"d[({reflect_x}, {y})] = {d[(reflect_x, y)]}, d[({x}, {y})] = {d[(x, y)]}")
                        if d[(reflect_x, y)] != d[(x,y)]:
                            return False
            return True

        def is_mirror_h(hori):
            for y in range(hori):
                reflect_y = 2*hori - y - 1
                if reflect_y >= 0 and reflect_y < H:
                    for x in range(W):
                        # print(f"d[({x}, {reflect_y})] = {d[(x, reflect_y)]}, d[({x}, {y})] = {d[(x, y)]}")
                        if d[(x, reflect_y)] != d[(x,y)]:
                            return False
            return True

        found = False
        hunt_score_v = 0
        hunt_score_h = 0
        for mirror in range(1, W):
            if is_mirror_v(mirror):
                if mirror != avoid_v:
                    found = True
                    hunt_score_v = mirror
                    break
        if not found:
            for mirror in range(1, H):
                if is_mirror_h(mirror):
                    if mirror != avoid_h:
                        found = True
                        hunt_score_h = mirror
                        break
        return (hunt_score_v, hunt_score_h)

    score_v, score_h = mirror_hunt(0,0)
    resulta += score_v + 100 * score_h

    def smudge():
        # Smudging for part b:
        for x in range(W):
            for y in range(H):
                # Do the smudge:
                presmudge = d[(x,y)] 
                d[(x,y)] = '.' if presmudge == '#' else '.'
                
                smudge_score_v, smudge_score_h = mirror_hunt(score_v, score_h)
                print(score_v, score_h, smudge_score_v, smudge_score_h)
                if smudge_score_h > 0 or smudge_score_v > 0:
                    return(smudge_score_v + 100 * smudge_score_h)

                # Unsmudge
                d[(x,y)] = presmudge
        return 0
    
    resultb += smudge()

print(resulta)
print(resultb)
