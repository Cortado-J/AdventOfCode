#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')
maxes = {"red":12, "green":13, "blue":14}
resulta = 0
resultb = 0
for game in lines:
    print(game)
    id = int(game.split(":")[0][5:])
    game_ok = True
    min_red = 0
    min_blue = 0
    min_green = 0
    draws = game.strip().split(":")[1].strip().split(";")
    print(id, draws)
    for draw in draws:
        print("draw=", draw)
        for colour_draw in draw.split(","):
            print("  colour_draw=", colour_draw)
            number = int(colour_draw.strip().split(" ")[0])
            colour = colour_draw.strip().split(" ")[1]
            if number > maxes[colour]:
                game_ok = False
            if colour == "red":
                min_red = max(min_red, number)
            if colour == "green":
                min_green = max(min_green, number)
            if colour == "blue":
                min_blue = max(min_blue, number)
    if game_ok:
        resulta += id
    power = min_red * min_green * min_blue
    resultb += power
print(resulta)
print(resultb)

