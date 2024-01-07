#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.splitlines()

recipes = None
elves = None

def reset():
    global recipes
    global elves
    recipes = [3,7]
    elves = [0,1]

def show():
    for pos, x in enumerate(recipes):
        ends = "  "
        if pos == elves[0]:
            ends = '()'
        elif pos == elves[1]:
            ends = '[]'
        print(f"{ends[0]}{x}{ends[1]}", end='')
    print()

# show()
def bake():    
    score0 = recipes[elves[0]]
    score1 = recipes[elves[1]]
    recipesum = score0 + score1 
    if recipesum > 9:
        recipes.append(recipesum // 10)
    recipes.append(recipesum % 10)
    elves[0] = (elves[0] + score0 + 1) % len(recipes)
    elves[1] = (elves[1] + score1 + 1) % len(recipes)

def run(n):
    reset()
    startrecipe = n
    endrecipe = n+10-1
    while len(recipes) <= endrecipe:
        bake()
    return ''.join([str(ch) for ch in recipes[startrecipe:endrecipe+1]])

def search(n):
    reset()
    term = str(n)
    length = len(term)
    # count = 0
    while True:
        bake()
        if len(recipes) > length:
            last = ''.join([str(ch) for ch in recipes[-length:]])
            if last == term:
                # print("End is ",recipes[-(length+3):])
                # print("Chosen ",recipes[-length:])
                return len(recipes) - length
            penultimate = ''.join([str(ch) for ch in recipes[-length-1:-1]])
            if penultimate == term:
                # print("End is ",recipes[-(length+3):])
                # print("Chosen ",recipes[-length-1:-1])
                return len(recipes) - length - 1
        # count += 1
        # if count % 100000 == 0:
        #     print(count)

input = 909441
resulta = run(input)
print("Result A = ", resulta)

resultb = search(input)
print("Result B = ", resultb)
