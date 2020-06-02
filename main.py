import pygame
from random import randrange
from config import Config
import board
import result


def randomColour():
    red = randrange(256)
    green = randrange(256)
    blue = randrange(256)
    return red, green, blue


def drawBoard(board):
    # Drawing grid
    blockSize = int(Config.Window.side / len(board))  # Set the size of the grid block
    for x in range(len(board)):
        for y in range(len(board)):
            rect = pygame.Rect(x * blockSize, y * blockSize,
                               blockSize, blockSize)
            pygame.draw.rect(SCREEN, Config.Grid.colour, rect, Config.Grid.thickness)

    # Drawing circles
    circleSize = int(Config.Window.side / len(board) / 4)  # Set the size of the grid block
    for x in range(len(board)):
        for y in range(len(board)):
            pygame.draw.circle(SCREEN, randomColour(),
                               ((x * blockSize) + circleSize, (y * blockSize) + circleSize), circleSize)


# pygame init
pygame.init()

# create the screen
SCREEN = pygame.display.set_mode(Config.Window.size)

# window caption
pygame.display.set_caption(Config.Window.caption)

# window logo
icon = pygame.image.load(Config.Window.iconPath)
pygame.display.set_icon(icon)

# TEST
BOARD = board.load("board_01.txt")
RESULT = result.load("result_01.txt")
print(BOARD)
print(RESULT)

# Action!
SCREEN.fill(Config.Window.backgroundColour)
drawBoard(BOARD)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()




