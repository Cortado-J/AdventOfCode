from collections import Counter
#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
lines = text.split('\n')

#  Part A
cards = {'A':14, 'K':13, 'Q':12, 'J':11, 'T':10, '9':9, '8':8, '7':7, '6':6, '5':5, '4':4, '3':3, '2':2}

def hand_strength(hand):
    counter = Counter(hand)
    result = sorted(list(counter.values()), reverse = True)
    while len(result) < 5:
        result.append(0)
    return result

def card_strength(hand):
    cards_signature = [cards[card] for card in hand]
    return cards_signature

gather = []
for line in lines:
    pair = line.split(" ")
    hand = pair[0]
    score = int(pair[1])
    strength = hand_strength(hand) + card_strength(hand) 
    gather.append((hand, score, strength))

sorted_hands = sorted(gather, key=lambda x: x[2])

score = 0
for index, sh in enumerate(sorted_hands):
    score += (index+1) * sh[1]

resulta = score
print(resulta)

#  Part B
cards = {'A':14, 'K':13, 'Q':12, 'T':10, '9':9, '8':8, '7':7, '6':6, '5':5, '4':4, '3':3, '2':2, 'J':1}

def strongest(original, hands):
    hands = [(hand, hand_strength(hand) + card_strength(original)) for hand in hands]
    hands = sorted(hands, key=lambda x: x[1])
    strongest_hand = hands[-1][0]
    return strongest_hand

# Recursive replacement of jokers:  Annoyingly we have to keep th original and pass it on.
def best(original, hand):
    joker_index = hand.find("J")
    if joker_index == -1:
        return hand
    if original == "JJJJJ":
        return "AAAAA"
    nonjokers = set([ch for ch in hand if ch != 'J'])
    candidates = []
    for replace_char in nonjokers:
        hand_copy = hand[:joker_index] + replace_char + hand[joker_index + 1:]
        candidate = best(original, hand_copy)
        candidates.append(candidate)
    return strongest(original, candidates)

gather = []
for line in lines:
    pair = line.split(" ")
    hand = pair[0]
    score = int(pair[1])
    if hand == "JJJJJ":
        a = 1
        a += 1
    bestie = best(hand, hand)
    gather.append((bestie, score, hand_strength(bestie) + card_strength(hand)))

# print(gather)

sorted_hands = sorted(gather, key=lambda x: x[2])

score = 0
for index, sh in enumerate(sorted_hands):
    score += (index+1) * sh[1]

resultb = score
print(resultb)
