import random


class HuntTarget():
    def __init__(self):
        self.potential_targets = []
        self.visited = []
        self.result = None
        self.last_guess = None
        self.possible_targets = []
        for i in range(10):
            for j in range(10):
                self.possible_targets.append([i, j])

    def turn(self):
        print(self.result, self.last_guess)
        if self.result:
            x, y = self.last_guess
            if x + 1 < 10 and [x + 1, y] in self.possible_targets:
                self.potential_targets.append([x + 1, y])
            if x - 1 > -1 and [x - 1, y] in self.possible_targets:
                self.potential_targets.append([x - 1, y])
            if y + 1 < 10 and [x, y + 1] in self.possible_targets:
                self.potential_targets.append([x, y + 1])
            if y - 1 > -1 and [x, y - 1] in self.possible_targets:
                self.potential_targets.append([x, y - 1])
            print(self.potential_targets)
        if self.potential_targets:
            cord = self.target()
        else:
            cord = self.hunt()
        self.possible_targets.remove(cord)
        self.last_guess = cord
        return cord

    def hunt(self):
        return random.choice(self.possible_targets)

    def target(self):
        return self.potential_targets.pop()
