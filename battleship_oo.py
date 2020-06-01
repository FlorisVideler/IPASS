import pygame
import random
import time


class Ship:
    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0
    length = None
    hits = 0

    def __init__(self, length, board):
        self.cords = []
        self.end_x = length
        self.length = length
        self.cords = self.get_cords()
        self.board = board

    def get_cords(self):
        if self.end_x - self.start_x > 0:
            for i in range(self.start_x, self.end_x):
                cord = [i, self.start_y]
                self.cords.append(cord)
        else:
            for i in range(self.start_y, self.end_y):
                cord = [self.start_x, i]
                self.cords.append(cord)
        return self.cords

    def move(self, direction):
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

    def draw(self, cords):
        for cord in cords:
            x, y = cord
            self.board.data["shoot_grid"][f"{x};{y}"] = "ship"

    def rotate(self):
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
        self.update_position(new_cords)

    def update_position(self, new_cords):
        if not self.board.overlap_cords(self, new_cords):
            for cord in self.cords:
                x, y = cord
                self.board.data["shoot_grid"][f"{x};{y}"] = "tile"
            for cord in new_cords:
                x, y = cord
                self.board.data["shoot_grid"][f"{x};{y}"] = "ship"
            self.cords = new_cords


class Board:

    def __init__(self, ship_sizes):
        self.ships = []
        self.shots = []
        self.ship_sizes = ship_sizes
        self.data = {}
        self.data["colors"] = {}
        self.data["colors"]["tile"] = (0, 0, 200)
        self.data["colors"]["hit"] = (200, 0, 0)
        self.data["colors"]["ship"] = (10, 10, 10)
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

    def overlap_cords(self, ship, cords):
        if self.out_of_bounds(cords):
            return True
        for cord in cords:
            x, y = cord
            if self.data["shoot_grid"][f"{x};{y}"] == "ship":
                other_ship = self.get_ship([x, y])
                return self.overlap(ship, other_ship)
        return False

    def out_of_bounds(self, cords):
        for cord in cords:
            for xy in cord:
                if xy < 0 or xy > 9:
                    return True
        return False

    def get_ship(self, cord):
        for s in self.ships:
            if cord in s.cords:
                return s

    def overlap(self, ship, other_ship):
        if ship != other_ship:
            return True
        return False

    def place_ships(self):
        for i in self.ship_sizes:
            self.place_ship(i)

    def place_ship(self, length):
        pass

    def hit(self, cord):
        for ship in self.ships:
            if cord in ship.cords:
                ship.hits += 1
                if ship.hits == ship.length:
                    print(f"DESTROYED {ship.length}")
                    self.ships.remove(ship)
                return True
        return False

    def shoot(self, cord):
        if cord in self.shots:
            return False
        else:
            x, y = cord
            if self.hit(cord):
                self.data["shoot_grid"][f"{x};{y}"] = "hit"
            else:
                self.data["shoot_grid"][f"{x};{y}"] = "miss"
            self.shots.append(cord)
            return True


class PlayerBoard(Board):
    def __init__(self, ship_sizes, display):
        super().__init__(ship_sizes)
        self.display = display

    def place_ship(self, length):
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

    def selector(self, newx, newy, oldx, oldy):
        if newx != oldx or newy != oldy:
            # selector is verplaatst
            self.data["prev"]["plot_grid"][f"{newx};{newy}"] = self.data["plot_grid"][f"{newx};{newy}"]
            o = self.data["prev"]["plot_grid"][f"{oldx};{oldy}"]
            # print(f"putting {o} on the old spot")
            self.data["plot_grid"][f"{oldx};{oldy}"] = self.data["prev"]["plot_grid"][f"{oldx};{oldy}"]
            self.data["plot_grid"][f"{newx};{newy}"] = "select"
        else:
            # selector is nog op zelfde plek
            pass

        # if self.data["prev"]["plot_grid"][f"{oldx};{oldy}"] != "select":
        #     self.data["prev"]["plot_grid"][f"{oldx};{oldy}"] = self.data["plot_grid"][f"{oldx};{oldy}"]
        #
        #
        # if self.data["plot_grid"][f"{newx};{newy}"] != "select":
        #     self.data["plot_grid"][f"{oldx};{oldy}"] = self.data["prev"]["plot_grid"][f"{oldx};{oldy}"]
        #     print(self.data["plot_grid"][f"{oldx};{oldy}"])
        #     self.data["prev"]["plot_grid"][f"{newx};{newy}"] = self.data["plot_grid"][f"{newx};{newy}"]
        #     print(self.data["prev"]["plot_grid"][f"{newx};{newy}"])
        # self.data["plot_grid"][f"{newx};{newy}"] = "select"

    def select_cord(self):
        newx = 0
        newy = 0
        oldx = 0
        oldy = 0
        selected = False
        while not selected:
            if (newx > -1 and newx < 10) and (newy > -1 and newy < 10):
                self.selector(newx, newy, oldx, oldy)
                self.display.show(self)
                oldy = newy
                oldx = newx
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.data["prev"]["plot_grid"][f"{newx};{newy}"] == "tile":
                            return [newx, newy]
                    elif event.key == pygame.K_DOWN:
                        newy = oldy + 1
                    elif event.key == pygame.K_UP:
                        newy = oldy - 1
                    elif event.key == pygame.K_LEFT:
                        newx = oldx - 1
                    elif event.key == pygame.K_RIGHT:
                        newx = oldx + 1


class AIBoard(Board):
    def __init__(self, ship_sizes):
        super().__init__(ship_sizes)

    def place_ship(self, length):
        cords = []
        x = random.randrange(10)
        y = random.randrange(10)
        r = random.randrange(2)

        ship = Ship(length, self)
        self.ships.append(ship)
        cords = self.random_cords(length)
        while self.overlap_cords(ship, cords):
            cords = self.random_cords(length)
        print(cords)
        ship.cords = cords
        ship.cords = cords

    def random_cords(self, length):
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

    def shoot(self, cord):
        x, y = cord
        if self.hit(cord):
            self.data["shoot_grid"][f"{x};{y}"] = "hit"
            return True
        else:
            self.data["shoot_grid"][f"{x};{y}"] = "miss"
            return False


class Display:
    def __init__(self):
        pygame.init()

        SCREEN_WIDTH = 1000
        SCREEN_HEIGHT = 500
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Battleships")
        self.texts = []

    def show(self, player_board):
        TILE_WIDTH = 40
        TILE_HEIGHT = 40

        data = player_board.data

        shoot_grid = data["shoot_grid"]
        plot_grid = data["plot_grid"]

        for i in range(10):
            for j in range(10):
                tile = pygame.Rect(i * (TILE_WIDTH + 1), j * (TILE_HEIGHT + 1), TILE_WIDTH, TILE_HEIGHT)
                pygame.draw.rect(self.screen, data["colors"][shoot_grid[f"{i};{j}"]], tile)
        for i in range(12, 22):
            for j in range(10):
                tile = pygame.Rect(i * (TILE_WIDTH + 1), j * (TILE_HEIGHT + 1), TILE_WIDTH, TILE_HEIGHT)
                pygame.draw.rect(self.screen, data["colors"][plot_grid[f"{i - 12};{j}"]], tile)
        pygame.display.flip()

    def show_text(self, text):
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(text, True, (250, 250, 250))
        self.screen.blit(textsurface, (0, 450))
        self.texts.append(textsurface)


class Game:
    def __init__(self, display, ship_sizes=[6]):
        self.display = display
        self.player_board = PlayerBoard(ship_sizes, self.display)
        self.ai_board = AIBoard(ship_sizes)
        self.game_over = False

    def ai_shoot(self):
        x, y = random.randrange(10), random.randrange(10)
        while not self.player_board.shoot([x, y]):
            x, y = random.randrange(10), random.randrange(10)

    def player_shoot(self):
        cord = self.player_board.select_cord()
        if self.ai_board.shoot(cord):
            self.player_board.data["plot_grid"][f"{cord[0]};{cord[1]}"] = "hit"
            pygame.mixer.music.load('hit.mp3')
            pygame.mixer.music.play(0)
        else:
            self.player_board.data["plot_grid"][f"{cord[0]};{cord[1]}"] = "miss"
            pygame.mixer.music.load('miss.mp3')
            pygame.mixer.music.play(0)

    def play(self):
        self.display.show(self.player_board)
        self.player_board.place_ships()
        self.ai_board.place_ships()
        while not self.game_over:
            self.player_shoot()
            self.check_ships(self.ai_board, self.player_board)
            self.ai_shoot()
            self.check_ships(self.ai_board, self.player_board)
            self.display.show(self.player_board)

    def check_ships(self, ai_board, player_board):
        if not ai_board.ships:
            self.display.show_text("YOU WIN")
        if not player_board.ships:
            self.display.show_text("YOU LOSE")
        self.game_over = True


if __name__ == "__main__":
    clock = pygame.time.Clock()
    d = Display()
    game = Game(d)
    game.play()
