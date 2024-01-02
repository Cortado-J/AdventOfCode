# Aoc 2018 day 9
players = 465
lastmarblepart1 = 71940

for part in ['A', 'B']:
    if part == 'B':
        print("Warning - Part B currently takes a couple of hours to run.  Double linked list (deque) would make loads quicker.")
    lastmarble = lastmarblepart1 if part == 'A' else lastmarblepart1 * 1000
    marbles = lastmarble+1
    scores = [0 for _ in range(players)]
    circle = [0]
    current = 0
    player = 0

    def offset(x):
        return ( current + x + len(circle)) % len(circle)
    
    for marble in range(1, marbles):
        if marble % 23 == 0:
            scores[player] += marble
            current = offset(-7)
            scores[player] += circle[current]
            del circle[current]
            current = offset(0) # to ensure current doesn’t fall off the end!
        else:
            current = offset(2)
            circle.insert(current, marble)
        player = (player + 1) % players
        if marble % 100000 == 0:
            print(f"Progress: marble = {marble} of {marbles}")

    result= max(scores)
    print(f"Result {part} = {result}")
