import math
# For A:
# race: (time, distance)
races = [(45,295), (98,1734), (83, 1278), (73, 1210)]
# Test data:
# races = [(7,9), (15,40), (30, 200)]

def distance(race, press_time):
    return (race[0]-press_time)*press_time

def beats(race):
    return sum([ (1 if distance(race, pt) > race[1] else 0) for pt in range(race[0])])

resulta = math.prod([beats(race) for race in races])
print("result a=", resulta)

#  For B:
time = 45988373
record = 295173412781210
# Test data:
# time = 71530
# record = 940200

#  Solving quadratic:
part1 = time/2
part2 = 0.5 * math.sqrt(time * time - 4 * record)
larger_answer = math.floor(part1 + part2) # Floor
smaller_answer = math.floor(part1 - part2) + 1 # Ceiling
# print("time=",time)
# print("record=",record)
# print("part1=",part1)
# print("part2=",part2)
# print("larger_answer=",larger_answer)
# print("smaller_answer=",smaller_answer)
print("result b=", larger_answer - smaller_answer + 1) # The "+1" is because we need to include the first and the last one (like counting fence posts) 


