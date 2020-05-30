from Army import Army
from Tile import Tile

import pygame
import os
import random

# Board
images_path = os.path.dirname(os.path.dirname(__file__)) + "/BattleShip/images/"
tile_path = images_path + "tiles/"
frame_image = pygame.image.load(tile_path + "frame.png")
mouse_over = pygame.image.load(images_path + "Over.png")
number_of_battleship = 8
number_of_tiles = 10
bg_image = pygame.image.load(images_path + 'Base.jpg')
op_rect = pygame.Rect(142, 176, 456, 376)
my_rect = pygame.Rect(920, 176, 456, 376)
my_board = [[0 for i in range(number_of_tiles)] for j in range(number_of_tiles)]
op_board = [[0 for i in range(number_of_tiles)] for j in range(number_of_tiles)]
# Tiles
tile_height = 37
tile_width = 44.7
# Game Base
# My Side
my_side = "me"
# Op Side
op_side = "op"
# BattleShips
my_battleship = [0 for i in range(number_of_battleship)]
amount_of_my_battleship = 0
op_battleship = [0 for i in range(number_of_battleship)]
amount_of_op_battleship = 8
sinked = images_path + "sinked/"
my_sink = [pygame.image.load(sinked + str(i) + "_blue.png") for i in range(1,5)]
op_sink = [pygame.image.load(sinked + str(i) + "_red.png") for i in range(1,5)]
# Main Window
win_x = bg_image.get_width()
win_y = bg_image.get_height()

class Board:

    def __init__(self, start_x: int, start_y: int, side: str, army: Army,
                 num_of_row: int, num_of_col: int, main_win: pygame.display):
        self.main_win = main_win
        self.board = [[0 for i in range(0, num_of_col)] for j in range(0, num_of_row)]
        self.start_x = start_x
        self.start_y = start_y
        self.num_of_col = num_of_col
        self.num_of_row = num_of_row
        self.side = side
        self.army = army
        self.ships_tiles = set()
        self.tiles_checked = set()
        self.set_board()
        self.amount_of_ship = 0

    def set_board(self):
        """
        Setting the board base
        """
        x = self.start_x
        y = self.start_y
        self.main_win.blit(frame_image, (x - 1, y - 1))
        count_tile = 0
        for i in range(0, self.num_of_col):
            for j in range(0, self.num_of_row):
                if x <= win_x and y < win_y:
                    if self.side == "me":
                        self.board[i][j] = Tile(x, y, my_side, i * 10 + j, self.main_win)
                    else:
                        self.board[i][j] = Tile(x, y, op_side, i * 10 + j, self.main_win)
                    count_tile += 1
                x += 46
                # y += 38
            # x += 46
            y += 38
            # y = 175
            x = self.start_x

    def get_amount_of_ship(self):
        return self.amount_of_ship

    def draw_board(self):
        """
        Drawing the board base
        """
        for i in range(number_of_tiles):
            for j in range(number_of_tiles):
                self.board[i][j].draw_tile()

    def get_board(self):
        """
        Return the board
        :return: Player's board
        """
        return self.board

    def get_army(self):
        """
        Return the army in the board
        :return: Army of the player's board
        """
        return self.army

    def add_checked_tile(self, pos: int):
        """

        :param pos:
        :return:
        """
        self.tiles_checked.add(pos)

    def fill_board(self):
        for i in range(number_of_battleship):
            curr_size = self.get_army().get_ship_by_pos(i).get_size()
            tile_to_chose = self.get_available_tiles(curr_size)[
                random.randint(1, len(self.get_available_tiles(curr_size)) - 1)]
            # i, j = Board.get_tile_numbers(tile_to_chose)
            self.put_ship_on_board(tile_to_chose, i)

    def put_ship_on_board(self, pos: int, num_of_ship: int):
        """
        Places a ship on the board.
        The function is dependable on the size of the ship
        :param pos: Tile number on the board (start position)
        :param num_of_ship: Ship number in the army (1->8)
        :return:
        """
        i, j = self.get_tile_numbers(pos)
        self.board[i][j].place_ship(num_of_ship)
        for z in range(self.army.get_ship_by_pos(num_of_ship).get_size()):
            self.board[i][j + z].place_ship(num_of_ship)
            self.get_army().get_ship_by_pos(num_of_ship).add_tiles(pos)
            self.ships_tiles.add(self.get_tile_number_i_j(i, j + z))
            pos += 1
        self.amount_of_ship += 1

    def get_available_tiles(self, ship_size: int):
        """
        Returns array of available tiles to put tiles
        :param ship_size: Ship size
        :return: Array of available tiles
        """
        available_tiles = []
        ship_size -= 1
        for i in range(self.num_of_row):
            for j in range(self.num_of_col - ship_size):
                if self.board[i][j].get_have_ship() == -1:
                    flag = 0
                    for s in range(ship_size + 1):
                        if self.board[i][j + s].get_have_ship() != -1:
                            flag = 1
                    if flag == 0:
                        available_tiles.append(self.get_tile_number_i_j(i, j))
        return available_tiles

    def get_available_ship_by_pos(self) -> list:
        result = list()
        for i in range(self.amount_of_ship):
            if not self.army.get_ship_by_pos(i).get_sunk():
                result.append(i)
        return result

    def get_available_to_check(self):
        """
        Returns the available tiles on the board.
        available tiles - tiles which can be checked
        :return: Array of available tiles
        """
        available_tiles = []
        for i in range(self.num_of_row):
            for j in range(self.num_of_col):
                if not self.board[i][j].get_checked():
                    available_tiles.append(self.get_tile_number_i_j(i, j))
        return available_tiles

    def get_hit_tiles(self):
        """
        Returns the hit tiles on the board.
        hit tiles - tile which checked and has a ship
        :return: Array of hit tiles
        """
        hit_tiles = set()
        for tile in self.ships_tiles:
            i, j = self.get_tile_numbers(tile)
            if self.board[i][j].get_checked():
                hit_tiles.add(tile)
        return hit_tiles

    def get_ship_not_sunk(self) -> list:
        ships = [0, 0, 0, 0]
        for i in range(self.amount_of_ship):
            if not self.army.get_ship_by_pos(i).get_sunk():
                ships[self.army.get_ship_by_pos(i).get_size() - 1] += 1
        return ships

    def get_ship_sunk(self) -> list:
        ships = list()
        for i in range(self.amount_of_ship):
            if self.army.get_ship_by_pos(i).get_sunk():
                ships.append(i)
        # print(ships)
        return ships

    def check_ship_sunk(self, pos):
        """

        :param pos:
        :return:
        """
        curr_ship = self.army.get_ship_by_pos(pos)
        curr_ship_tiles = set(curr_ship.get_tile_number())
        # print(curr_ship_tiles)
        # print(self.tiles_checked)
        # print(curr_ship_tiles.intersection(self.tiles_checked))
        if len(curr_ship_tiles.intersection(self.tiles_checked)) == curr_ship.get_size():
            self.army.get_ship_by_pos(pos).sink_ship()
            print(pos)

    def show_battleship_menu_status(self):
        """
        Showing the battleship on the menu
        """
        if self.side == my_side:
            x_pos = [864, 1048, 1204, 1204, 1301, 1301, 1356, 1356]
            y_pos = [108, 101, 100, 141, 90, 129, 90, 129]
        else:
            x_pos = [83, 83, 140, 140, 203, 203, 314, 456]
            y_pos = [89, 130, 89, 130, 100, 132, 109, 116]
        for i in range(self.army.get_total_size()):
            # Menu
            if self.side == my_side:
                curr_side_img = self.army.get_ship_by_pos(self.army.get_total_size() - i - 1).get_side_img()
            else:
                curr_side_img = self.army.get_ship_by_pos(i).get_side_img()
            self.main_win.blit(curr_side_img, (x_pos[i], y_pos[i]))

    def show_battleship_board_status(self):
        """
        Showing the battleship on the board
        """
        # available_ships = self.get_available_ship_by_pos()
        if self.side == my_side:
            for j in range(self.amount_of_ship):
                # ship_number = available_ships[j]
                curr_ship = self.army.get_ship_by_pos(j)
                tile_number = curr_ship.get_tile_number()[0]
                i, j = Board.get_tile_numbers(tile_number)
                x, y = self.board[i][j].get_pos()
                if curr_ship.get_size() == 2:
                    y += 7
                    x += 7
                elif curr_ship.get_size() == 3:
                    y -= 10
                    x += 7
                elif curr_ship.get_size() == 4:
                    x += 14
                self.main_win.blit(curr_ship.get_side_img(), (x, y))
            # print(self.get_ship_sunk())
        sunk_ships = self.get_ship_sunk()
        for i in range(len(sunk_ships)):
            curr_ship = self.army.get_ship_by_pos(sunk_ships[i])
            tile_number = curr_ship.get_tile_number()[0]
            i, j = Board.get_tile_numbers(tile_number)
            x, y = self.board[i][j].get_pos()
            # print(f"{x}, {y} -> {op_sink[curr_ship.get_size() - 1]}")
            if self.side == "me":
                self.main_win.blit(my_sink[curr_ship.get_size() - 1], (x - 3, y - 3))
            else:
                self.main_win.blit(op_sink[curr_ship.get_size() - 1], (x - 3, y - 3))



    # Auxiliary functions

    # Get i and j
    def get_tile_i_j_by_pos(self, x: int, y: int) -> tuple:
        """
        Auxiliary function to get row and column based on position
        of the mouse
        :param x: width
        :param y: height
        :return: Tuple, (number of row, number of column)
        """
        if self.side == op_side:
            return int((y - op_rect.top) / (tile_height + 1)), int((x - op_rect.left) / (tile_width + 1))
        else:
            return int((y - my_rect.top) / (tile_height + 1)), int((x - my_rect.left) / (tile_width + 1))

    # Get x and y
    def get_tile_x_y_by_i_j(self, i: int, j: int) -> tuple:
        """
        Auxiliary function to get the mouse position on the window based
        on the place in board
        :param i: number of row
        :param j: number of column
        :return: mouse position
        """
        return self.board[i][j].get_x(), self.board[i][j].get_y()

    def get_tile_number_i_j(self, i: int, j: int) -> int:
        """
        Auxiliary function to get the tile number (i*row+j)
        :param i: row number
        :param j: column number
        :return: tile number as an array
        """
        return i * self.num_of_row + j

    @staticmethod
    def get_side_by_x_y(x: int, y: int):
        """
        Auxiliary function to get which side is the mouse based
        on the mouse position.
        :param x: width
        :param y: height
        :return: Which side is the mouse
        """
        if my_rect.collidepoint(x, y):
            return my_side
        return op_side

    # Get tile numbers by one number
    @staticmethod
    def get_tile_numbers(tile_number) -> tuple:
        """
        Auxiliary function to get the row and column number in the board
        :param tile_number: tile number
        :return: i -> row j -> column
        """
        return int(tile_number / 10), int(tile_number % 10)
