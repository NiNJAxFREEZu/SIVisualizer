import pygame
import sys
from math import pi
from config import Config
import puzzle_parser
import result
import FreeFlowSolver.SAT as SatSolver

def drawButton():
    # Drawing button rectangle
    pygame.draw.rect(SCREEN, Config.Window.buttonColour,
                     (0, Config.Window.side, Config.Window.side, Config.Window.buttonHeight))

    #Drawing button text
    myfont = pygame.font.SysFont('Arial', int(Config.Window.buttonHeight/2))
    textsurface = myfont.render(Config.Window.buttonText, False, (255, 255, 255))
    SCREEN.blit(textsurface, (Config.Window.side/2-40, Config.Window.side+5))

def drawBoard(board):
    # Drawing grid
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
            # draw circle border
            # pygame.draw.circle(SCREEN, Config.Circle.borderColour,
            #                    (int(x * blockSize + blockSize / 2), int(y * blockSize + blockSize / 2)), circleSize,
            #                    int(Config.Grid.thickness/2))


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

            #rect = pygame.Rect(x * blockSize, y * blockSize,
                               #     blockSize, blockSize)
            #pygame.draw.rect(SCREEN, colour, rect)
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

boardPath = "boards/board_7_03.txt"
# resultPath = "result_01.txt"

BOARD, COLORS_PARSED_INPUT = SatSolver.parse_puzzle(boardPath)
color_var, dir_vars, num_vars, clauses = SatSolver.reduce_to_sat(BOARD, COLORS_PARSED_INPUT)
_, SAT_DECODED_SOLUTION = SatSolver.solve_sat(BOARD, COLORS_PARSED_INPUT, color_var, dir_vars, clauses)

SWAPED_COLORS = dict([(str(value), str(key)) for key, value in COLORS_PARSED_INPUT.items()])

BOARD = puzzle_parser.parse_input_file_to_2d_array(BOARD)
COLOR_RESULT, DIR_RESULT = puzzle_parser.parse_result_to_2d_array(SAT_DECODED_SOLUTION, SWAPED_COLORS)

# Action!
SCREEN.fill(Config.Window.backgroundColour)
drawButton()
drawBoard(BOARD)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # If solve button was pressed
            if pos[1] > Config.Window.side:
                drawResult(COLOR_RESULT, DIR_RESULT)
                #drawBoard(BOARD)

    pygame.display.update()
