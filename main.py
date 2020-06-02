import pygame
import sys
from config import Config
import puzzle_parser
import result


def drawBoard(board):
    # Drawing grid
    blockSize = int(Config.Window.side / len(board))  # Set the size of the grid block
    for x in range(len(board)):
        for y in range(len(board)):
            rect = pygame.Rect(x * blockSize, y * blockSize,
                               blockSize, blockSize)
            pygame.draw.rect(SCREEN, Config.Grid.colour, rect, Config.Grid.thickness)

    # Drawing circles
    circleSize = int(blockSize / 4)
    for x in range(len(board)):
        for y in range(len(board)):
            colour = board[y][x]
            if colour == 'blank':
                continue
            # draw circle
            pygame.draw.circle(SCREEN, colour,
                               (int(x * blockSize + blockSize / 2), int(y * blockSize + blockSize / 2)), circleSize)
            # draw circle border
            pygame.draw.circle(SCREEN, Config.Circle.borderColour,
                               (int(x * blockSize + blockSize / 2), int(y * blockSize + blockSize / 2)), circleSize, int(Config.Grid.thickness / 2))


def drawResult(result):
    # Drawing grid
    blockSize = int(Config.Window.side / len(result))  # Set the size of the grid block
    for x in range(len(result)):
        for y in range(len(result)):
            colour = result[y][x]
            rect = pygame.Rect(x * blockSize, y * blockSize,
                               blockSize, blockSize)
            pygame.draw.rect(SCREEN, colour, rect)


# pygame init
pygame.init()

# create the screen
SCREEN = pygame.display.set_mode(Config.Window.size)

# window caption
pygame.display.set_caption(Config.Window.caption)

# window logo
icon = pygame.image.load(Config.Window.iconPath)
pygame.display.set_icon(icon)

# load parameters
# if len(sys.argv) != 3:
    # sys.stderr.write("ERROR: Amount of parameters don't match!\n")
    # sys.stderr.write("Try using: visualizer.py [board-file-path] [result-file-path]")
    # exit(1)

# boardPath = str(sys.argv[1])
# resultPath = str(sys.argv[2])

boardPath = "board_01.txt"
resultPath = "result_01.txt"

BOARD = puzzle_parser.parse_input_file_to_2d_array(boardPath)
RESULT = puzzle_parser.parse_result_to_2d_array(resultPath, puzzle_parser.c)

# Action!
SCREEN.fill(Config.Window.backgroundColour)
drawBoard(BOARD)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawResult(RESULT)
            drawBoard(BOARD)

    pygame.display.update()




