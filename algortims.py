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
        # ADD [0] FOR NOT IN!
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


class OldHuntTarget:
    def __init__(self, ships):
        self.potential_targets = []
        self.visited = []
        self.result = None
        self.last_guess = None
        self.possible_targets = []
        self.parity_grid = []
        self.data = {}
        self.ships = ships
        for i in range(10):
            for j in range(10):
                self.possible_targets.append([i, j])
                self.data[f"{i};{j}"] = "tile"
        for i in range(10):
            if i % 2 == 0:
                for j in range(1, 10, 2):
                    self.parity_grid.append([i, j])
            else:
                for j in range(0, 10, 2):
                    self.parity_grid.append([i, j])

    def turn(self):
        # print(self.result, self.last_guess)

        if self.result is not None:
            if self.result:
                self.data[f"{self.last_guess[0]};{self.last_guess[1]}"] = "hit"
            else:
                self.data[f"{self.last_guess[0]};{self.last_guess[1]}"] = "miss"

        self.parity(self.data)
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
            # print(self.potential_targets)
        # while True:
        if self.potential_targets:
            cord = self.target()
        else:
            cord = self.hunt()
            # if self.parity(cord):
            #     break
        if cord in self.parity_grid:
            self.parity_grid.remove(cord)
        try:
            self.possible_targets.remove(cord)
        except ValueError:
            # WORDT NOG STEEDS IN POTENTIAL TARGETS GEZET!
            print(cord, "NOT IN LIST??")
        self.last_guess = cord
        return cord

    def hunt(self):
        # while True:
        #     cord = random.choice(self.parity_grid)
        #     if cord not in self.possible_targets:
        #         self.parity_grid.remove(cord)
        #     else:
        #         break
        cord = random.choice(self.possible_targets)
        return cord
        # return random.choice(self.possible_targets)

    def target(self):
        for i in self.potential_targets:
            if i not in self.possible_targets:
                self.potential_targets.remove(i)
        if self.potential_targets:
            return self.potential_targets.pop()
        else:
            return self.hunt()

    def parity(self, data):
        parity_data = {}
        posi = []
        maybeposi = []
        notposi = []
        smallest_ship = min(self.ships)
        for i in data:
            if data[i] == "tile":
                cord = [int(i.split(";")[0]), int(i.split(";")[1])]
                north, east, south, west = self.check_directions(cord, data)

                parity_data[i] = {}
                parity_data[i]["north"] = north
                parity_data[i]["east"] = east
                parity_data[i]["south"] = south
                parity_data[i]["west"] = west

        #         if north < smallest_ship and east < smallest_ship and south < smallest_ship and west < smallest_ship:
        #             maybeposi.append(cord)
        #         else:
        #             posi.append(cord)
        #         for j in maybeposi:
        #             if j not in posi and j not in notposi:
        #                 notposi.append(j)
        # print("NOT POSI", notposi)

        for i in parity_data:
            smaller = 0
            if parity_data[i]["north"] + parity_data[i]["south"] + 1 < smallest_ship and parity_data[i]["east"] + \
                    parity_data[i]["west"] + 1 < smallest_ship:

                x = int(i.split(";")[0])
                y = int(i.split(";")[1])
                if [x, y] in self.possible_targets:
                    # print("REMOVING:", i, parity_data[i])
                    self.possible_targets.remove([x, y])
            # for j in parity_data[i]:
            #     if parity_data[i][j]+1 < smallest_ship:
            #         smaller += 1
            # if smaller == 4:
            #     print("REMOVING:", i, parity_data[i])

        # print(parity_data)

        # CHECK VOOR TILES NIET HIT OR MISS ZIJN
        # if data[i] == "tile":
        #     cord = i.split(";")
        #     smaller_directions = 0
        #     north, east, south, west = self.check_directions(cord, data)
        #     # print(north, east, south, west)
        #     smallest_ship = min(self.ships)
        #     x = int(cord[0])
        #     y = int(cord[1])
        #     # SHOULD BE north + south
        #     # NEE GRAPJE HET HAD ALLEEN +1 MOETEN ZIJN!!
        #     if north + south + 1 < smallest_ship:
        #         if [x, y - 1] in self.possible_targets and [x, y + 1] in self.possible_targets:
        #             for j in range(1, north):
        #                 print("REMOVING", [x, y - j])
        #                 self.possible_targets.remove([x, y - j])
        #             for j in range(1, south):
        #                 print("REMOVING", [x, y+j])
        #                 self.possible_targets.remove([x, y+j])
        #             smaller_directions += 1
        #
        #     if east + west + 1 < smallest_ship:
        #         if [x + 1, y] in self.possible_targets and [x - 1, y] in self.possible_targets:
        #             for j in range(1, east):
        #                 print("REMOVING", [x+j, y])
        #                 self.possible_targets.remove([x+j, y])
        #             for j in range(1, west):
        #                 print("REMOVING", [x - j, y])
        #                 self.possible_targets.remove([x - j, y])
        #             smaller_directions += 1

        # if north+1 < smallest_ship:
        #     if [x, y-1] in self.possible_targets:
        #         for j in range(1, north):
        #             print("REMOVING NORTH", [x, y-j])
        #             self.possible_targets.remove([x, y-j])
        #         smaller_directions += 1
        # if east+1 < smallest_ship:
        #     if [x+1, y] in self.possible_targets:
        #         for j in range(1, east):
        #             print("REMOVING EAST", [x+j, y])
        #             self.possible_targets.remove([x+j, y])
        #         smaller_directions += 1
        # if south+1 < smallest_ship:
        #     if [x, y+1] in self.possible_targets:
        #         for j in range(1, south):
        #             print("REMOVING SOUTH", [x, y+j])
        #             self.possible_targets.remove([x, y+j])
        #         smaller_directions += 1
        # if west+1 < smallest_ship:
        #     if [x-1, y] in self.possible_targets:
        #         for j in range(1, west):
        #             print("REMOVING WEST", [x-j, y])
        #             self.possible_targets.remove([x-j, y])
        #         smaller_directions += 1
        # if smaller_directions == 4:
        #     print("REMOVING", [x, y])
        #     if [x, y] in self.possible_targets:
        #         self.possible_targets.remove([x, y])

    def check_directions(self, cord, data):
        north = 0
        east = 0
        south = 0
        west = 0

        x, y = cord

        while f"{x};{y - (north + 1)}" in data and (
                data[f"{x};{y - (north + 1)}"] == "tile" or data[f"{x};{y - (north + 1)}"] == "hit"):
            north += 1

        while f"{x + (east + 1)};{y}" in data and (
                data[f"{x + (east + 1)};{y}"] == "tile" or data[f"{x + (east + 1)};{y}"] == "hit"):
            east += 1

        while f"{x};{y + (south + 1)}" in data and (
                data[f"{x};{y + (south + 1)}"] == "tile" or data[f"{x};{y + (south + 1)}"] == "hit"):
            south += 1

        while f"{x - (west + 1)};{y}" in data and (
                data[f"{x - (west + 1)};{y}"] == "tile" or data[f"{x - (west + 1)};{y}"] == "hit"):
            west += 1

        return north, east, south, west


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
        try:
            self.possible_targets.remove(cord)
        except:
            print("break")
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
    # SELECTEERD SOMS OUT OF BOUNDS CORDS
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
        try:
            self.possible_targets.remove(cord)
        except:
            print("b")
        self.last_guess = cord
        # print(cord)
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
        # cord = self.potential_targets.pop()
        # while cord not in self.possible_targets:
        #     if len(self.potential_targets) > 0:
        #         cord = self.potential_targets.pop()
        #     else:
        #         cord = random.choice(self.possible_targets)
        # return cord

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

            if vertical < smallest_ship-1 and horizontal < smallest_ship-1:
                elimination.append(i)
        for i in elimination:
            self.parity_grid.clear()
            if i in self.possible_targets:
                self.possible_targets.remove(i)
        # print("ELEM:", elimination)



class ProbabilityDensity(Algorithm):
    # Voor elk schip dat er nog is
    #   Voor elke tile
    #       Past schip? Tile prob ++
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
                # print(self.result[1], len(self.hit_streak))
                if self.result[1] == len(self.hit_streak):
                    self.hit_streak.clear()
        if self.hit_streak:
            probabilities = self.probability(True)
        else:
            probabilities = self.probability(False)
        try:
            cord = list(probabilities.pop())
        except:
            print("b")
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

        # print(probability_tracker)

        for i in range(10):
            string = ""
            for j in range(10):
                try:
                    string += str(probability_tracker[j, i]) + "  "
                except KeyError:
                    string += "0  "
            # print(string)
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
        try:
            cord = random.choice(self.possible_targets)
            self.possible_targets.remove(cord)
        except:
            print("breaking")
        return cord

# IDEAS:
# Keep track of entire ships ( see "C:/Users/Floris%20Videler/Pictures/Aantekening%202020-06-08%20092556.png" why this is usefull)
# Better target algorithm ( check what direction the ship is facing )
