#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
grid = {}
ylen = len(lines)
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        grid[(x,y)] = (int(char) if char != '.' else -1)
    xlen = len(line)

def get_trails(pos, level):
    result = []
    if level == 9:
        result.append((pos))
        return result
    for next in [(pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0], pos[1]-1)]:
        if next in grid:
            if grid[next] == level+1:
                result += get_trails(next, level+1)
    return result

parta, partb = 0, 0
for pos, val in grid.items():
    if val == 0:
        trails = get_trails(pos, 0)
        unique = set(trails)
        parta += len(unique)
        partb += len(trails)

print("Part A:", parta)
print("Part B:", partb)
