import algortims
import battleship
import json
import time


class Simulation:
    def __init__(self, ship_sizes: list, i: int):
        """
        Initiator for Simulation.
        :param ship_sizes: List
        """
        self.AI = None
        self.ship_sizes = ship_sizes
        self.write(i)

    def shoot(self, ai: algortims.Algorithm, board: battleship.AIBoard):
        """
        Shoots shot at board.
        :param ai: Algorithm object
        :param board: Board object
        """
        cord = ai.turn()
        ai.result = board.shoot(cord)

    def simulate(self, algo: str, i: int):
        """
        Runs the actual simulations.
        :param algo: String
        :param i: Int
        """
        total_turns = 0

        for i in range(i):
            self.ship_sizes = [5, 4, 3, 3]
            # print(self.ship_sizes)
            if algo == "random":
                self.AI = algortims.Random(self.ship_sizes)
            elif algo == "hunttarget":
                self.AI = algortims.HuntTarget(self.ship_sizes)
            elif algo == "hunttargetparity":
                self.AI = algortims.HuntTargetParity(self.ship_sizes)
            elif algo == "prob":
                self.AI = algortims.ProbabilityDensity(self.ship_sizes)
            ai_board = battleship.AIBoard(self.ship_sizes)
            ai_board.place_ships()
            turns = 0
            while len(ai_board.ships) > 0:
                self.shoot(self.AI, ai_board)
                turns += 1
            self.write_append(turns, algo)
            total_turns += turns
            if i % 10000 == 0:
                print(i)
            # print(f"{i} -- took {turns} turns")

        print(f"{algo} took {total_turns/i} turns on average.")

    def write(self, i: int):
        """
        Writes the amount of times the simulation is going to run to the data file.
        :param i: Int
        """
        data = {"runs": i}
        with open('JSON/data6443332222.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def write_append(self, turns: int, algo: str):
        """
        appends each game to the file
        :param turns: Int
        :param algo: String
        """
        with open('JSON/data6443332222.json') as json_file:
            data = json.load(json_file)
        if algo not in data:
            data[algo] = []
        data[algo].append(turns)
        with open('JSON/data6443332222.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)


def main():
    """
    Runs the simulations.
    """
    # Set all the ship sizes
    ship_sizes = [6, 4, 4, 3, 3, 3, 2, 2, 2, 2]

    times = 50000

    algortims_names = ["random", "hunttarget", "hunttargetparity", "prob"]

    print("Using default ship sizes", ship_sizes)
    print(f"Running all the algorithms {times} times")

    simulation = Simulation(ship_sizes, times)

    for i in algortims_names:
        simulation.simulate(i, times)


if __name__ == "__main__":
    """
    This is run when the program starts. It times the simulation.
    """
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
