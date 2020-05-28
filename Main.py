from Army import Army
from Board import Board

import os
import platform
import random

import time

import pyautogui
import pygame

# Global Variables
# Game Base
# My Side
my_side = "me"
my_ships_tile_number = set()
# Op Side
op_side = "op"
op_ships_tile_number = set()
# Project images path
# from PyGame.font import FontType
images_path = os.path.dirname(os.path.dirname(__file__)) + "/BattleShip/images/"
tile_path = images_path + "tiles/"
selected_tile_path = images_path + "tiles_selected/"
r_tile_path = images_path + "red_tiles/"
my_battleship_path = images_path + "my_battleship/"
op_battleship_path = images_path + "op_battleship/"

# Computer Information
computer_info = dict()
computer_info['width'], computer_info['height'] = pyautogui.size()
computer_info['operating_system'] = platform.system()
window_scale = computer_info['width'] / computer_info['height']
# Colors
transparent = (0, 0, 0, 0)
black = (0, 0, 0)
# Game Sprites
icon = pygame.image.load(images_path + 'icon.gif')

number_of_tiles = 10
number_of_battleship = 8
# Game Progress
game_status = ["Putting ships on my side", "My turn to guess", "My opponent turn to guess", "Game over"]
curr_game_status = game_status[0]
my_checked_tiles = []
op_checked_tiles = []

# Intro
intro_img = pygame.image.load(images_path + "Intro.jpg")
turn = 1
# Board
bg_image = pygame.image.load(images_path + 'Base.jpg')
op_rect = pygame.Rect(142, 176, 456, 376)
my_rect = pygame.Rect(920, 176, 456, 376)
# BattleShips
my_battleship = [0 for i in range(number_of_battleship)]
amount_of_my_battleship = 0
op_battleship = [0 for i in range(number_of_battleship)]
amount_of_op_battleship = 8
# Tiles
tile_height = 37
tile_width = 44.7
my_board = [[0 for i in range(number_of_tiles)] for j in range(number_of_tiles)]
op_board = [[0 for i in range(number_of_tiles)] for j in range(number_of_tiles)]
frame_image = pygame.image.load(tile_path + "frame.png")
mouse_over = pygame.image.load(images_path + "Over.png")
me_hit = pygame.image.load(images_path + "me_hit.png")
op_hit = pygame.image.load(images_path + "op_hit.png")
hover_active_check = 0
# Mouses Cursor
base = ((16, 16), (0, 0), (0, 0, 64, 0, 96, 0, 112, 0, 120, 0, 124, 0, 126, 0, 127, 0, 127, 128, 124, 0, 108, 0, 70, 0,
                           6, 0, 3, 0, 3, 0, 0, 0), (64, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255, 0, 255, 128,
                                                     255, 192, 255, 128, 254, 0, 239, 0, 79, 0, 7, 128, 7, 128, 3, 0))
bullseye = (8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0)
broken = ((16, 16), (7, 7), (0, 0, 96, 6, 112, 14, 56, 28, 28, 56, 12, 48, 0, 0, 0, 0, 0, 0, 0, 0, 12, 48, 28, 56, 56,
                             28, 112, 14, 96, 6, 0, 0), (224, 7, 240, 15, 248, 31, 124, 62, 62, 124, 30, 120, 14, 112,
                                                         0, 0, 0, 0, 14, 112, 30, 120, 62, 124, 124, 62, 248, 31, 240,
                                                         15, 224, 7))
# Main Window
win_x = bg_image.get_width()
win_y = bg_image.get_height()
main_win = pygame.display.set_mode((win_x, win_y))


def draw_tiles(side: str):
    for i in range(number_of_tiles):
        for j in range(number_of_tiles):
            if side == my_side:
                my_board.draw_board()
            else:
                op_board.draw_board()


# Add Hover Effect To Put On Tiles
def hover_active_put_ships(size: int, x_pos: int, y_pos: int, curr_board: Board):
    available_tiles = curr_board.get_available_tiles(size)
    i, j = curr_board.get_tile_i_j_by_pos(x_pos, y_pos)
    if curr_board.get_tile_number_i_j(i, j) in available_tiles:
        main_win.blit(mouse_over, (curr_board.get_board()[i][j].get_x() - 8, curr_board.get_board()[i][j].get_y() - 8))
    pygame.display.flip()


def hover_check_put_ships(x_pos: int, y_pos: int):
    available_tiles = op_board.get_available_to_check()
    i, j = op_board.get_tile_i_j_by_pos(x_pos, y_pos)
    if op_board.get_tile_number_i_j(i, j) in available_tiles:
        main_win.blit(mouse_over, (op_board.get_board()[i][j].get_x() - 8, op_board.get_board()[i][j].get_y() - 8))
    pygame.display.flip()

def board_text():
    # Text
    font = "Cooper Std"
    title_font = pygame.font.SysFont("Cooper Std", 24)
    par_font = pygame.font.SysFont("Cooper Std", 18)
    title = title_font.render("Game Status", 1, black)
    game_status_label = par_font.render(curr_game_status, 1, black)
    # turn = par_font.render("Game :", 1, black)
    # put the label object on the screen at point x=100, y=100
    main_win.blit(title, (688, 114))
    main_win.blit(game_status_label, (670, 150))
    # main_win.blit(turn, (685, 150))


# Update Mouse Position
def mouse_position(mou_pos):
    par_font = pygame.font.SysFont("Cooper Std", 18)
    mouse_pos = par_font.render(str(mou_pos), 1, black)
    main_win.blit(mouse_pos, (732, 190))


def fill_enemy_battleship():
    global op_board
    for i in range(number_of_battleship):
        curr_size = op_board.get_army().get_ship_by_pos(i).get_size()
        tile_to_chose = op_board.get_available_tiles(curr_size)[random.randint(1, len(op_board.get_available_tiles(curr_size)) - 1)]
        # i, j = Board.get_tile_numbers(tile_to_chose)
        op_board.put_ship_on_board(tile_to_chose, i)


def check_op_square(i: int, j: int):
    global op_board
    op_board[i][j].check_tile()


# Game Intro
def game_intro():
    main_win.blit(intro_img, (0, 0))


# Game Init
def game_init():
    global my_battleship, op_battleship, my_board, op_board
    pygame.init()
    pygame.display.set_caption('BattleShips - Moshe Gotam')
    pygame.display.set_icon(icon)
    main_win.blit(bg_image, (0, 0))
    my_battleship = Army(4, 2, 1, 1, my_side)
    op_battleship = Army(4, 2, 1, 1, op_side)
    my_board = Board(my_rect.left, my_rect.top, my_side, my_battleship, number_of_tiles, number_of_tiles, main_win)
    op_board = Board(op_rect.left, op_rect.top, op_side, op_battleship, number_of_tiles, number_of_tiles, main_win)
    fill_enemy_battleship()
    op_board.show_battleship_menu_status()
    pygame.display.flip()


# Show Game Status
def show_game_status():
    my_board.draw_board()
    op_board.draw_board()
    my_board.show_battleship_menu_status()
    my_board.show_battleship_board_status()
    op_board.show_battleship_menu_status()
    # op_board.show_battleship_board_status()
    board_text()


# Play Game
# def play(event, x_pos, y_pos):
#     global turn, my_battleship, op_battleship, amount_of_my_battleship, amount_of_op_battleship, curr_game_status
#     side = Board.get_side_by_x_y(x_pos, y_pos)
#     # First Turn
#     if curr_game_status == game_status[0] and turn <= my_battleship.get_total_size():
#         no_ship = turn - 1
#         curr_ship = my_battleship.get_ship_by_pos(no_ship)
#         my_battleship.get_ship_by_pos(no_ship).set_status("active")
#         pygame.display.flip()
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             x, y = event.pos
#             if Board.get_side_by_x_y(x, y) == my_side:
#                 # Set the x, y positions of the mouse click
#                 i, j = my_board.get_tile_i_j_by_pos(x, y)
#                 tile_number = my_board.get_tile_number_i_j(i, j)
#                 if tile_number in my_board.get_available_tiles(curr_ship.get_size()):
#                     # main_win.blit(curr_ship.get_side_img(), my_board[i][j].get_pos())
#                     turn += 1
#                     amount_of_my_battleship += 1
#                     my_board.put_ship_on_board(tile_number, no_ship)
#             # if turn > my_battleship.get_total_size():
#             #     print(str(my_board.get_army().get_ship_by_pos(0).get_status()))

# Running Function
def run_game():
    global turn, my_battleship, op_battleship, amount_of_my_battleship, \
        amount_of_op_battleship, curr_game_status, hover_active_check
    game_init()
    run = True
    while run:
        # pygame.time.delay(80)
        main_win.blit(bg_image, (0, 0))
        show_game_status()
        x, y = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            run = False
        mouse_position((x, y))
#########################################################################################
#########################################################################################
############################### Status - Player Put Ships ###############################
#########################################################################################
#########################################################################################
        if curr_game_status == game_status[0]:
            if turn > my_board.get_army().get_total_size():
                curr_game_status = game_status[1]
            else:
                if my_rect.collidepoint(pygame.mouse.get_pos()):
                    curr_size = my_board.get_army().get_ship_by_pos(turn - 1).get_size()
                    hover_active_put_ships(curr_size, x, y, my_board)
                    pygame.mouse.set_cursor(*bullseye)
                else:
                    pygame.mouse.set_cursor(*base)
                for event in pygame.event.get():
                    side = Board.get_side_by_x_y(x, y)
                    # First Turn
                    if curr_game_status == game_status[0] and turn <= my_battleship.get_total_size():
                        no_ship = turn - 1
                        curr_ship = my_battleship.get_ship_by_pos(no_ship)
                        my_battleship.get_ship_by_pos(no_ship).set_status("active")
                        pygame.display.flip()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = event.pos
                            if Board.get_side_by_x_y(x, y) == my_side:
                                # Set the x, y positions of the mouse click
                                i, j = my_board.get_tile_i_j_by_pos(x, y)
                                tile_number = my_board.get_tile_number_i_j(i, j)
                                if tile_number in my_board.get_available_tiles(curr_ship.get_size()):
                                    turn += 1
                                    amount_of_my_battleship += 1
                                    my_board.put_ship_on_board(tile_number, no_ship)
#########################################################################################
#########################################################################################
################################## Status - Player Guess ################################
#########################################################################################
#########################################################################################
        if curr_game_status == game_status[1]:
            for tile_num in range(len(op_board.get_hit_tiles())):
                i, j = Board.get_tile_numbers(op_board.get_hit_tiles()[tile_num])
                main_win.blit(op_hit, (op_board.get_board()[i][j].get_x() - 4, op_board.get_board()[i][j].get_y() - 8))
            for tile_num in range(len(my_board.get_hit_tiles())):
                i, j = Board.get_tile_numbers(my_board.get_hit_tiles()[tile_num])
                main_win.blit(me_hit, (my_board.get_board()[i][j].get_x() - 4, my_board.get_board()[i][j].get_y() - 8))
            # op_board.show_battleship_board_status()
            if turn % 2 != 0:
                if op_rect.collidepoint(pygame.mouse.get_pos()):
                    hover_active_put_ships(1, x, y, op_board)
                    x_pos, y_pos = pygame.mouse.get_pos()
                    hover_check_put_ships(x_pos, y_pos)
                    pygame.mouse.set_cursor(*bullseye)
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = event.pos
                            if Board.get_side_by_x_y(x, y) == op_side:
                                # Set the x, y positions of the mouse click
                                i, j = op_board.get_tile_i_j_by_pos(x, y)
                                tile_number = op_board.get_tile_number_i_j(i, j)
                                if tile_number in op_board.get_available_to_check():
                                    # op_board.get_board()[i][j].check_tile()
                                    if not (op_board.get_board()[i][j].check_tile()):
                                        turn += 1
                                    op_checked_tiles.append(tile_number)
                else:
                    pygame.mouse.set_cursor(*base)
            else:
                available_tiles_for_op = my_board.get_available_to_check()
                tile_number = random.randint(1, len(available_tiles_for_op))
                tile_to_check = available_tiles_for_op[tile_number - 1]
                i, j = Board.get_tile_numbers(tile_to_check)
                if not (my_board.get_board()[i][j].check_tile()):
                    turn += 1
        # op_rect = pygame.Rect(142, 176, 456, 376) (598, 552)
        # my_rect = pygame.Rect(775, 176, 456, 376) (1231, 552)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # play(event, x, y)
        pygame.display.update()
    pygame.quit()


def main():
    run_game()
    # print(str(computer_info['width']) + ", " + str(computer_info['height']))


if __name__ == "__main__":
    main()
