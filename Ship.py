import os
import pygame

images_path = os.path.dirname(os.path.dirname(__file__)) + "/BattleShip/images/"
my_battleship_path = images_path + "my_battleship/"
op_battleship_path = images_path + "op_battleship/"

bat_size = ["S", "M", "L", "XL"]
# My Battleship Images
my_battleships_up_img = [pygame.image.load(my_battleship_path + bat_size[i] + "BattleShipUp" + ".png")
                         for i in range(4)]
my_battleships_side_img = [pygame.image.load(my_battleship_path + bat_size[i] + "BattleShipSide" + ".png")
                           for i in range(4)]
# My Battleships Images - Active
my_battleships_active_up_img = [pygame.image.load(my_battleship_path + bat_size[i] + "BattleShipUp_selected" + ".png")
                                for i in range(4)]
my_battleships_active_side_img = [pygame.image.load(my_battleship_path + bat_size[i] + "BattleShipSide_selected"
                                                    + ".png") for i in range(4)]
# My Battleships Images - Bombed
my_battleships_bombed_up_img = [pygame.image.load(my_battleship_path + bat_size[i] + "BattleShipUp_bombed" + ".png")
                                for i in range(4)]
my_battleships_bombed_side_img = [pygame.image.load(my_battleship_path + bat_size[i] + "BattleShipSide_bombed"
                                                    + ".png") for i in range(4)]
# My Battleships Images - On Board
my_battleships_on_board_side_img = [pygame.image.load(my_battleship_path + bat_size[i] + "BattleShipSide_on_board"
                                                      + ".png") for i in range(4)]
# Op Battleship Images
op_battleships_up_img = [pygame.image.load(op_battleship_path + bat_size[i] + "BattleShipUp" + ".png")
                         for i in range(4)]
op_battleships_side_img = [pygame.image.load(op_battleship_path + bat_size[i] + "BattleShipSide" + ".png")
                           for i in range(4)]
op_battleships_on_board_side_img = [pygame.image.load(op_battleship_path + bat_size[i] + "BattleShipSide_on_board"
                                                      + ".png") for i in range(4)]
# My Battleships Images - Active
op_battleships_active_up_img = [pygame.image.load(op_battleship_path + bat_size[i] + "BattleShipUp_selected" + ".png")
                                for i in range(4)]
op_battleships_active_side_img = [pygame.image.load(op_battleship_path + bat_size[i] + "BattleShipSide_selected"
                                                    + ".png") for i in range(4)]
# My Battleships Images - Bombed
op_battleships_bombed_up_img = [pygame.image.load(op_battleship_path + bat_size[i] + "BattleShipUp_bombed" + ".png")
                                for i in range(4)]
op_battleships_bombed_side_img = [pygame.image.load(op_battleship_path + bat_size[i] + "BattleShipSide_bombed"
                                                    + ".png") for i in range(4)]
# Game Base
my_side = "me"
op_side = "op"

class Ship:

    def __init__(self, size: int, side: str, status: str):
        self.size = size
        self.side = side
        self.status = status
        self.tile_number = list()
        self.up_image = self.set_up_image(status)
        self.side_image = self.set_side_image(status)
        self.sunk = False

    def set_up_image(self, status: str):
        if self.side == my_side:
            switcher = {
                "active": my_battleships_active_up_img[self.size - 1],
                "bombed": my_battleships_bombed_up_img[self.size - 1],
            }
            return switcher.get(status, my_battleships_up_img[self.size - 1])
        switcher = {
            "active": op_battleships_active_up_img[self.size - 1],
            "bombed": op_battleships_bombed_up_img[self.size - 1],
        }
        return switcher.get(status, op_battleships_up_img[self.size - 1])

    def set_side_image(self, status: str):
        if self.side == my_side:
            switcher = {
                "active": my_battleships_active_side_img[self.size - 1],
                "bombed": my_battleships_bombed_side_img[self.size - 1],
                "On_Board": my_battleships_on_board_side_img[self.size - 1],
            }
            return switcher.get(status, my_battleships_side_img[self.size - 1])
        switcher = {
            "active": op_battleships_active_side_img[self.size - 1],
            "bombed": op_battleships_bombed_side_img[self.size - 1],
            "On_Board": op_battleships_on_board_side_img[self.size - 1],
        }
        return switcher.get(status, op_battleships_side_img[self.size - 1])

    def get_size(self):
        return self.size

    def get_status(self):
        return self.status

    def set_status(self, status: str):
        self.status = status
        self.up_image = self.set_up_image(status)
        self.side_image = self.set_side_image(status)

    def get_tile_number(self) -> list:
        return self.tile_number

    def add_tiles(self, tile: int):
        self.tile_number.append(tile)

    def get_side_img(self):
        return self.side_image

    def put_on_tile(self):
        self.status = "On_Board"
        self.set_side_image("On_Board")

    def sink_ship(self):
        self.sunk = True

    def get_sunk(self):
        return self.sunk
        self.status = "bombed"
        self.set_side_image("bombed")
