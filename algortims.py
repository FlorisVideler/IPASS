import random


class Algorithm:
    def __init__(self, ships):
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


class HuntTarget:
    def __init__(self, ships):
        self.result = None
        self.possible_targets = []
        self.last_guess = None
        self.potential_targets = []
        for i in range(10):
            for j in range(10):
                self.possible_targets.append([i, j])

    def turn(self):
        if self.result:
            self.potential_targets.extend(self.get_surrounding(self.last_guess))
        if self.potential_targets:
            cord = self.target()
        else:
            cord = self.hunt()
        self.last_guess = cord
        self.possible_targets.remove(cord)
        return cord

    def hunt(self):
        return random.choice(self.possible_targets)

    def target(self):
        return self.potential_targets.pop()

    def get_surrounding(self, cord):
        surroundings = []
        x, y = cord
        if x + 1 < 10 and [x + 1, y] in self.possible_targets and [x + 1, y] not in self.potential_targets:
            surroundings.append([x + 1, y])
        if x - 1 > -1 and [x - 1, y] in self.possible_targets and [x - 1, y] not in self.potential_targets:
            surroundings.append([x - 1, y])
        if y + 1 < 10 and [x, y + 1] in self.possible_targets and [x, y + 1] not in self.potential_targets:
            surroundings.append([x, y + 1])
        if y - 1 > -1 and [x, y - 1] in self.possible_targets and [x, y - 1] not in self.potential_targets:
            surroundings.append([x, y - 1])
        return surroundings


class HuntTargetParity:
    def __init__(self, ships):
        self.result = None
        self.possible_targets = []
        self.last_guess = None
        self.potential_targets = []
        for i in range(10):
            for j in range(10):
                self.possible_targets.append([i, j])
        self.parity_grid = []
        for i in range(10):
            if i % 2 == 0:
                for j in range(1, 10, 2):
                    self.parity_grid.append([i, j])
            else:
                for j in range(0, 10, 2):
                    self.parity_grid.append([i, j])

    def turn(self):
        if self.result:
            self.potential_targets.extend(self.get_surrounding(self.last_guess))
        if self.potential_targets:
            cord = self.target()
        else:
            cord = self.hunt()
        self.possible_targets.remove(cord)
        self.last_guess = cord
        return cord

    def hunt(self):
        if self.parity_grid:
            cord = random.choice(self.parity_grid)
            while cord not in self.possible_targets:
                cord = random.choice(self.parity_grid)
            self.parity_grid.remove(cord)
        else:
            cord = random.choice(self.possible_targets)
        return cord

    def target(self):
        return self.potential_targets.pop()

    def get_surrounding(self, cord):
        surroundings = []
        x, y = cord
        if x + 1 < 10 and [x + 1, y] in self.possible_targets and [x + 1, y] not in self.potential_targets:
            surroundings.append([x + 1, y])
        if x - 1 > -1 and [x - 1, y] in self.possible_targets and [x - 1, y] not in self.potential_targets:
            surroundings.append([x - 1, y])
        if y + 1 < 10 and [x, y + 1] in self.possible_targets and [x, y + 1] not in self.potential_targets:
            surroundings.append([x, y + 1])
        if y - 1 > -1 and [x, y - 1] in self.possible_targets and [x, y - 1] not in self.potential_targets:
            surroundings.append([x, y - 1])
        return surroundings


class ProbabilityDensity:
    # Voor elk schip dat er nog is
    #   Voor elke tile
    #       Past schip? Tile prob ++
    def __init__(self, ships):
        self.ships = ships
        self.result = None
        self.possible_targets = []
        self.last_guess = None
        self.hit_streak = []
        for i in range(10):
            for j in range(10):
                self.possible_targets.append([i, j])

    def turn(self):

        if self.result:
            if not isinstance(self.result, bool):
                self.ships.remove(self.result[1])
            self.hit_streak.append(self.last_guess)
        if self.hit_streak:
            probabilities = self.hit_probabilties()
        else:
            probabilities = self.probability()
        cord = list(probabilities.pop())
        self.possible_targets.remove(cord)
        self.last_guess = cord
        return cord

    def hit_probabilties(self):
        if not isinstance(self.result, bool):
            if self.result[1] == len(self.hit_streak):
                self.hit_streak.clear()
                print("SHIP DESTOYYEEEDDDD")
                return self.probability()
        probability_tracker = {}
        if len(self.hit_streak) == 1:
            x, y = self.hit_streak[0]
            directions = {
                "north": 0,
                "east": 0,
                "south": 0,
                "west": 0
            }
            for ship in self.ships:

                for i in range(1, ship):
                    if [x+1, y] in self.possible_targets:
                        directions["east"] += 1
                    if [x-1, y] in self.possible_targets:
                        directions["west"] += 1
                    if [x, y+1] in self.possible_targets:
                        directions["south"] += 1
                    if [x, y-1] in self.possible_targets:
                        directions["north"] += 1
            best_direction = max(directions, key=directions.get)
            print(best_direction, directions)
            if best_direction == "north":
                return [[x, y-1]]
            elif best_direction == "east":
                return [[x+1, y]]
            elif best_direction == "south":
                return [[x, y+1]]
            else:
                return [[x-1, y]]
        elif len(self.hit_streak) > 1:
            horizontal = False
            vertical = False
            for i in range(1, len(self.hit_streak)):
                prevx, prevy = self.hit_streak[i-1]
                x, y = self.hit_streak[i]
                if abs(x - prevx) != 0:
                    horizontal = True
                else:
                    vertical = True
            if horizontal and not vertical:
                x, y = self.hit_streak[len(self.hit_streak)-1]
                if [x+1, y] in self.possible_targets:
                    return [[x+1, y]]
                elif [x-1, y] in self.possible_targets:
                    return [[x-1, y]]

            if vertical and not horizontal:
                x, y = self.hit_streak[len(self.hit_streak) - 1]
                if [x, y+1] in self.possible_targets:
                    return [[x, y+1]]
                elif [x, y-1] in self.possible_targets:
                    return [[x, y-1]]

            if vertical and horizontal:
                cord = random.choice(self.possible_targets)
                return [[cord]]
            else:
                cord = random.choice(self.possible_targets)
                return [[cord]]



            # directions_tracker = {}
            #
            # for ship in self.ships:
            #     x, y = self.hit_streak[0]
            #     north_tracker = {}
            #     east_tracker = {}
            #     south_tracker = {}
            #     west_tracker = {}
            #     for i in range(1, ship):
            #         if [x+i, y] in self.possible_targets:
            #             if tuple([x+i, y]) not in east_tracker:
            #                 east_tracker[tuple([x+i, y])] = 0
            #             east_tracker[tuple([x+i, y])] += 1
            #         else:
            #             east_tracker.clear()
            #         if [x-i, y] in self.possible_targets:
            #             if tuple([x-i, y]) not in west_tracker:
            #                 west_tracker[tuple([x-i, y])] = 0
            #             west_tracker[tuple([x-i, y])] += 1
            #         else:
            #             west_tracker.clear()
            #         if [x, y+i] in self.possible_targets:
            #             if tuple([x, y+i]) not in south_tracker:
            #                 south_tracker[tuple([x, y+i])] = 0
            #             south_tracker[tuple([x, y+i])] += 1
            #         else:
            #             south_tracker.clear()
            #         if [x, y-i] in self.possible_targets:
            #             if tuple([x, y-i]) not in north_tracker:
            #                 north_tracker[tuple([x, y-i])] = 0
            #             north_tracker[tuple([x, y-i])] += 1
            #         else:
            #             north_tracker.clear()
            #
            #     for i in north_tracker.keys():
            #         if i not in directions_tracker:
            #             directions_tracker[i] = 0
            #         directions_tracker[i] += north_tracker[i]
            #     for i in east_tracker.keys():
            #         if i not in directions_tracker:
            #             directions_tracker[i] = 0
            #         directions_tracker[i] += east_tracker[i]
            #     for i in south_tracker.keys():
            #         if i not in directions_tracker:
            #             directions_tracker[i] = 0
            #         directions_tracker[i] += south_tracker[i]
            #     for i in west_tracker.keys():
            #         if i not in directions_tracker:
            #             directions_tracker[i] = 0
            #         directions_tracker[i] += west_tracker[i]
            #
            # probability_tracker = directions_tracker
            # sorted_tracker = {k: v for k, v in sorted(probability_tracker.items(), key=lambda item: item[1])}
            # probability_tracker_list = [*sorted_tracker]
            # return probability_tracker_list


            # for ship in self.ships:
            #     for tile in self.hit_streak:
            #         # Check which direction the ships can go form the hit
            #         x, y = tile
            #         north = 0
            #         east = 0
            #         south = 0
            #         west = 0
            #         for i in range(1, ship):
            #             if [x+i, y] in self.possible_targets:
            #                 east += 1
            #             if [x-i, y] in self.possible_targets:
            #                 west += 1
            #             if [x, y+1] in self.possible_targets:
            #                 south += 1
            #             if [x, y-1] in self.possible_targets:
            #                 north += 1



    def probability(self):
        probability_tracker = {}
        for ship in self.ships:
            for tile in self.possible_targets:
                # Horizontal
                x, y = tile
                horizontal_tile_tracker = {}
                vertical_tile_tracker = {}

                for i in range(ship):
                    if [x+i, y] in self.possible_targets:
                        if tuple([x+i, y]) not in horizontal_tile_tracker:
                            horizontal_tile_tracker[tuple([x+i, y])] = 0
                        horizontal_tile_tracker[tuple([x+i, y])] += 1
                    else:
                        horizontal_tile_tracker.clear()
                    if [x, y+i] in self.possible_targets:
                        if tuple([x, y+i]) not in vertical_tile_tracker:
                            vertical_tile_tracker[tuple([x, y+i])] = 0
                        vertical_tile_tracker[tuple([x, y+i])] += 1
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
                #
                #
                #
                # horizontal = 0
                # vertical = 0
                # for i in range(ship):
                #     if [x+i, y] in self.possible_targets:
                #         horizontal += 1
                #     if [x, y+i] in self.possible_targets:
                #         vertical += 1
                # if tuple(tile) not in probability_tracker:
                #     probability_tracker[tuple(tile)] = 0
                # if horizontal == ship:
                #     probability_tracker[tuple(tile)] += 1
                # if vertical == ship:
                #     probability_tracker[tuple(tile)] += 1
        print(probability_tracker)
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
        return probability_tracker_list
                #print(probability_tracker[(j,i)], probability_tracker[(j,i)], probability_tracker[(j,i)], probability_tracker[(j,i)], probability_tracker[(j,i)], probability_tracker[(j,i)], probability_tracker[(j,i)], probability_tracker[(j,i)], probability_tracker[(j,i)], probability_tracker[(j,i)])
        #print(probability_tracker[(0,0)], probability_tracker[(1,0)], probability_tracker[(2,0)], probability_tracker[(3,0)], probability_tracker[(4,0)], probability_tracker[(5,0)], probability_tracker[(6,0)], probability_tracker[(7,0)], probability_tracker[(8,0)], probability_tracker[(9,0)])



class Random:
    def __init__(self):
        self.possible_targets = []
        for i in range(10):
            for j in range(10):
                self.possible_targets.append([i, j])

    def turn(self):
        cord = random.choice(self.possible_targets)
        self.possible_targets.remove(cord)
        return cord

# IDEAS:
# Keep track of entire ships ( see "C:/Users/Floris%20Videler/Pictures/Aantekening%202020-06-08%20092556.png" why this is usefull)
# Better target algorithm ( check what direction the ship is facing )
# Devide hunt/target and prob algoritms
