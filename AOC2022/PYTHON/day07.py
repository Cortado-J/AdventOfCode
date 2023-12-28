#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
input = text.splitlines()
input.append("$ cd /")  # To ensure end for ls

class Dir:
    def __init__(self, dirname, parent=None):
        self.name = dirname
        self.filenames = list()
        self.filesizes = list()
        self.children = list()  # Array of Dirs
        self.parent = parent  # Parent

    def __repr__(self):
        result = self.name + '['
        for file in range(0, len(self.filenames)):
            result += self.filenames[file] + ' '
        if len(self.children) > 0:
            for child in self.children:
                result += child.__repr__()
        result += '] '
        return result

    def childrenNames(self):
        return [ch.name for ch in self.children]

    def size(self):
        result = 0
        for s in self.filesizes:
            result += s
        for c in self.children:
            result += c.size()
        return result

    def dirlist(self):
        dirs = [self]
        for c in self.children:
            for d in c.dirlist():
                dirs.append(d)
        return dirs


root = Dir("root")
current = root
# print(root)

next = 0
while next < len(input):
    line = input[next].split()
    next += 1
    if line[0] == '$':
        if line[1] == 'cd':
            dir = line[2]
            if dir == '/':
                current = root
            elif dir == '..':
                current = current.parent
            else:
                if not dir in current.childrenNames():
                    current.children.append(Dir(dir, current))
                for hunt in current.children:
                    if hunt.name == dir:
                        current = hunt
                        break
        else:  # Must be ls
            while input[next][0] != '$':
                line = input[next].split()
                next += 1
                if line[0] == 'dir':
                    if not line[1] in current.childrenNames():
                        current.children.append(Dir(line[1], current))
                else:
                    if line[1] not in current.filenames:
                        current.filenames.append(line[1])
                        current.filesizes.append(int(line[0]))

# print(root)
# print('-------')
parta = 0
for d in root.dirlist():
    s = d.size()

    # print(d, d.size())
    if s < 100000:
        parta += s
print(f"Day {daytext}: Part A = {parta}")

outersize = root.size()
disksize = 70000000
currentspace = disksize - outersize
needspace = 30000000
needtofree = needspace - currentspace

best = disksize
for d in root.dirlist():
    s = d.size()
    if s < best and s >= needtofree:
        best = s
partb = best

print(f"Day {daytext}: Part B = {partb}")
