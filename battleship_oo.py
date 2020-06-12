import pygame
import random
import algortims
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
        self.update_position(new_cords, True)

    def update_position(self, new_cords, rotate=False):
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

    def overlap_cords(self, ship, cords, rotate=False):
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
            # print("OVERLAP")
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
            # print(False, new_cords)
            # if not self.overlap_cords(ship, new_cords):
            return False, new_cords
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

    def overlap_cord_ship(self, cords, ship):
        for cord in cords:
            if cord in ship.cords:
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
                    # print(f"DESTROYED {ship.length}")
                    self.ships.remove(ship)
                    return True, ship.length
                return True
        return False

    def shot_available(self, cord):
        if cord in self.shots:
            return False
        return True

    def shoot(self, cord):
        x, y = cord
        self.shots.append(cord)
        hit = self.hit(cord)
        if hit:
            self.data["shoot_grid"][f"{x};{y}"] = "hit"
            if not isinstance(hit, bool):
                return hit
            return True
        else:
            self.data["shoot_grid"][f"{x};{y}"] = "miss"
            return False

    def reset(self):
        for ship in self.ships:
            del ship
        self.ships.clear()


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

    def selector(self, newx, newy, oldx, oldy, first=False):
        if first:
            self.data["prev"]["plot_grid"][f"0;0"] = self.data["plot_grid"][f"0;0"]
            self.data["plot_grid"][f"0;0"] = "select"
        if newx != oldx or newy != oldy:
            # selector is verplaatst
            self.data["prev"]["plot_grid"][f"{newx};{newy}"] = self.data["plot_grid"][f"{newx};{newy}"]
            self.data["plot_grid"][f"{oldx};{oldy}"] = self.data["prev"]["plot_grid"][f"{oldx};{oldy}"]
            self.data["plot_grid"][f"{newx};{newy}"] = "select"

    def selector_click(self, position):
        rects = self.display.rects
        for rect in rects:
            if rect.collidepoint(position):
                index = rects.index(rect)
                cord_string = list(self.data["plot_grid"].keys())[index]
                cord = [int(cord_string.split(";")[0]), int(cord_string.split(";")[1])]
                return cord
        pass

    def select_cord(self):
        newx = 0
        newy = 0
        oldx = 0
        oldy = 0
        selected = False
        self.selector(newx, newy, oldx, oldy, True)
        while not selected:
            if (-1 < newx < 10) and (-1 < newy < 10):
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    cord = self.selector_click(pos)
                    return cord


class AIBoard(Board):
    def __init__(self, ship_sizes):
        super().__init__(ship_sizes)

    def place_ship(self, length):
        ship = Ship(length, self)
        self.ships.append(ship)
        cords = self.random_cords(length)
        while self.overlap_cords(ship, cords):
            cords = self.random_cords(length)
        # print(cords)
        ship.cords = cords
        ship.draw(cords)

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

    # def shoot(self, cord):
    #     x, y = cord
    #     if self.hit(cord):
    #         self.data["shoot_grid"][f"{x};{y}"] = "hit"
    #         return True
    #     else:
    #         self.data["shoot_grid"][f"{x};{y}"] = "miss"
    #         return False


class Display:
    def __init__(self):
        self.rects = []
        self.text = "begin text"
        pygame.init()
        self.RED = (255, 0, 0)
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 500
        self.background = (0, 0, 0)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Battleships")

        text = 'this text is editable'
        self.font = pygame.font.SysFont(None, 30)
        self.img = self.font.render(text, True, self.RED)

        self.rect = self.img.get_rect()
        self.rect.topleft = (20, 420)

    def show(self, player_board, w=None, h=None):
        img = self.font.render(self.text, True, self.RED)
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

        # pygame.display.flip()
        pygame.display.update()

        if w is None or h is None:
            w = self.SCREEN_WIDTH
            h = self.SCREEN_HEIGHT
        else:
            self.SCREEN_WIDTH = w
            self.SCREEN_HEIGHT = h

        self.screen = pygame.display.set_mode((w, h),
                                              pygame.RESIZABLE)

    def show_text(self, text):
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(text, True, (250, 250, 250))
        self.screen.blit(textsurface, (0, 450))


class Game:
    def __init__(self, display, ship_sizes=[5, 4, 3, 3, 2]):
        self.display = display
        self.player_board = PlayerBoard(ship_sizes, self.display)
        self.ai_board = AIBoard(ship_sizes)
        self.game_over = False
        self.AI = algortims.ProbabilityDensity(ship_sizes)

    def ai_shoot(self):
        cord = self.AI.turn()
        self.AI.result = self.player_board.shoot(cord)
        # x, y = random.randrange(10), random.randrange(10)
        # while not self.player_board.shot_available([x, y]):
        #     x, y = random.randrange(10), random.randrange(10)
        # result = self.player_board.shoot([x, y])

    def player_shoot(self):
        cord = self.player_board.select_cord()
        if self.ai_board.shoot(cord):
            self.player_board.data["plot_grid"][f"{cord[0]};{cord[1]}"] = "hit"
            self.display.text = "HIT!"
            pygame.mixer.music.load('hit.mp3')
            pygame.mixer.music.play(0)
        else:
            self.player_board.data["plot_grid"][f"{cord[0]};{cord[1]}"] = "miss"
            self.display.text = "MISS!"
            pygame.mixer.music.load('miss.mp3')
            pygame.mixer.music.play(0)

    def play(self):
        self.display.show(self.player_board)
        self.display.text = "Set up your ships, you can move your ships with the arrow keys and rotate them with the r key"
        self.player_board.place_ships()
        self.ai_board.place_ships()
        i = 0
        while not self.game_over:
            # self.display.show_text(str(i))
            self.display.text = "Use the arrow keys to choose where to attack"
            self.player_shoot()
            self.ai_shoot()
            self.check_ships(self.ai_board, self.player_board)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pass

                if event.type == pygame.VIDEORESIZE:
                    # There's some code to add back window content here.
                    # print("eventwidth:", event.w, "| eventheight:", event.h)
                    width = event.w
                    height = int(width / 2)
                    # print("width:", width, "| height:", height)
                    self.check_ships(self.ai_board, self.player_board)
                    self.display.show(self.player_board, width, height)
                else:
                    self.check_ships(self.ai_board, self.player_board)
                    self.display.show(self.player_board)
            # pygame.time.delay(1000)
            # self.check_ships(self.ai_board, self.player_board)
            # self.display.show(self.player_board)

    def check_ships(self, ai_board, player_board):
        if not ai_board.ships:
            self.display.show_text("YOU WIN")
            self.game_over = True
        if not player_board.ships:
            self.display.show_text("YOU LOSE")
            self.game_over = True


if __name__ == "__main__":
    while True:
        clock = pygame.time.Clock()
        d = Display()
        game = Game(d)
        game.play()

# BUGS: Ship placement is wrong. Ships can be placed in side one another (Maybe implement same system as with the
# guessing / move the ships like this https://cliambrown.com/battleship/play.php?)
# Out of bounds tiles can be selected

# IDEAS:
# Add title and under text to text function
# Beter waits between turns
# Text: EX: "AI: G-13.... HIT!"
# Add numbers and letters to the board 1, 10 and a, j
# Replace selector for outline or blinker
# Add exit thingy
# Add parity grid
# Selector spawns near last shot
# Better OO
# Make input loop function
# Add simulation mode
