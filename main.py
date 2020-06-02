import pygame
from config import Config
from board import Board
from result import Result

# pygame init
pygame.init()

# create the screen
screen = pygame.display.set_mode(Config.Window.size)

# window caption
pygame.display.set_caption(Config.Window.caption)

# window logo
icon = pygame.image.load(Config.Window.iconPath)
pygame.display.set_icon(icon)

# TEST
board = Board.load("board_01.txt")
print(board)
print(len(board))

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(Config.Window.backgroundColour)
    pygame.display.update()


