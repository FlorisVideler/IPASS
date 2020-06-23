import algortims
import battleship_oo
import json
import time


class Simulation2:
    def __init__(self, ship_sizes):
        self.sizes = ship_sizes
        self.ai_board = battleship_oo.AIBoard(self.sizes)
        self.json_data = {}

    def ai_shoot(self, AI, board, run, turns):
        cord = AI.turn()
        self.add_shot(cord, run, turns)
        AI.result = board.shoot(cord)

    def simulation_game_loop(self, run):
        AI = algortims.HuntTarget([5, 4, 3, 2])
        self.ai_board.reset()
        # print(self.sizes)
        self.ai_board.ship_sizes = [5, 4, 3, 2]
        self.ai_board.place_ships()
        game_over = False
        turns = 0
        while not game_over:
            turns += 1
            self.ai_shoot(AI, self.ai_board, run, turns)
            if not self.ai_board.ships:
                game_over = True
        self.add_result(run, turns)
        # print(turns)

    def add_run(self, run):
        self.json_data[run] = {}
        self.json_data[run]["shots"] = {}
        self.json_data[run]["turns"] = 0

    def add_shot(self, cord, run, turn):
        self.json_data[run]["shots"][turn] = cord

    def add_result(self, run, result):
        self.json_data[run]["turns"] = result

    def write_data(self):
        with open('ai_data.json', 'w') as aid:
            aid.write(json.dumps(self.json_data, indent=4))

    def run(self, times):
        print(f"Running simulation {times} times:")
        for i in range(1, times + 1):
            self.add_run(i)
            self.simulation_game_loop(i)
            # print(i)
        self.write_data()
        pass


class Simulation:
    def __init__(self, ship_sizes):
        self.AI = None
        self.ship_sizes = ship_sizes
        self.write(50000)

    def shoot(self, ai: algortims.Algorithm, board: battleship_oo.AIBoard):
        cord = ai.turn()
        ai.result = board.shoot(cord)

    def simulate(self, algo):
        total_turns = 0

        for i in range(50000):
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
            ai_board = battleship_oo.AIBoard(self.ship_sizes)
            ai_board.place_ships()
            turns = 0
            while len(ai_board.ships) > 0:
                self.shoot(self.AI, ai_board)
                turns += 1
            self.write_append(turns, i, algo)
            total_turns += turns
            if i % 10000 == 0:
                print(i)
            # print(f"{i} -- took {turns} turns")

        print(f"{algo} took {total_turns/50000} turns on average.")

    def write(self, i):
        data = {"runs": i}
        with open('JSON/data6443332222.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def write_append(self, turns, run, algo):
        with open('JSON/data6443332222.json') as json_file:
            data = json.load(json_file)
        if algo not in data:
            data[algo] = []
        data[algo].append(turns)
        with open('JSON/data6443332222.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)


def main():
    ship_sizes = [6, 4, 4, 3, 3, 3, 2, 2, 2, 2]

    algortims_names = ["random", "hunttarget", "hunttargetparity", "prob"]

    print("Using default ship sizes", ship_sizes)
    print("Running all the algorithms 50000 times")

    simulation = Simulation(ship_sizes)

    for i in algortims_names:
        simulation.simulate(i)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
