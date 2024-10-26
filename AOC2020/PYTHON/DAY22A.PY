from collections import deque

def play_combat(player1_deck, player2_deck):
    # Initialize decks as deque for efficient popping and appending
    player1 = deque(player1_deck)
    player2 = deque(player2_deck)
    
    # Play rounds until one player has all the cards
    while player1 and player2:
        card1 = player1.popleft()
        card2 = player2.popleft()
        
        if card1 > card2:
            player1.append(card1)
            player1.append(card2)
        else:
            player2.append(card2)
            player2.append(card1)
    
    # Determine winner and calculate score
    winner = player1 if player1 else player2
    score = sum((i + 1) * card for i, card in enumerate(reversed(winner)))
    
    return score

# Example input
player1_deck = [7,
1,
9,
10,
12,
4,
38,
22,
18,
3,
27,
31,
43,
33,
47,
42,
21,
24,
50,
39,
8,
6,
16,
46,
11]

player2_deck = [49,
41,
40,
35,
44,
29,
30,
19,
14,
2,
34,
17,
25,
5,
15,
32,
20,
48,
45,
26,
37,
28,
36,
23,
13]

# Play the game and print the winning player's score
winning_score = play_combat(player1_deck, player2_deck)
print(f"The winning player's score is: {winning_score}")
