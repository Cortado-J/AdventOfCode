from collections import deque

def play_recursive_combat(player1_deck, player2_deck):
    # Initialize decks as deque for efficient popping and appending
    player1 = deque(player1_deck)
    player2 = deque(player2_deck)
    
    # Set to store previous rounds and prevent infinite loops
    previous_rounds = set()

    # Play rounds until one player has all the cards
    while player1 and player2:
        # Check if the current state has been seen before
        current_state = (tuple(player1), tuple(player2))
        if current_state in previous_rounds:
            return 1, player1  # Player 1 wins the game to avoid infinite loop
        previous_rounds.add(current_state)
        
        # Draw the top cards
        card1 = player1.popleft()
        card2 = player2.popleft()
        
        # Determine the winner of the round
        if len(player1) >= card1 and len(player2) >= card2:
            # Recurse with copies of the next cards
            sub_winner, _ = play_recursive_combat(list(player1)[:card1], list(player2)[:card2])
            if sub_winner == 1:
                player1.append(card1)
                player1.append(card2)
            else:
                player2.append(card2)
                player2.append(card1)
        else:
            if card1 > card2:
                player1.append(card1)
                player1.append(card2)
            else:
                player2.append(card2)
                player2.append(card1)
    
    # Determine winner and calculate score
    if player1:
        return 1, player1
    else:
        return 2, player2

def calculate_score(winning_deck):
    return sum((i + 1) * card for i, card in enumerate(reversed(winning_deck)))

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
_, winning_deck = play_recursive_combat(player1_deck, player2_deck)
winning_score = calculate_score(winning_deck)
print(f"The winning player's score is: {winning_score}")
