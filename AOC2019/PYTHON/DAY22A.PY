class SlamShuffle:
    def __init__(self, deck_size):
        self.deck_size = deck_size
        self.deck = list(range(deck_size))

    def deal_into_new_stack(self):
        self.deck.reverse()

    def cut(self, n):
        self.deck = self.deck[n:] + self.deck[:n]

    def deal_with_increment(self, n):
        new_deck = [None] * self.deck_size
        position = 0
        for card in self.deck:
            new_deck[position] = card
            position = (position + n) % self.deck_size
        self.deck = new_deck

    def shuffle(self, instructions):
        for instruction in instructions:
            if instruction == "deal into new stack":
                self.deal_into_new_stack()
            elif instruction.startswith("cut "):
                n = int(instruction.split(" ")[1])
                self.cut(n)
            elif instruction.startswith("deal with increment "):
                n = int(instruction.split(" ")[3])
                self.deal_with_increment(n)

    def find_position_of_card(self, card_value):
        return self.deck.index(card_value)

    def get_deck(self):
        return self.deck

# Example usage
# Test cases provided

test_cases = [
    (
        ["deal with increment 7", "deal into new stack", "deal into new stack"],
        [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
    ),
    (
        ["cut 6", "deal with increment 7", "deal into new stack"],
        [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
    ),
    (
        ["deal with increment 7", "deal with increment 9", "cut -2"],
        [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]
    ),
    (
        [
            "deal into new stack", "cut -2", "deal with increment 7", "cut 8", "cut -4", 
            "deal with increment 7", "cut 3", "deal with increment 9", "deal with increment 3", "cut -1"
        ],
        [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]
    )
]

# Run test cases
deck_size = 10
for i, (instructions, expected_result) in enumerate(test_cases):
    slam_shuffle = SlamShuffle(deck_size)
    slam_shuffle.shuffle(instructions)
    result = slam_shuffle.get_deck()
    assert result == expected_result, f"Test case {i+1} failed: expected {expected_result}, got {result}"
    print(f"Test case {i+1} passed: {result}")

# Example usage for large deck
deck_size = 10007
slam_shuffle = SlamShuffle(deck_size)

instructions = """
cut -1468
deal with increment 19
cut -7127
deal with increment 8
cut -8697
deal with increment 58
cut 4769
deal into new stack
cut 4921
deal with increment 16
cut -1538
deal with increment 55
cut 3387
deal with increment 41
cut 4127
deal with increment 26
cut 5512
deal with increment 21
deal into new stack
deal with increment 44
cut -7989
deal with increment 28
cut 569
deal into new stack
cut -9795
deal into new stack
cut -6877
deal with increment 60
cut -6500
deal with increment 37
cut -9849
deal with increment 66
cut -4821
deal with increment 50
deal into new stack
cut 9645
deal with increment 22
cut -6430
deal with increment 17
cut 658
deal with increment 67
cut -9951
deal into new stack
deal with increment 31
cut -2423
deal with increment 39
cut -5126
deal with increment 7
cut 432
deal with increment 8
cut 682
deal with increment 45
deal into new stack
deal with increment 41
cut -130
deal with increment 74
deal into new stack
cut -9207
deal into new stack
cut 7434
deal with increment 31
cut -5165
deal into new stack
cut 6209
deal with increment 25
cut 2734
deal with increment 53
deal into new stack
cut -1528
deal with increment 25
deal into new stack
deal with increment 68
cut 6458
deal into new stack
cut 1895
deal with increment 16
cut -6137
deal with increment 53
cut 2761
deal with increment 73
deal into new stack
cut 1217
deal with increment 69
deal into new stack
deal with increment 54
cut -6639
deal into new stack
cut -2891
deal with increment 10
cut -6297
deal with increment 31
cut 4591
deal with increment 35
cut -4035
deal with increment 65
cut -7504
deal into new stack
deal with increment 54
deal into new stack
cut 1313
""".splitlines()

slam_shuffle.shuffle(instructions)
position = slam_shuffle.find_position_of_card(2019)
print(f"Position of card 2019: {position}")
