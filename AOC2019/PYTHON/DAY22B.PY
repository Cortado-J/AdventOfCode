class SlamShuffle:
    def __init__(self, deck_size):
        self.deck_size = deck_size

    def mod_inv(self, n, mod):
        # Modular inverse using Fermat's little theorem, since mod is prime
        return pow(n, mod - 2, mod)

    def apply_deal_into_new_stack(self, a, b):
        # Reverse the entire deck: f(x) = (-a * x - 1) % deck_size
        a, b = (-a) % self.deck_size, (-b - 1) % self.deck_size
        print(f"Applied deal into new stack: a = {a}, b = {b}")
        return a, b

    def apply_cut(self, a, b, n):
        # Cut n cards: f(x) = (x - n) % deck_size
        b = (b - n) % self.deck_size  # Corrected to subtract n instead of adding
        print(f"Applied cut {n}: a = {a}, b = {b}")
        return a, b

    def apply_deal_with_increment(self, a, b, n):
        # Deal with increment n: f(x) = (n * x) % deck_size
        # This multiplies both a and b by n to correctly reflect the transformation
        a = (a * n) % self.deck_size
        b = (b * n) % self.deck_size
        print(f"Applied deal with increment {n}: a = {a}, b = {b}")
        return a, b

    def shuffle(self, instructions):
        a, b = 1, 0  # Start with identity transformation
        for instruction in instructions:
            if instruction == "deal into new stack":
                a, b = self.apply_deal_into_new_stack(a, b)
            elif instruction.startswith("cut "):
                n = int(instruction.split(" ")[1])
                a, b = self.apply_cut(a, b, n)
            elif instruction.startswith("deal with increment "):
                n = int(instruction.split(" ")[3])
                a, b = self.apply_deal_with_increment(a, b, n)
        print(f"Final linear transformation: a = {a}, b = {b}")
        return a, b

    def repeat_shuffle(self, a, b, times):
        # Use exponentiation by squaring to apply the shuffle multiple times
        a_n = pow(a, times, self.deck_size)
        if a == 1:
            # If a == 1, the transformation is purely additive, simply multiply b by times
            b_n = (b * times) % self.deck_size
        else:
            # General case: use geometric series to calculate b_n
            inv_1_minus_a = self.mod_inv((1 - a) % self.deck_size, self.deck_size)
            b_n = (b * (1 - a_n) * inv_1_minus_a) % self.deck_size
        return a_n, b_n

    def find_card_at_position(self, position, a, b, times):
        # Apply the shuffle transformation `times` times in reverse to find which card ends up at the given position
        a_n, b_n = self.repeat_shuffle(a, b, times)
        # To find the card at a specific position, we need to invert the transformation
        inv_a_n = self.mod_inv(a_n, self.deck_size)
        return (position * inv_a_n + (-b_n * inv_a_n) % self.deck_size) % self.deck_size

# Example usage for part 2

# Updated requirements for Part 2
large_deck_size = 119315717514047
repeated_shuffles = 101741582076661
position_to_find = 2020

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

slam_shuffle = SlamShuffle(large_deck_size)

# Compute the linear transformation for the shuffle
a, b = slam_shuffle.shuffle(instructions)

# Apply the repeated shuffles
a_n, b_n = slam_shuffle.repeat_shuffle(a, b, repeated_shuffles)

# Find the card at the given position after all the shuffles
card_at_position = slam_shuffle.find_card_at_position(position_to_find, a_n, b_n, 1)

print(f"Card at position {position_to_find} after {repeated_shuffles} shuffles: {card_at_position}")
