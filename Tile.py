import pygame
import os

# Tiles
tile_height = 37
tile_width = 44.7
images_path = os.path.dirname(os.path.dirname(__file__)) + "/BattleShip/images/"
# hit = pygame.image.load(images_path + "Hit.png")
tile_path = images_path + "tiles/"
selected_tile_path = images_path + "tiles_selected/"
r_tile_path = images_path + "red_tiles/"
tile_image = [[pygame.image.load(tile_path + str((i * j) + 1) + ".png") for i in range(10)] for j in range(10)]
selected_tile_image = [[pygame.image.load(selected_tile_path + str((i * j) + 1) + ".png") for i in range(10)] for j in
                       range(10)]
red_tiles_images = [[pygame.image.load(r_tile_path + str((i * j) + 1) + ".png") for i in range(10)] for j in range(10)]

# Game Base
my_side = "me"
op_side = "op"

class Tile:
    hovered = False

    def __init__(self, x: int, y: int, side: str, number: int, main_win: pygame.display):
        self.x = x
        self.y = y
        self.side = side
        self.number = number
        self.height = tile_height
        self.width = tile_width
        self.have_ship = False
        self.checked = False
        self.hit = False
        self.main_win = main_win
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # Return the the width and height of the tile in a list
    def get_size(self):
        return [self.width, self.height]

    # Return the position of the tile
    def get_pos(self):
        return self.x, self.y

    def get_rect(self):
        return self.rect

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_have_ship(self) -> bool:
        return self.have_ship

    def get_checked(self) -> bool:
        return self.checked

    def place_ship(self):
        self.have_ship = True

    def check_tile(self):
        self.checked = True
        if self.have_ship:
            self.hit = True
            return True
        return False

    def get_hit(self):
        return self.hit

    def draw_tile(self):
        if self.side == my_side:
            if self.checked:
                self.main_win.blit(selected_tile_image[int(self.number / 10)][self.number % 10], (self.x, self.y))
            else:
                self.main_win.blit(tile_image[int(self.number / 10)][self.number % 10], (self.x, self.y))
        else:
            if self.checked:
                self.main_win.blit(selected_tile_image[int(self.number / 10)][self.number % 10], (self.x, self.y))
            else:
                self.main_win.blit(tile_image[int(self.number / 10)][self.number % 10], (self.x, self.y))

