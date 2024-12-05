#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
from collections import defaultdict
from functools import cmp_to_key

sections = text.split('\n\n')
rules_text = sections[0].split('\n')
updates_text = sections[1].split('\n')

updates = [[int(page) for page in update.split(',')] for update in updates_text]

rules = defaultdict(set)
for rule in rules_text:
    page1 = int(rule[0:2])
    page2 = int(rule[3:5])
    rules[page1].add(page2)

parta, partb = 0, 0

def is_ordered(pages):
    for index, page1 in enumerate(pages[:-1]):
        page2 = pages[index+1]
        if page1 in rules[page2]:
            return False
    return True

def middle(update):
    return update[int((len(update)-1)/2)]


def page_sort(x, y):
    if x in rules[y]:
        return 1
    if y in rules[x]:
        return -1
    return 0

unordered = []
for update in updates:
    if is_ordered(update):
        parta += middle(update)
    else:
        pages = sorted(update, key=cmp_to_key(page_sort))
        partb += middle(pages)

print("Part A:", parta)
print("Part B:", partb)
