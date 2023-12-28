#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
inp = text.split('\n\n')

class Monkey:
    def __init__(self, lines):
        lines = lines.splitlines()
        # Monkey 0:
        # Starting items: 57, 58
        self.items = [int(x.replace(',', '')) for x in lines[1].split(' ')[4:]]

        # Operation: new = old * 19
        fact = lines[2].split(' ')[-1]
        op   = lines[2].split(' ')[-2]
        if fact == 'old':
            fact = '2'
            op   = 'pow'
        self.factor = int(fact)
        self.op = op

        # Test: divisible by 7
        self.div = int(lines[3].split(' ')[-1])

        #   If true: throw to monkey 2
        self.acttrue = int(lines[4].split(' ')[-1])

        #   If false: throw to monkey 3
        self.actfals = int(lines[5].split(' ')[-1])

        self.inspections = 0

    # inspect all items and return instructions for where the items should be distributed to other monkeys
    # as an array of tuples where each tuple is (destinationMonkey, worry)
    def inspect(self, modulus, divby3):
        result = []
        for worry in self.items:
            self.inspections += 1
            worry = self.operate(worry, self.op, self.factor) % modulus
            if divby3:
                worry = worry // 3
            dest = self.acttrue if worry % self.div == 0 else self.actfals
            # print(f"Monkey {m} throws item with worry {worry} to monkey {dest}")
            send = (dest, worry)
            result.append(send)
        self.items = []  # Clear the items from this monkey because they are being redistributed
        return result


    def operate(self, x, op, fact):
        if op == '+':
            return x + fact
        if op == '*':
            return x * fact
        if op == 'pow':
            return x * x
        return -7777777


class Part:
    def __init__(self, divby3):
        self.divby3 = divby3
        self.monkeys = []
        self.modulus = 1
        for monkeyString in inp:
            monk = Monkey(monkeyString)
            self.monkeys.append(monk)
            self.modulus *= monk.div


    def round(self):
        for monk in range(len(self.monkeys)):
            sends = self.monkeys[monk].inspect(self.modulus, self.divby3)
            for send in sends:
                # Distribute the inspected items to other monkeys
                self.monkeys[send[0]].items.append(send[1])

    def run(self, rounds):
        for monkey in self.monkeys:
            monkey.inspections = 0
        for r in range(rounds):
            self.round()
        inspections = [monkey.inspections for monkey in self.monkeys]
        print(inspections)
        biggest = sorted(inspections, reverse=True)
        return biggest[0] * biggest[1]


parta = Part(True).run(20)
print(f"Day {daytext}: Part A = {parta}")

partb = Part(False).run(10000)
print(f"Day {daytext}: Part B = {partb}")
