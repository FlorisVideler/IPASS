import pygame
import random
import algortims
import sys


class Ship:
    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0
    length = None
    hits = 0

    def __init__(self, length: int, board: object):
        """
        Initializer for Ship.

        :param length: Int
        :param board: Board
        """
        self.cords = []
        self.end_x = length
        self.length = length
        self.cords = self.get_cords()
        self.board = board

    def get_cords(self) -> list:
        """
        Gets te coordinates based on a start and end.

        :return: List
        """
        if self.end_x - self.start_x > 0:
            for i in range(self.start_x, self.end_x):
                cord = [i, self.start_y]
                self.cords.append(cord)
        else:
            for i in range(self.start_y, self.end_y):
                cord = [self.start_x, i]
                self.cords.append(cord)
        return self.cords

    def move(self, direction: str):
        """
        Translates the direction input to coordinates.

        :param direction: String
        """
        new_cords = []
        if direction == "up":
            for cord in self.cords:
                x, y = cord
                new_cords.append([x, y - 1])
        elif direction == "right":
            for cord in self.cords:
                x, y = cord
                new_cords.append([x + 1, y])
        elif direction == "down":
            for cord in self.cords:
                x, y = cord
                new_cords.append([x, y + 1])
        else:
            for cord in self.cords:
                x, y = cord
                new_cords.append([x - 1, y])
        self.update_position(new_cords)

    def draw(self, cords: list):
        """
        Draws the given coordinates on in the data object.

        :param cords: List
        """
        for cord in cords:
            x, y = cord
            self.board.data["shoot_grid"][f"{x};{y}"] = "ship"

    def rotate(self):
        """
        Rotates the current ship.
        """
        new_cords = [self.cords[0]]
        xdelta = self.cords[len(self.cords) - 1][0] - self.cords[0][0]
        ydelta = self.cords[len(self.cords) - 1][1] - self.cords[0][1]

        if xdelta > ydelta:
            for i in range(0, self.length - 1):
                x, y = new_cords[i][0], new_cords[i][1] + 1
                new_cords.append([x, y])
        else:
            for i in range(0, self.length - 1):
                x, y = new_cords[i][0] + 1, new_cords[i][1]
                new_cords.append([x, y])
        self.update_position(new_cords, True)

    def update_position(self, new_cords: list, rotate: bool = False):
        """
        Updates the position of the ship.

        :param new_cords: List
        :param rotate: List
        """
        overlap = self.board.overlap_cords(self, new_cords, rotate)
        if not isinstance(overlap, bool):
            while overlap:
                new_cords = overlap[1]
                overlap = self.board.overlap_cords(self, new_cords, rotate)
                if not isinstance(overlap, bool):
                    new_cords = overlap[1]
                if not overlap:
                    break
                if overlap == True:
                    break

        if not overlap:
            for cord in self.cords:
                x, y = cord
                self.board.data["shoot_grid"][f"{x};{y}"] = "tile"
            for cord in new_cords:
                x, y = cord
                self.board.data["shoot_grid"][f"{x};{y}"] = "ship"
            self.cords = new_cords


class Board:

    def __init__(self, ship_sizes: list):
        """
        Initiator for Board

        :param ship_sizes: List
        """
        self.ships = []
        self.shots = []
        self.ship_sizes = ship_sizes
        self.data = {}
        self.data["colors"] = {}
        self.data["colors"]["tile"] = (0, 0, 200)
        self.data["colors"]["hit"] = (200, 0, 0)
        self.data["colors"]["ship"] = (175, 175, 175)
        self.data["colors"]["select"] = (168, 235, 52)
        self.data["colors"]["miss"] = (52, 235, 232)

        self.data["shoot_grid"] = {}
        self.data["plot_grid"] = {}

        for i in range(10):
            for j in range(10):
                self.data["shoot_grid"][f"{i};{j}"] = "tile"
        for i in range(10):
            for j in range(10):
                self.data["plot_grid"][f"{i};{j}"] = "tile"

        self.data["prev"] = {}
        self.data["prev"]["shoot_grid"] = {}
        self.data["prev"]["plot_grid"] = {}

        for i in range(10):
            for j in range(10):
                self.data["prev"]["shoot_grid"][f"{i};{j}"] = "tile"
        for i in range(10):
            for j in range(10):
                self.data["prev"]["plot_grid"][f"{i};{j}"] = "tile"

    def overlap_cords(self, ship: Ship, cords: list, rotate: bool = False) -> (bool, list):
        """
        Returns if a ship is overlapping with coordinates given and if so also return valid coordinates.

        :param ship: Ship
        :param cords: List
        :param rotate: Boolean
        :return: Bool, List
        """
        if self.out_of_bounds(cords):
            return True
        # Remove the first cord if an rotation is being made, this will always be itself.
        if rotate:
            cords = cords[1:]
        overlap = False
        for cord in cords:
            x, y = cord
            if self.data["shoot_grid"][f"{x};{y}"] == "ship":
                other_ship = self.get_ship([x, y])
                if self.overlap(ship, other_ship):
                    overlap = True
                    break
        if rotate and overlap:
            return True
        if overlap:
            deltax = abs(ship.cords[0][0] - cords[0][0])
            deltay = abs(ship.cords[0][1] - cords[0][1])
            new_cords = []
            if deltax > deltay:
                # Left or right
                if ship.cords[0][0] > cords[0][0]:
                    for cord in cords:
                        x, y = cord
                        new_cords.append([x - 1, y])
                else:
                    for cord in cords:
                        x, y = cord
                        new_cords.append([x + 1, y])
            else:
                # Up or down
                if ship.cords[0][1] > cords[0][1]:
                    # UP
                    for cord in cords:
                        x, y = cord
                        new_cords.append([x, y - 1])
                else:
                    # Down
                    for cord in cords:
                        x, y = cord
                        new_cords.append([x, y + 1])
            return False, new_cords
        return False

    def out_of_bounds(self, cords: list) -> bool:
        """
        Returns whether or not coordinates are out of bounds.

        :param cords: List
        :return: Boolean
        """
        for cord in cords:
            for xy in cord:
                if xy < 0 or xy > 9:
                    return True
        return False

    def get_ship(self, cord: list) -> Ship:
        """
        Returns the ship on a given coordinate.

        :param cord: List
        :return: Ship
        """
        for s in self.ships:
            if cord in s.cords:
                return s

    def overlap(self, ship: Ship, other_ship: Ship) -> bool:
        """
        Returns whether or not a ship is overlapping with another ship.

        :param ship: Ship
        :param other_ship: Ship
        :return: Boolean
        """
        if ship != other_ship:
            return True
        return False

    def overlap_cord_ship(self, cords: list, ship: Ship) -> bool:
        """
        Returns if a coordinate overlaps with the coordinates of a Ship.

        :param cords: List
        :param ship: Ship
        :return: Boolean
        """
        for cord in cords:
            if cord in ship.cords:
                return True
        return False

    def place_ships(self):
        """
        Places all the ships
        """
        for i in self.ship_sizes:
            self.place_ship(i)

    def hit(self, cord: list) -> (bool, int):
        """
        Returns whether the guess was a hit or not and if a ship was destroyed also return what the length of the
        ships was.

        :param cord: List
        :return: Boolean, Int
        """
        for ship in self.ships:
            if cord in ship.cords:
                ship.hits += 1
                if ship.hits == ship.length:
                    self.ships.remove(ship)
                    return True, ship.length
                return True, 0
        return False, 0

    def shot_available(self, cord: list) -> bool:
        """
        Returns whether or not a shot is available.
        :param cord: List
        :return: Boolean
        """
        if cord in self.shots:
            return False
        return True

    def shoot(self, cord: list) -> (bool, int):
        """
        Returns hit info.

        :param cord: list
        :return: Boolean, Int
        """
        x, y = cord
        self.shots.append(cord)
        hit = self.hit(cord)
        if hit[0]:
            self.data["shoot_grid"][f"{x};{y}"] = "hit"
        else:
            self.data["shoot_grid"][f"{x};{y}"] = "miss"
        return hit

    def reset(self):
        """
        Removes all the ships.
        """
        for ship in self.ships:
            del ship
        self.ships.clear()

    def place_ship(self, i: int):
        """
        Places a Ship.

        :param i: Int
        """
        pass


class PlayerBoard(Board):
    def __init__(self, ship_sizes: list, display):
        """
        Initiator for PlayerBoard
        :param ship_sizes: List
        :param display: Display
        """
        super().__init__(ship_sizes)
        self.display = display

    def place_ship(self, length: int):
        """
        Moves the ship bases on keyboard input.

        :param length: Int
        """
        ship = Ship(length, self)
        ship.draw(ship.cords)
        self.ships.append(ship)
        placed = False
        while not placed:
            self.display.show(self)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        placed = True
                    elif event.key == pygame.K_DOWN:
                        ship.move("down")
                    elif event.key == pygame.K_UP:
                        ship.move("up")
                    elif event.key == pygame.K_LEFT:
                        ship.move("left")
                    elif event.key == pygame.K_RIGHT:
                        ship.move("right")
                    elif event.key == pygame.K_r:
                        ship.rotate()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def selector_click(self, position: tuple) -> list:
        """
        Returns the coordinate of the clicked tile

        :param position: List
        :return: List
        """
        rects = self.display.rects
        for rect in rects:
            if rect.collidepoint(position):

                index = rects.index(rect)
                cord_string = list(self.data["plot_grid"].keys())[index]
                cord = [int(cord_string.split(";")[0]), int(cord_string.split(";")[1])]
                if self.data["plot_grid"][f"{cord[0]};{cord[1]}"] == "tile":
                    return cord
        return [0]

    def select_cord(self) -> list:
        """
        Returns what coordinate was selected.

        :return: List
        """
        while True:
            self.display.show(self)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    cord = self.selector_click(pos)
                    if cord != [0]:
                        return cord
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


class AIBoard(Board):
    def __init__(self, ship_sizes):
        """
        Initiator for AIBoard

        :param ship_sizes: List
        """
        super().__init__(ship_sizes)

    def place_ship(self, length: int):
        """
        Places all the ships randomly.

        :param length: Int
        """
        ship = Ship(length, self)
        self.ships.append(ship)
        cords = self.random_cords(length)
        while self.overlap_cords(ship, cords):
            cords = self.random_cords(length)
        ship.cords = cords
        ship.draw(cords)

    def random_cords(self, length: int) -> list:
        """
        Returns random coordinates to place a ship.

        :param length: Int
        :return: List
        """
        x = random.randrange(10)
        y = random.randrange(10)
        r = random.randrange(2)

        cords = [[x, y]]

        for i in range(length - 1):
            if r == 1:
                # horizontal
                cords.append([cords[i][0] + 1, cords[i][1]])
            else:
                cords.append([cords[i][0], cords[i][1] + 1])
                # vert
        return cords


class Display:
    def __init__(self):
        """
        Initiator for Display.
        """
        self.rects = []
        self.text = "begin text"
        pygame.init()
        self.text_color = (52, 235, 232)
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 500
        self.background = (10, 10, 10)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Battleships")
        self.font = pygame.font.SysFont('rockwellvet', 30)
        self.img = self.font.render(self.text, True, self.text_color)
        self.rect = self.img.get_rect()
        self.rect.topleft = (20, 420)


    def show(self, player_board: Board, w: int = None, h: int = None):
        """
        Shows the game on the screen.

        :param player_board: Board
        :param w: Int
        :param h: Int
        """
        img = self.font.render(self.text, True, self.text_color)
        self.rect.size = img.get_size()
        self.rect.size = self.img.get_size()
        self.rect.topleft = (20, self.SCREEN_HEIGHT * 0.84)
        self.screen.fill(self.background)
        self.screen.blit(img, self.rect)
        TILE_WIDTH = self.screen.get_width() / 25
        TILE_HEIGHT = self.screen.get_height() / 12.5
        SPACE = self.screen.get_height() / 500

        data = player_board.data

        shoot_grid = data["shoot_grid"]
        plot_grid = data["plot_grid"]

        self.rects.clear()

        for i in range(10):
            for j in range(10):
                tile = pygame.Rect(i * (TILE_WIDTH + SPACE), j * (TILE_HEIGHT + SPACE), TILE_WIDTH, TILE_HEIGHT)
                pygame.draw.rect(self.screen, data["colors"][shoot_grid[f"{i};{j}"]], tile)
        for i in range(12, 22):
            for j in range(10):
                tile = pygame.Rect(i * (TILE_WIDTH + SPACE), j * (TILE_HEIGHT + SPACE), TILE_WIDTH, TILE_HEIGHT)
                pygame.draw.rect(self.screen, data["colors"][plot_grid[f"{i - 12};{j}"]], tile)
                self.rects.append(tile)

        pygame.display.update()

        if w is None or h is None:
            w = self.SCREEN_WIDTH
            h = self.SCREEN_HEIGHT
        else:
            self.SCREEN_WIDTH = w
            self.SCREEN_HEIGHT = h

        self.screen = pygame.display.set_mode((w, h),
                                              pygame.RESIZABLE)

    def pick_algorithm(self):
        font = pygame.font.SysFont('rockwellvet', 30)
        lines = ["Pick an algorithm to battle against!", "1. Random (easy)", "2. Hunt/Target (medium)",
                 "3. Hunt/Target with parity (hard)", "4. Probability Density (hardest)"]
        labels = []
        for line in lines:
            labels.append(font.render(line, True, self.text_color))
        i = 0
        for label in labels:
            rect = label.get_rect()
            rect.topleft = (20, 20+(30*i))
            self.screen.blit(label, rect)
            i += 1
        pygame.display.update()


class Game:
    def __init__(self, display, ship_sizes=[5, 4, 3, 3, 2]):
        """
        Initiator for Game.

        :param display: Display
        :param ship_sizes: List
        """
        self.display = display
        self.player_board = PlayerBoard(ship_sizes, self.display)
        self.ai_board = AIBoard(ship_sizes)
        self.game_over = False
        self.AI = self.pick_algorithm(ship_sizes)

    def pick_algorithm(self, ship_sizes: list) -> algortims.Algorithm:
        """
        Returns what algorithm to use based on user input.
        :param ship_sizes: List
        :return: Algorithm object
        """
        self.display.pick_algorithm()
        ai_set = False
        ai = "1"
        while not ai_set:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        ai = "1"
                        ai_set = True
                    if event.key == pygame.K_2:
                        ai = "2"
                        ai_set = True
                    if event.key == pygame.K_3:
                        ai = "3"
                        ai_set = True
                    if event.key == pygame.K_4:
                        ai = "4"
                        ai_set = True
        if ai == "1":
            return algortims.Random(ship_sizes)
        if ai == "2":
            return algortims.HuntTarget(ship_sizes)
        if ai == "3":
            return algortims.HuntTargetParity(ship_sizes)
        if ai == "4":
            return algortims.ProbabilityDensity(ship_sizes)
        return algortims.Random(ship_sizes)

    def ai_shoot(self):
        """
        Makes the AI shoot.
        """
        cord = self.AI.turn()
        self.AI.result = self.player_board.shoot(cord)

    def player_shoot(self):
        """
        Make the player decided where to shoot.
        """
        cord = self.player_board.select_cord()
        if self.ai_board.shoot(cord)[0]:
            self.player_board.data["plot_grid"][f"{cord[0]};{cord[1]}"] = "hit"
            self.display.text = "HIT!"
            pygame.mixer.music.load('assests/sounds/hit.mp3')
            pygame.mixer.music.play(0)
        else:
            self.player_board.data["plot_grid"][f"{cord[0]};{cord[1]}"] = "miss"
            self.display.text = "MISS!"
            pygame.mixer.music.load('assests/sounds/miss.mp3')
            pygame.mixer.music.play(0)

    def play(self):
        """
        The game setup and main loop.
        """
        self.display.show(self.player_board)
        self.display.text = "Set up your ships"
        self.player_board.place_ships()
        self.ai_board.place_ships()
        i = 0

        while not self.game_over:
            self.display.text = "Use the the mouse to choose where to attack"
            self.player_shoot()
            i += 1
            self.ai_shoot()

            self.check_ships(self.ai_board, self.player_board, i)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pass

                if event.type == pygame.VIDEORESIZE:
                    # There's some code to add back window content here.
                    width = event.w
                    height = int(width / 2)
                    self.check_ships(self.ai_board, self.player_board, i)
                    self.display.show(self.player_board, width, height)
                else:
                    self.check_ships(self.ai_board, self.player_board, i)
                    self.display.show(self.player_board)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def check_ships(self, ai_board: Board, player_board: Board, steps: int):
        """
        Checks if there are still ships on the board.
        :param ai_board: AIBoard
        :param player_board: PlayerBoard
        :param steps: Int
        """
        if not ai_board.ships:
            pygame.mixer.music.load('assests/sounds/win.mp3')
            pygame.mixer.music.play(0)
            self.display.text = f"You win with {steps} shots"
            self.game_over = True
            self.display.show(self.player_board)
        if not player_board.ships:
            pygame.mixer.music.load('assests/sounds/lose.mp3')
            pygame.mixer.music.play(0)
            self.display.text = f"You lost with {steps} shots"
            self.game_over = True
            self.display.show(self.player_board)


if __name__ == "__main__":
    while True:
        d = Display()
        game = Game(d)
        game.play()
