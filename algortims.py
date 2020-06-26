import random


class Algorithm:
    def __init__(self, ships: list):
        """
        Initiator for Algorithm.

        :param ships: List
        """
        self.possible_targets = []
        self.last_guess = None
        self.potential_targets = []
        self.result = False, 0
        self.ships = ships
        for i in range(10):
            for j in range(10):
                self.possible_targets.append([i, j])

    def get_surrounding(self, cord: list) -> list:
        """
        Returns the 4 surrounding coordinates of a coordinate.

        :param cord: List
        """
        surrounding = []
        x, y = cord
        # north
        north = [x, y - 1]
        if north not in surrounding and north in self.possible_targets:
            surrounding.append(north)
        else:
            surrounding.append([0])
        # east
        east = [x + 1, y]
        if east not in surrounding and east in self.possible_targets:
            surrounding.append(east)
        else:
            surrounding.append([0])
        # south
        south = [x, y + 1]
        if south not in surrounding and south in self.possible_targets:
            surrounding.append(south)
        else:
            surrounding.append([0])
        # west
        west = [x - 1, y]
        if west not in surrounding and west in self.possible_targets:
            surrounding.append(west)
        else:
            surrounding.append([0])

        return surrounding

    def turn(self):
        pass


class HuntTarget(Algorithm):
    def turn(self) -> list:
        """
        Returns the coordinate where the AI will shoot.

        :return: List
        """
        if self.result[0]:
            self.potential_targets.extend(self.check_surrounding(self.last_guess))
        if self.potential_targets:
            cord = self.target()
        else:
            cord = self.hunt()
        self.last_guess = cord
        self.possible_targets.remove(cord)
        return cord

    def hunt(self) -> list:
        """
        Returns a random coordinate from all coordinates that are still possible.

        :return: List
        """
        return random.choice(self.possible_targets)

    def target(self) -> list:
        """
        Returns a coordinate from the potential targets

        :return: List
        """
        while True:
            if len(self.potential_targets) > 0:
                cord = self.potential_targets.pop()
                if cord in self.possible_targets:
                    return cord
            else:
                cord = random.choice(self.possible_targets)
                return cord

    def check_surrounding(self, cord: list) -> list:
        """
        Returns the checked surrounding coordinates.

        :param cord: List
        :return: List
        """
        surroundings = self.get_surrounding(cord)
        for cord in surroundings:
            if cord in self.potential_targets or cord == [0]:
                surroundings.remove(cord)
        return surroundings


class HuntTargetParity(Algorithm):
    def __init__(self, ships: list):
        """
        Initiator for HuntTargetParity
        """
        super().__init__(ships)
        self.parity_grid = []
        self.smallest_ship = min(self.ships)
        for i in range(10):
            if i % 2 == 0:
                for j in range(1, 10, 2):
                    self.parity_grid.append([i, j])
            else:
                for j in range(0, 10, 2):
                    self.parity_grid.append([i, j])

    def turn(self) -> list:
        """
        Returns the coordinate where the AI will shoot.

        :return: List
        """

        if self.result[0]:
            self.potential_targets.extend(self.check_surrounding(self.last_guess))
            if self.result[1] in self.ships:
                self.ships.remove(self.result[1])
        if self.potential_targets:
            cord = self.target()
        else:
            if self.smallest_ship < min(self.ships):
                self.smallest_ship = min(self.ships)
                self.parity()
            cord = self.hunt()
        self.possible_targets.remove(cord)
        self.last_guess = cord
        return cord

    def hunt(self) -> list:
        """
        Returns a coordinate taking parity into account.

        :return: List
        """
        if self.parity_grid:
            cord = random.choice(self.parity_grid)
            self.parity_grid.remove(cord)
            while cord not in self.possible_targets:
                cord = random.choice(self.parity_grid)
                self.parity_grid.remove(cord)
        else:
            cord = random.choice(self.possible_targets)
        return cord

    def target(self) -> list:
        """
        Returns a potential coordinate.

        :return: List
        """
        while True:
            if len(self.potential_targets) > 0:
                cord = self.potential_targets.pop()
                if cord in self.possible_targets:
                    return cord
            else:
                cord = self.hunt()
                return cord

    def check_surrounding(self, cord: list) -> list:
        """
        Returns the checked surrounding coordinates.

        :param cord: List
        :return: List
        """
        surroundings = self.get_surrounding(cord)
        for cord in surroundings:
            if cord in self.potential_targets or cord == [0] or cord not in self.possible_targets:
                surroundings.remove(cord)
        return surroundings

    def parity(self):
        """
        Checks where the smallest ship doesn't fit and removes those coordinates from the list with possible
        coordinates.
        """
        elimination = []

        smallest_ship = min(self.ships)

        for i in self.possible_targets:
            # Horizontal
            horizontal = 0
            checking_cord = i
            while self.get_surrounding(checking_cord)[1] in self.possible_targets:
                horizontal += 1
                checking_cord = self.get_surrounding(checking_cord)[1]
            checking_cord = i
            while self.get_surrounding(checking_cord)[3] in self.possible_targets:
                horizontal += 1
                checking_cord = self.get_surrounding(checking_cord)[3]
            # Vertical
            vertical = 0
            checking_cord = i
            while self.get_surrounding(checking_cord)[0] in self.possible_targets:
                vertical += 1
                checking_cord = self.get_surrounding(checking_cord)[0]
            checking_cord = i
            while self.get_surrounding(checking_cord)[2] in self.possible_targets:
                vertical += 1
                checking_cord = self.get_surrounding(checking_cord)[2]

            if vertical < smallest_ship - 1 and horizontal < smallest_ship - 1:
                elimination.append(i)
        for i in elimination:
            self.parity_grid.clear()
            if i in self.possible_targets:
                self.possible_targets.remove(i)


class ProbabilityDensity(Algorithm):
    def __init__(self, ships):
        """
        Initiator for ProbabilityDensity.

        :param ships: List
        """
        super().__init__(ships)
        self.hit_streak = []

    def turn(self) -> list:
        """
        Returns where the AI wants to shoot.

        :return: List
        """
        if self.result[0]:
            self.hit_streak.append(self.last_guess)
            if self.result[1] > 0:
                self.ships.remove(self.result[1])
                if self.result[1] == len(self.hit_streak):
                    self.hit_streak.clear()
        if self.hit_streak:
            probabilities = self.probability(True)
        else:
            probabilities = self.probability(False)
        cord = list(probabilities.pop())
        self.possible_targets.remove(cord)
        self.last_guess = cord
        return cord

    def probability(self, hit: bool) -> list:
        """
        Returns a list sorted based on where a ship most likely is.

        :param hit: Boolean
        :return: List
        """
        probability_tracker = {}

        probable_targets = self.possible_targets + self.hit_streak

        for ship in self.ships:
            for tile in probable_targets:
                # Horizontal
                x, y = tile
                horizontal_tile_tracker = {}
                vertical_tile_tracker = {}

                for i in range(ship):
                    if [x + i, y] in probable_targets:
                        if tuple([x + i, y]) not in horizontal_tile_tracker:
                            horizontal_tile_tracker[tuple([x + i, y])] = 0
                        horizontal_tile_tracker[tuple([x + i, y])] += 1
                    else:
                        horizontal_tile_tracker.clear()
                    if [x, y + i] in probable_targets:
                        if tuple([x, y + i]) not in vertical_tile_tracker:
                            vertical_tile_tracker[tuple([x, y + i])] = 0
                        vertical_tile_tracker[tuple([x, y + i])] += 1
                    else:
                        vertical_tile_tracker.clear()

                for i in horizontal_tile_tracker.keys():
                    if i not in probability_tracker:
                        probability_tracker[i] = 0
                    probability_tracker[i] += horizontal_tile_tracker[i]
                for i in vertical_tile_tracker.keys():
                    if i not in probability_tracker:
                        probability_tracker[i] = 0
                    probability_tracker[i] += vertical_tile_tracker[i]

        surrounding = []

        for hit in self.hit_streak:
            for cord in self.get_surrounding(hit):
                if cord not in self.hit_streak and cord not in surrounding and cord != [0]:
                    surrounding.append(cord)

        if hit and self.hit_streak:
            hit_probability_tracker = probability_tracker
            probability_tracker = {}
            for i in hit_probability_tracker:
                if list(i) not in self.hit_streak and list(i) in surrounding:
                    probability_tracker[i] = hit_probability_tracker[i]

        sorted_tracker = {k: v for k, v in sorted(probability_tracker.items(), key=lambda item: item[1])}
        probability_tracker_list = [*sorted_tracker]
        if len(probability_tracker_list) > 0:
            return probability_tracker_list
        else:
            return [random.choice(self.possible_targets)]


class Random(Algorithm):
    def turn(self) -> list:
        """
        Returns a random coordinate on the board.

        :return: List
        """
        cord = random.choice(self.possible_targets)
        self.possible_targets.remove(cord)
        return cord
