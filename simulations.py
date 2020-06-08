import algortims
import battleship_oo
import json
import time


class Simulation:
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
        print(self.sizes)
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
        print(turns)

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
            print(i)
        self.write_data()
        pass


def main():
    print("Welcome to the simulations")
    print("What algorithm would you like to simulate?\n"
          "1. Deze")
    algorithm_to_sim = input(": ")
    ship_sizes = [5, 4, 3, 2]

    simulation = Simulation(ship_sizes)
    tic = time.perf_counter()
    simulation.run(1000000)
    toc = time.perf_counter()
    print(f"Simulation ran in {toc - tic:0.4f} seconds")


if __name__ == "__main__":
    main()
