import random


class HuntTarget():
    def __init__(self, ships):
        self.potential_targets = []
        self.visited = []
        self.result = None
        self.last_guess = None
        self.possible_targets = []
        self.parity_grid = []
        self.ships = ships
        for i in range(10):
            for j in range(10):
                self.possible_targets.append([i, j])
        for i in range(10):
            if i % 2 == 0:
                for j in range(1, 10, 2):
                    self.parity_grid.append([i, j])
            else:
                for j in range(0, 10, 2):
                    self.parity_grid.append([i, j])

    def turn(self):
        print(self.result, self.last_guess)
        if self.result:
            if not isinstance(self.result, bool):
                self.ships.remove(self.result[1])
            x, y = self.last_guess
            if x + 1 < 10 and [x + 1, y] in self.possible_targets and [x + 1, y] not in self.potential_targets:
                self.potential_targets.append([x + 1, y])
            if x - 1 > -1 and [x - 1, y] in self.possible_targets and [x - 1, y] not in self.potential_targets:
                self.potential_targets.append([x - 1, y])
            if y + 1 < 10 and [x, y + 1] in self.possible_targets and [x, y + 1] not in self.potential_targets:
                self.potential_targets.append([x, y + 1])
            if y - 1 > -1 and [x, y - 1] in self.possible_targets and [x, y - 1] not in self.potential_targets:
                self.potential_targets.append([x, y - 1])
            print(self.potential_targets)
        while True:
            if self.potential_targets:
                cord = self.target()
            else:
                cord = self.hunt()
            if self.parity(cord):
                break
        try:
            self.possible_targets.remove(cord)
        except ValueError:
            print(cord, "NOT IN LIST??")
        self.last_guess = cord
        return cord

    def hunt(self):
        cord = random.choice(self.parity_grid)
        self.parity_grid.remove(cord)
        return cord
        #return random.choice(self.possible_targets)

    def target(self):
        return self.potential_targets.pop()

    def parity(self, cord):
        # x, y = cord
        # north = [x, y-1]
        # east = [x+1, y]
        # south = [x, y+1]
        # west = [x-1, y]
        #
        # if north not in self.possible_targets and east not in self.possible_targets and south not in self.possible_targets and west not in self.possible_targets:
        #     return False
        return True


