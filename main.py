import pygame
import sys
from math import pi
from config import Config
import puzzle_parser
import result
import random
import FreeFlowSolver.SAT as SatSolver

def drawButton():
    # Drawing button rectangle
    pygame.draw.rect(SCREEN, Config.Window.buttonColour,
                     (0, Config.Window.side, Config.Window.side, Config.Window.buttonHeight))

    pygame.draw.rect(SCREEN, Config.Window.buttonColour_01,
                     (0, Config.Window.side+Config.Window.buttonHeight, Config.Window.side+Config.Window.buttonHeight,
                      Config.Window.buttonHeight))

    pygame.draw.rect(SCREEN, Config.Window.buttonColour_02,
                     (0, Config.Window.side+2*Config.Window.buttonHeight, Config.Window.side+2* Config.Window.buttonHeight,
                      Config.Window.buttonHeight))

    pygame.draw.rect(SCREEN, Config.Window.buttonColour_03,
                     (0, Config.Window.side+3*Config.Window.buttonHeight, Config.Window.side+3*Config.Window.buttonHeight,
                      Config.Window.buttonHeight))

    #Drawing button text
    myfont = pygame.font.SysFont('Arial', int(Config.Window.buttonHeight/2))
    textsurface = myfont.render(Config.Window.buttonText, False, (255, 255, 255))
    SCREEN.blit(textsurface, (Config.Window.side/2-40, Config.Window.side+5))

    textsurface_01 = myfont.render(Config.Window.buttonText_01, False, (255, 255, 255))
    SCREEN.blit(textsurface_01, (Config.Window.side / 2 - 35, Config.Window.side + Config.Window.buttonHeight+5))

    textsurface_02 = myfont.render(Config.Window.buttonText_02, False, (255, 255, 255))
    SCREEN.blit(textsurface_02, (Config.Window.side / 2 - 35, Config.Window.side + 2*Config.Window.buttonHeight+5))

    textsurface_03 = myfont.render(Config.Window.buttonText_03, False, (255, 255, 255))
    SCREEN.blit(textsurface_03, (Config.Window.side / 2 - 50, Config.Window.side + 3*Config.Window.buttonHeight+5))

def drawBoard(board):
    # Drawing grid
    rect = pygame.Rect(0,0,Config.Window.side, Config.Window.side)
    pygame.draw.rect(SCREEN, (255,255,255), rect)

    blockSize = int(Config.Window.side / len(board))  # Set the size of the grid block
    for x in range(len(board)):
        for y in range(len(board)):
            rect = pygame.Rect(x * blockSize, y * blockSize,
                               blockSize, blockSize)
            pygame.draw.rect(SCREEN, Config.Grid.colour, rect, Config.Grid.thickness)

    # Drawing circles
    circleSize = int(blockSize / 3)
    for x in range(len(board)):
        for y in range(len(board)):
            colour = board[y][x]
            if colour == 'blank':
                continue
            # draw circle
            pygame.draw.circle(SCREEN, colour,
                               (int(x * blockSize + blockSize / 2), int(y * blockSize + blockSize / 2)), circleSize)


def drawResult(colors, dirs):

    def drawDir(dirtype, colour, x, y):
        line_width=int(blockSize / 10)
        top = (x * blockSize + blockSize/2, y * blockSize-(blockSize/2))
        bottom = (x * blockSize + blockSize/2, (y+1) * blockSize+blockSize/5)
        left = (x * blockSize-(blockSize/5), y * blockSize + blockSize / 2)
        right = ((x+1) * blockSize+blockSize/5, y * blockSize + blockSize / 2)
        middle = (x * blockSize + blockSize / 2, y * blockSize + (blockSize / 2))

        # straight line from top to bottom
        if(dirtype==12): pygame.draw.line(SCREEN, colour, top, bottom, line_width)

        #straight line from left to right
        elif(dirtype==3): pygame.draw.line(SCREEN, colour, left, right, line_width)

        #turn from top to left
        elif(dirtype==5):
            pygame.draw.line(SCREEN, colour, top, middle, line_width)
            pygame.draw.line(SCREEN, colour, (x * blockSize - (blockSize / 5), y * blockSize + blockSize / 2),
                              ((x + 1) * blockSize - blockSize / 2+line_width/2, y * blockSize + blockSize / 2), line_width)

        #turn from top to right
        elif (dirtype == 6):
            pygame.draw.line(SCREEN, colour, top, middle, line_width)
            pygame.draw.line(SCREEN, colour, (x * blockSize + (blockSize / 2)-line_width/3, y * blockSize + blockSize / 2),
                             ((x + 1) * blockSize + blockSize / 2 + line_width/2, y * blockSize + blockSize / 2),
                             line_width)

        #from bottom to right
        elif(dirtype==10):
            pygame.draw.line(SCREEN, colour, bottom, middle, line_width)
            pygame.draw.line(SCREEN, colour,
                             (x * blockSize + (blockSize / 2)-line_width/3, y * blockSize + blockSize / 2),
                             ((x + 1) * blockSize + blockSize / 2 + line_width / 2, y * blockSize + blockSize / 2),
                             line_width)

        #from bottom to left
        if(dirtype==9):
            pygame.draw.line(SCREEN, colour, bottom, middle, line_width)
            pygame.draw.line(SCREEN, colour, (x * blockSize - (blockSize / 5), y * blockSize + blockSize / 2),
                            (x * blockSize+blockSize/2+line_width/2, y * blockSize + blockSize / 2), line_width)

    # Drawing grid
    blockSize = int(Config.Window.side / len(colors))  # Set the size of the grid block
    for x in range(len(colors)):
        for y in range(len(colors)):
            colour = colors[x][y]
            dirtype = dirs[x][y]
            drawDir(dirtype, colour, y, x)


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

boards_3 = ["boards/board_3_01.txt"]
boards_5 = ["boards/board_5_01.txt", "boards/board_5_02.txt", "boards/board_5_03.txt"]
boards_7 = ["boards/board_7_01.txt", "boards/board_7_02.txt", "boards/board_7_03.txt"]
boards_10 = ["boards/board_10_01.txt", "boards/board_10_02.txt", "boards/board_10_03.txt"]

boardPath = "boards/board_7_02.txt"

def loadBoard(path):
    BOARD, COLORS_PARSED_INPUT = SatSolver.parse_puzzle(path)
    color_var, dir_vars, num_vars, clauses = SatSolver.reduce_to_sat(BOARD, COLORS_PARSED_INPUT)
    _, SAT_DECODED_SOLUTION = SatSolver.solve_sat(BOARD, COLORS_PARSED_INPUT, color_var, dir_vars, clauses)

    SWAPED_COLORS = dict([(str(value), str(key)) for key, value in COLORS_PARSED_INPUT.items()])

    BOARD = puzzle_parser.parse_input_file_to_2d_array(BOARD)
    COLOR_RESULT, DIR_RESULT = puzzle_parser.parse_result_to_2d_array(SAT_DECODED_SOLUTION, SWAPED_COLORS)
    return BOARD, COLOR_RESULT, DIR_RESULT

# Action!
SCREEN.fill(Config.Window.backgroundColour)
drawButton()
BOARD, COLOR_RESULT, DIR_RESULT = loadBoard(boardPath)
drawBoard(BOARD)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # If solve button was pressed
            if pos[1] < Config.Window.side + Config.Window.buttonHeight:
                drawResult(COLOR_RESULT, DIR_RESULT)
                #drawBoard(BOARD)

            elif pos[1] < Config.Window.side + 2*Config.Window.buttonHeight:
                print("3x3")
                boardPath = random.choice(boards_3)
                BOARD, COLOR_RESULT, DIR_RESULT = loadBoard(boardPath)
                drawBoard(BOARD)

            elif pos[1] < Config.Window.side + 3*Config.Window.buttonHeight:
                print("5x5")
                boardPath = random.choice(boards_5)
                BOARD, COLOR_RESULT, DIR_RESULT = loadBoard(boardPath)
                drawBoard(BOARD)

            else:
                print("10x10")
                boardPath = random.choice(boards_10)
                BOARD, COLOR_RESULT, DIR_RESULT = loadBoard(boardPath)
                drawBoard(BOARD)

    pygame.display.update()
